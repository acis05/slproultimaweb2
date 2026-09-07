"""PostgreSQL compatibility layer for the legacy StokLedger SQL repository.

The desktop codebase was written against sqlite3's convenient Connection.execute()
API and qmark placeholders.  The web PostgreSQL edition keeps that repository API
stable while translating the small SQLite dialect surface used by StokLedger.
"""
from __future__ import annotations

import re
from typing import Any, Iterable

import psycopg
from psycopg import errors as pg_errors

IntegrityError = psycopg.IntegrityError
OperationalError = psycopg.OperationalError
DatabaseError = psycopg.DatabaseError


class CompatRow(dict):
    """Mapping row with sqlite.Row-style numeric indexing."""
    __slots__ = ("_values",)

    def __init__(self, columns, values):
        super().__init__(zip(columns, values))
        self._values = tuple(values)

    def __getitem__(self, key):
        if isinstance(key, int):
            return self._values[key]
        return super().__getitem__(key)


def _qmark_to_pyformat(sql: str) -> str:
    # StokLedger SQL does not use '?' as an operator. Keep quoted question marks
    # untouched so text literals remain safe.
    out = []
    quote = None
    i = 0
    while i < len(sql):
        ch = sql[i]
        if quote:
            out.append(ch)
            if ch == quote:
                if i + 1 < len(sql) and sql[i + 1] == quote:
                    out.append(sql[i + 1]); i += 1
                else:
                    quote = None
        else:
            if ch in ("'", '"'):
                quote = ch; out.append(ch)
            elif ch == '?':
                out.append('%s')
            else:
                out.append(ch)
        i += 1
    return ''.join(out)


def _convert_insert_or_replace(sql: str) -> str:
    m = re.match(r"\s*INSERT\s+OR\s+REPLACE\s+INTO\s+([\w\"]+)\s*\((.*?)\)\s*VALUES\s*\((.*?)\)\s*$",
                 sql, flags=re.I | re.S)
    if not m:
        return re.sub(r"\bINSERT\s+OR\s+REPLACE\s+INTO\b", "INSERT INTO", sql, flags=re.I)
    table, col_text, values = m.groups()
    cols = [c.strip().strip('"') for c in col_text.split(',')]
    conflict = 'id' if 'id' in [x.lower() for x in cols] else cols[0]
    updates = [f'"{c}"=EXCLUDED."{c}"' for c in cols if c.lower() != conflict.lower()]
    return f'INSERT INTO {table} ({col_text}) VALUES ({values}) ON CONFLICT ("{conflict}") DO UPDATE SET ' + ','.join(updates)


def normalize_sql(sql: str) -> str:
    s = str(sql)
    s = re.sub(r"\s+COLLATE\s+NOCASE\b", "", s, flags=re.I)
    s = re.sub(r"\bCAST\((.*?)\s+AS\s+REAL\)", r"CAST(\1 AS DOUBLE PRECISION)", s, flags=re.I | re.S)
    s = re.sub(r"\bMAX\s*\(\s*0\s*,", "GREATEST(0,", s, flags=re.I)
    s = re.sub(r"\bMIN\s*\(\s*0\s*,", "LEAST(0,", s, flags=re.I)
    s = re.sub(r"CAST\(julianday\(date\(COALESCE\(bp\.opening_balance_date,\?\),\s*'\+'\|\|COALESCE\(bp\.payment_term_days,0\)\|\|' day'\)\)-julianday\(\?\) AS INTEGER\)",
               "((COALESCE(CAST(bp.opening_balance_date AS date),CAST(? AS date)) + COALESCE(bp.payment_term_days,0) * INTERVAL '1 day')::date-CAST(? AS date))", s, flags=re.I)
    s = re.sub(r"\bdate\s*\(\s*'now'\s*\)", "TO_CHAR(CURRENT_DATE,'YYYY-MM-DD')", s, flags=re.I)
    # SQLite date arithmetic used by dashboard due-date queries. Dates are stored
    # as ISO text in the legacy schema, so cast only while calculating.
    s = re.sub(r"date\(COALESCE\(bp\.opening_balance_date,\?\),\s*'\+'\|\|COALESCE\(bp\.payment_term_days,0\)\|\|' day'\)",
               "TO_CHAR((COALESCE(CAST(bp.opening_balance_date AS date),CAST(? AS date)) + COALESCE(bp.payment_term_days,0) * INTERVAL '1 day')::date,'YYYY-MM-DD')", s, flags=re.I)
    s = re.sub(r"CAST\(julianday\(COALESCE\(\?,TO_CHAR\(CURRENT_DATE,'YYYY-MM-DD'\)\)\)-julianday\(COALESCE\(s\.due_date,s\.sale_date\)\) AS INTEGER\)",
               "(COALESCE(CAST(? AS date),CURRENT_DATE)-COALESCE(CAST(s.due_date AS date),CAST(s.sale_date AS date)))", s, flags=re.I)
    s = re.sub(r"CAST\(julianday\(COALESCE\(\?,TO_CHAR\(CURRENT_DATE,'YYYY-MM-DD'\)\)\)-julianday\(COALESCE\(p\.due_date,p\.purchase_date\)\) AS INTEGER\)",
               "(COALESCE(CAST(? AS date),CURRENT_DATE)-COALESCE(CAST(p.due_date AS date),CAST(p.purchase_date AS date)))", s, flags=re.I)
    s = re.sub(r"CAST\(julianday\(s\.due_date\)-julianday\(\?\) AS INTEGER\)", "(CAST(s.due_date AS date)-CAST(? AS date))", s, flags=re.I)
    s = re.sub(r"CAST\(julianday\(p\.due_date\)-julianday\(\?\) AS INTEGER\)", "(CAST(p.due_date AS date)-CAST(? AS date))", s, flags=re.I)
    if re.search(r"\bINSERT\s+OR\s+REPLACE\s+INTO\b", s, flags=re.I):
        s = _convert_insert_or_replace(s)
    elif re.search(r"\bINSERT\s+OR\s+IGNORE\s+INTO\b", s, flags=re.I):
        s = re.sub(r"\bINSERT\s+OR\s+IGNORE\s+INTO\b", "INSERT INTO", s, flags=re.I)
        if not re.search(r"\bON\s+CONFLICT\b", s, flags=re.I):
            s = s.rstrip().rstrip(';') + " ON CONFLICT DO NOTHING"
    # SQLite LIKE is case-insensitive for ASCII by default; ILIKE preserves the
    # behavior users expect in search fields.
    s = re.sub(r"\sLIKE\s", " ILIKE ", s, flags=re.I)
    return _qmark_to_pyformat(s)


def _split_sql_script(script: str):
    parts, current = [], []
    quote = None
    depth = 0
    i = 0
    while i < len(script):
        ch = script[i]
        if quote:
            current.append(ch)
            if ch == quote:
                if i + 1 < len(script) and script[i + 1] == quote:
                    current.append(script[i + 1]); i += 1
                else:
                    quote = None
        else:
            if ch in ("'", '"'):
                quote = ch; current.append(ch)
            elif ch == '(':
                depth += 1; current.append(ch)
            elif ch == ')':
                depth = max(0, depth - 1); current.append(ch)
            elif ch == ';' and depth == 0:
                text = ''.join(current).strip()
                if text: parts.append(text)
                current = []
            else:
                current.append(ch)
        i += 1
    text = ''.join(current).strip()
    if text: parts.append(text)
    return parts


def _split_top_level(body: str):
    parts, current = [], []
    quote = None
    depth = 0
    i = 0
    while i < len(body):
        ch = body[i]
        if quote:
            current.append(ch)
            if ch == quote:
                if i + 1 < len(body) and body[i + 1] == quote:
                    current.append(body[i + 1]); i += 1
                else:
                    quote = None
        else:
            if ch in ("'", '"'):
                quote = ch; current.append(ch)
            elif ch == '(':
                depth += 1; current.append(ch)
            elif ch == ')':
                depth -= 1; current.append(ch)
            elif ch == ',' and depth == 0:
                parts.append(''.join(current).strip()); current = []
            else:
                current.append(ch)
        i += 1
    if current: parts.append(''.join(current).strip())
    return parts


def _strip_fk_fragment(fragment: str) -> str | None:
    if re.match(r"^FOREIGN\s+KEY\b", fragment, flags=re.I):
        return None
    # PostgreSQL requires referenced tables to exist when CREATE TABLE runs.
    # The legacy schema was not topologically ordered, so initial bootstrap omits
    # inline FK clauses. Business-level validation remains in repository methods.
    fragment = re.sub(
        r"\s+REFERENCES\s+[\w\"]+\s*\([^)]*\)(?:\s+ON\s+DELETE\s+(?:CASCADE|SET\s+NULL|RESTRICT|NO\s+ACTION))?(?:\s+ON\s+UPDATE\s+(?:CASCADE|SET\s+NULL|RESTRICT|NO\s+ACTION))?",
        "", fragment, flags=re.I)
    return fragment


def postgres_schema(sqlite_schema: str) -> list[str]:
    cleaned = re.sub(r"^\s*PRAGMA\s+[^;]+;?\s*$", "", sqlite_schema, flags=re.I | re.M)
    statements = []
    for statement in _split_sql_script(cleaned):
        st = statement.strip()
        if not st:
            continue
        st = re.sub(r"\s+COLLATE\s+NOCASE\b", "", st, flags=re.I)
        st = re.sub(r"\bINTEGER\s+PRIMARY\s+KEY\s+AUTOINCREMENT\b", "BIGSERIAL PRIMARY KEY", st, flags=re.I)
        st = re.sub(r"\bAUTOINCREMENT\b", "", st, flags=re.I)
        st = re.sub(r"\bBLOB\b", "BYTEA", st, flags=re.I)
        st = re.sub(r"\bREAL\b", "DOUBLE PRECISION", st, flags=re.I)
        if re.match(r"^CREATE\s+TABLE", st, flags=re.I):
            first = st.find('('); last = st.rfind(')')
            if first > 0 and last > first:
                head, body, tail = st[:first+1], st[first+1:last], st[last:]
                frags = []
                for frag in _split_top_level(body):
                    f = _strip_fk_fragment(frag)
                    if f: frags.append(f)
                st = head + '\n  ' + ',\n  '.join(frags) + '\n' + tail
        statements.append(st)
    return statements


class PgCursor:
    def __init__(self, connection, cursor, sql: str = ''):
        self.connection = connection
        self.cursor = cursor
        self.sql = sql
        self.lastrowid = None
        self._columns = [d.name if hasattr(d, 'name') else d[0] for d in (cursor.description or [])]

    @property
    def rowcount(self):
        return self.cursor.rowcount

    @property
    def description(self):
        return self.cursor.description

    def _wrap(self, row):
        if row is None: return None
        return CompatRow(self._columns, row)

    def fetchone(self):
        return self._wrap(self.cursor.fetchone())

    def fetchall(self):
        return [self._wrap(r) for r in self.cursor.fetchall()]

    def __iter__(self):
        while True:
            row = self.cursor.fetchone()
            if row is None: break
            yield self._wrap(row)

    def close(self):
        self.cursor.close()


class PgConnection:
    def __init__(self, raw):
        self.raw = raw
        self._has_id_cache = {}

    def _table_has_id(self, table: str) -> bool:
        table = table.strip('"').lower()
        if table in self._has_id_cache:
            return self._has_id_cache[table]
        with self.raw.cursor() as cur:
            cur.execute("""SELECT EXISTS(SELECT 1 FROM information_schema.columns
                         WHERE table_schema=current_schema() AND table_name=%s AND column_name='id')""", (table,))
            result = bool(cur.fetchone()[0])
        self._has_id_cache[table] = result
        return result

    def execute(self, sql: str, params: Iterable[Any] | None = None):
        normalized = normalize_sql(sql)
        params = tuple(params or ())
        cur = self.raw.cursor()
        insert_match = re.match(r"\s*INSERT\s+INTO\s+([\w\"]+)", normalized, flags=re.I)
        wants_id = False
        if insert_match and ' RETURNING ' not in normalized.upper():
            table = insert_match.group(1)
            try: wants_id = self._table_has_id(table)
            except Exception: wants_id = False
            if wants_id:
                normalized = normalized.rstrip().rstrip(';') + ' RETURNING id'
        try:
            cur.execute(normalized, params)
            wrapper = PgCursor(self, cur, normalized)
            if wants_id:
                row = cur.fetchone()
                wrapper.lastrowid = row[0] if row else None
                wrapper._columns = []
            return wrapper
        except Exception:
            cur.close()
            raise

    def executemany(self, sql: str, seq_of_params):
        normalized = normalize_sql(sql)
        cur = self.raw.cursor()
        cur.executemany(normalized, seq_of_params)
        return PgCursor(self, cur, normalized)

    def executescript(self, script: str):
        for statement in postgres_schema(script):
            with self.raw.cursor() as cur:
                cur.execute(statement)
        self._has_id_cache.clear()
        return self

    def commit(self): self.raw.commit()
    def rollback(self): self.raw.rollback()
    def close(self): self.raw.close()

    def __enter__(self): return self
    def __exit__(self, typ, value, tb):
        if typ is None: self.commit()
        else: self.rollback()
        self.close()
        return False


def connect(database_url: str, schema: str | None = None) -> PgConnection:
    raw = psycopg.connect(database_url, autocommit=False)
    if schema:
        safe = str(schema).strip()
        if not re.match(r"^[A-Za-z_][A-Za-z0-9_]*$", safe):
            raw.close(); raise ValueError("Schema PostgreSQL tidak valid.")
        with raw.cursor() as cur:
            cur.execute(f'SET search_path TO "{safe}", public')
    return PgConnection(raw)
