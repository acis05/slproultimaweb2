import base64
import ctypes
import json
import os
import threading
from datetime import datetime, timezone, timedelta
from pathlib import Path

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey
from cryptography.exceptions import InvalidSignature

from .config import BASE_DIR, DATA_DIR, WEB_MODE
from . import subscription

APP_ID = 'STOKLEDGER-PRO-ULTIMA'
TRIAL_TRANSACTION_LIMIT = 100
TRIAL_USER_LIMIT = 3
DEVICE_HEARTBEAT_SECONDS = 5
DEVICE_IDLE_SECONDS = 10
TRIAL_DEVICE_IDLE_MINUTES = 30  # kompatibilitas konfigurasi lama
LICENSED_USER_LIMIT = 3
LICENSE_FILENAME = 'STOKLEDGER_PRO_ULTIMA.LIC'
REBIND_FILENAME = 'STOKLEDGER_PRO_ULTIMA_REBIND.AUTH'
PUBLIC_KEY_PEM = b"""-----BEGIN PUBLIC KEY-----
MCowBQYDK2VwAyEAHEygdmEtNHK7fKGJpkeiJjSZiJrLxh5LKEFu7tDYiB4=
-----END PUBLIC KEY-----
"""
BINDING_FILE = DATA_DIR / "dongle_binding.json"
_BINDING_WRITE_LOCK = threading.RLock()



def normalize_serial(value):
    text = str(value or "").strip().upper().replace("0X", "")
    return "".join(ch for ch in text if ch in "0123456789ABCDEF")


def _read_binding():
    try:
        data = json.loads(BINDING_FILE.read_text(encoding="utf-8"))
        if data.get("app_id") != APP_ID:
            return None
        serial = normalize_serial(data.get("dongle_serial"))
        if not serial:
            return None
        # Kompatibel dengan binding schema v1 yang masih menyimpan license_id.
        data["dongle_serial"] = serial
        return data
    except Exception:
        return None


def _write_binding(license_data, *, rebound_from=None):
    # current_license_status() dipanggil oleh banyak request browser secara paralel.
    # Serialisasi seluruh read/write binding agar thread tidak berebut file temporary.
    with _BINDING_WRITE_LOCK:
        old = _read_binding() or {}
        now = datetime.now(timezone.utc).isoformat()
        payload = {
            "schema_version": 2,
            "app_id": APP_ID,
            "dongle_serial": normalize_serial(license_data.get("dongle_serial")),
            "customer": str(license_data.get("customer") or old.get("customer") or ""),
            "activated_at": str(old.get("activated_at") or now),
            "last_seen_at": now,
            # Hanya metadata/audit. license_id TIDAK dipakai untuk menentukan binding.
            "last_license_id": str(license_data.get("license_id") or ""),
        }
        if rebound_from:
            payload["rebound_from"] = normalize_serial(rebound_from)
            payload["rebound_at"] = now
        BINDING_FILE.parent.mkdir(parents=True, exist_ok=True)

        # Nama temp unik mencegah benturan jika suatu saat ada lebih dari satu proses.
        temp = BINDING_FILE.with_name(
            f"{BINDING_FILE.stem}.{os.getpid()}.{threading.get_ident()}.tmp"
        )
        try:
            temp.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
            os.replace(str(temp), str(BINDING_FILE))
        finally:
            try:
                temp.unlink(missing_ok=True)
            except Exception:
                pass


def _windows_drive_type(root):
    if os.name != "nt":
        return None
    return int(ctypes.windll.kernel32.GetDriveTypeW(ctypes.c_wchar_p(root)))


def _is_removable_license_path(path):
    if os.environ.get("STOKLEDGER_ALLOW_TEST_LICENSE") == "1":
        return True
    if os.name != "nt":
        return False
    root = Path(path).drive + "\\"
    return bool(root and _windows_drive_type(root) == 2)


def _canonical(payload):
    return json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def _windows_volume_serial(root):
    serial = ctypes.c_uint32()
    max_component = ctypes.c_uint32()
    flags = ctypes.c_uint32()
    volume_name = ctypes.create_unicode_buffer(261)
    fs_name = ctypes.create_unicode_buffer(261)
    ok = ctypes.windll.kernel32.GetVolumeInformationW(
        ctypes.c_wchar_p(root), volume_name, len(volume_name), ctypes.byref(serial),
        ctypes.byref(max_component), ctypes.byref(flags), fs_name, len(fs_name)
    )
    if not ok:
        return None
    return f"{serial.value:08X}", volume_name.value


def _windows_usb_roots():
    drives = ctypes.windll.kernel32.GetLogicalDrives()
    result = []
    for index in range(26):
        if not drives & (1 << index):
            continue
        root = f"{chr(65 + index)}:\\"
        drive_type = ctypes.windll.kernel32.GetDriveTypeW(ctypes.c_wchar_p(root))
        if drive_type == 2:
            result.append(root)
    return result


def candidate_license_locations():
    locations = []
    override = os.environ.get("STOKLEDGER_LICENSE_FILE")
    if override:
        locations.append(Path(override))
    if os.name == "nt":
        for root in _windows_usb_roots():
            locations.append(Path(root) / LICENSE_FILENAME)
    locations.append(BASE_DIR / "license" / LICENSE_FILENAME)
    seen = set()
    for item in locations:
        key = str(item).lower()
        if key not in seen:
            seen.add(key)
            yield item


def _serial_for_license_path(path):
    forced = os.environ.get("STOKLEDGER_DONGLE_SERIAL")
    if forced:
        return normalize_serial(forced), "TEST"
    if os.name != "nt":
        return None, None
    root = path.drive + "\\"
    if not root or len(root) < 3:
        return None, None
    info = _windows_volume_serial(root)
    return info if info else (None, None)


def _public_key():
    key = serialization.load_pem_public_key(PUBLIC_KEY_PEM)
    if not isinstance(key, Ed25519PublicKey):
        raise ValueError("Kunci lisensi tidak valid.")
    return key


def verify_license_file(path):
    try:
        raw = json.loads(Path(path).read_text(encoding="utf-8"))
        payload = raw["payload"]
        signature = base64.b64decode(raw["signature"], validate=True)
        _public_key().verify(signature, _canonical(payload))
        if payload.get("app_id") != APP_ID:
            return None, 'Lisensi bukan untuk StokLedger Online.'
        if payload.get("license_type") != "LIFETIME":
            return None, "Jenis lisensi tidak didukung."
        if not _is_removable_license_path(Path(path)):
            return None, "File lisensi harus berada di root USB removable yang terdaftar."
        expected = normalize_serial(payload.get("dongle_serial"))
        actual, volume_label = _serial_for_license_path(Path(path))
        if not expected or not actual or expected != actual:
            return None, "Lisensi tidak cocok dengan dongle USB yang terpasang."
        max_users = int(payload.get("max_users") or 0)
        if max_users < 1 or max_users > LICENSED_USER_LIMIT:
            return None, "Batas user pada lisensi tidak valid."
        return {
            "mode": "LICENSED",
            "license_type": "LIFETIME",
            "customer": str(payload.get("customer") or "").strip(),
            "license_id": str(payload.get("license_id") or "").strip(),
            "dongle_serial": expected,
            "dongle_label": volume_label or "",
            "max_users": max_users,
            "license_path": str(path),
            "issued_at": payload.get("issued_at"),
        }, None
    except FileNotFoundError:
        return None, None
    except (InvalidSignature, ValueError, KeyError, TypeError, json.JSONDecodeError):
        return None, "File lisensi rusak atau tanda tangan tidak sah."
    except Exception:
        return None, "Lisensi tidak dapat dibaca."


def _verify_rebind_authorization(path, old_serial, new_serial):
    try:
        auth_path = Path(path).parent / REBIND_FILENAME
        if not auth_path.exists():
            return False, "Izin rebind tidak ditemukan."
        raw = json.loads(auth_path.read_text(encoding="utf-8"))
        payload = raw["payload"]
        signature = base64.b64decode(raw["signature"], validate=True)
        _public_key().verify(signature, _canonical(payload))
        if payload.get("app_id") != APP_ID or payload.get("action") != "REBIND_DONGLE":
            return False, "Izin rebind bukan untuk edisi aplikasi ini."
        if normalize_serial(payload.get("old_dongle_serial")) != normalize_serial(old_serial):
            return False, "Serial dongle lama pada izin rebind tidak sesuai."
        if normalize_serial(payload.get("new_dongle_serial")) != normalize_serial(new_serial):
            return False, "Serial dongle baru pada izin rebind tidak sesuai."
        expires = str(payload.get("expires_at") or "")
        if expires:
            expiry = datetime.fromisoformat(expires.replace("Z", "+00:00"))
            if expiry.tzinfo is None:
                expiry = expiry.replace(tzinfo=timezone.utc)
            if datetime.now(timezone.utc) > expiry.astimezone(timezone.utc):
                return False, "Izin rebind sudah kedaluwarsa."
        return True, auth_path
    except (InvalidSignature, ValueError, KeyError, TypeError, json.JSONDecodeError):
        return False, "Izin rebind rusak atau tanda tangan tidak sah."
    except Exception as exc:
        return False, f"Izin rebind tidak dapat dibaca: {exc}"


def _ensure_trial_usage_schema(connection):
    connection.execute("""CREATE TABLE IF NOT EXISTS trial_usage_events(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        event_key TEXT NOT NULL UNIQUE,
        event_type TEXT NOT NULL,
        reference_no TEXT,
        source_table TEXT,
        source_id TEXT,
        units INTEGER NOT NULL DEFAULT 1,
        active INTEGER NOT NULL DEFAULT 1,
        created_at TEXT NOT NULL,
        released_at TEXT
    )""")
    columns={row[1] for row in connection.execute("PRAGMA table_info(trial_usage_events)")}
    if 'active' not in columns:
        connection.execute("ALTER TABLE trial_usage_events ADD COLUMN active INTEGER NOT NULL DEFAULT 1")
    if 'released_at' not in columns:
        connection.execute("ALTER TABLE trial_usage_events ADD COLUMN released_at TEXT")
    marker = connection.execute("SELECT 1 FROM trial_usage_events WHERE event_key='BOOTSTRAP-COMPLETE'").fetchone()
    if not marker:
        rows = connection.execute("SELECT id,COALESCE(source_type,'JOURNAL') source_type,reference_no,created_at FROM journal_entries WHERE status='POSTED' ORDER BY id").fetchall()
        for row in rows:
            connection.execute("""INSERT OR IGNORE INTO trial_usage_events(
              event_key,event_type,reference_no,source_table,source_id,units,created_at
            ) VALUES(?,?,?,?,?,1,?)""",(
              f"LEGACY-JOURNAL-{row['id']}",str(row['source_type'] or 'JOURNAL'),row['reference_no'],
              'journal_entries',str(row['id']),row['created_at'] or datetime.now(timezone.utc).isoformat()))
        connection.execute("""INSERT OR IGNORE INTO trial_usage_events(
          event_key,event_type,reference_no,source_table,source_id,units,created_at
        ) VALUES('BOOTSTRAP-COMPLETE','SYSTEM',NULL,NULL,NULL,0,?)""",(datetime.now(timezone.utc).isoformat(),))


def _trial_transaction_count(connection):
    _ensure_trial_usage_schema(connection)
    return int(connection.execute("""SELECT COUNT(*) FROM (
        SELECT CASE WHEN COALESCE(TRIM(reference_no),'')<>''
                    THEN COALESCE(NULLIF(TRIM(event_type),''),'TRANSACTION')||'|'||TRIM(reference_no)
                    ELSE event_key END logical_key
        FROM trial_usage_events WHERE active=1 AND COALESCE(units,0)>0
        GROUP BY logical_key
    )""").fetchone()[0])


def current_license_status(connection=None):
    if WEB_MODE:
        if connection is None:
            from .database import connect
            c=connect()
            try:return subscription.status(c)
            finally:c.close()
        return subscription.status(connection)
    errors = []
    for path in candidate_license_locations():
        if not path.exists():
            continue
        license_data, error = verify_license_file(path)
        if license_data:
            binding = _read_binding()
            serial = normalize_serial(license_data.get("dongle_serial"))
            if not binding:
                _write_binding(license_data)
            else:
                bound_serial = normalize_serial(binding.get("dongle_serial"))
                if bound_serial == serial:
                    # Migrasi otomatis dari binding lama yang memakai license_id.
                    _write_binding(license_data)
                else:
                    ok, auth = _verify_rebind_authorization(path, bound_serial, serial)
                    if not ok:
                        errors.append(
                            f"Aplikasi terikat ke dongle serial {bound_serial}. "
                            f"Dongle baru {serial} memerlukan izin rebind dari generator internal. {auth}"
                        )
                        continue
                    _write_binding(license_data, rebound_from=bound_serial)
                    try:
                        Path(auth).unlink(missing_ok=True)
                    except Exception:
                        pass
            license_data["transaction_limit"] = None
            license_data["license_valid"] = True
            license_data["device_limit"] = int(license_data.get("max_users") or 1)
            if connection is not None:
                try:
                    license_data["active_devices"] = int(connection.execute(
                        "SELECT COUNT(DISTINCT COALESCE(NULLIF(device_id,''),client_ip||':'||client_name)) FROM sessions WHERE expires_at>?",
                        (datetime.now(timezone.utc).isoformat(),)).fetchone()[0])
                except Exception:
                    license_data["active_devices"] = 0
            else:
                license_data["active_devices"] = 0
            return license_data
        if error:
            errors.append(error)
    # Lifetime dongle adalah upgrade. Tanpa USB, aplikasi otomatis kembali ke trial 100 transaksi.
    # Binding tetap disimpan untuk memvalidasi dongle saat USB dipasang kembali.
    binding = _read_binding()
    transaction_count = 0
    active_users = 0
    if connection is not None:
        transaction_count = _trial_transaction_count(connection)
        active_users = int(connection.execute("SELECT COUNT(*) FROM users WHERE is_active=1").fetchone()[0])
    remaining = max(0, TRIAL_TRANSACTION_LIMIT - transaction_count)
    active_devices = 0
    if connection is not None:
        try:
            active_devices = int(connection.execute(
                "SELECT COUNT(DISTINCT COALESCE(NULLIF(device_id,''),client_ip||':'||client_name)) FROM sessions WHERE expires_at>? AND last_seen_at>=?",
                (datetime.now(timezone.utc).isoformat(), (datetime.now(timezone.utc)-timedelta(seconds=DEVICE_IDLE_SECONDS)).isoformat())).fetchone()[0])
        except Exception:
            active_devices = 0
    return {
        "mode": "TRIAL",
        "license_type": "TRIAL",
        "license_valid": False,
        "max_users": TRIAL_USER_LIMIT,
        "device_limit": TRIAL_USER_LIMIT,
        "active_devices": active_devices,
        "transaction_limit": TRIAL_TRANSACTION_LIMIT,
        "transaction_count": transaction_count,
        "transactions_remaining": remaining,
        "active_users": active_users,
        "error": errors[0] if errors else None,
    }


def enforce_transaction_capacity(connection, units=1):
    if WEB_MODE:
        st=current_license_status(connection)
        if not st.get('license_valid'):
            raise ValueError('Masa trial/langganan telah berakhir. Hubungi administrator untuk aktivasi.')
        return st
    units = int(units or 0)
    if units < 0:
        raise ValueError("Jumlah transaksi trial tidak valid.")
    status = current_license_status(connection)
    if status["mode"] == "DONGLE_REQUIRED":
        raise ValueError(status.get("error") or "Dongle lisensi wajib terpasang.")
    if status["mode"] == "TRIAL" and status["transaction_count"] + units > TRIAL_TRANSACTION_LIMIT:
        raise ValueError(
            f"Batas trial maksimal {TRIAL_TRANSACTION_LIMIT} transaksi. "
            f"Sisa kuota {status['transactions_remaining']} transaksi, sedangkan proses ini membutuhkan {units} transaksi. "
            "Hubungkan dongle lisensi lifetime untuk melanjutkan."
        )
    return status


def record_transaction_usage(connection, *, event_key, event_type, reference_no=None,
                             source_table=None, source_id=None, units=1):
    status = current_license_status(connection)
    if WEB_MODE:
        enforce_transaction_capacity(connection, units)
        return status
    if status["mode"] != "TRIAL":
        return status
    enforce_transaction_capacity(connection, units)
    now=datetime.now(timezone.utc).isoformat()
    existing=connection.execute("SELECT id,active FROM trial_usage_events WHERE event_key=?",(str(event_key),)).fetchone()
    if existing:
        if not int(existing['active']):
            enforce_transaction_capacity(connection, units)
            connection.execute("UPDATE trial_usage_events SET active=1,units=?,released_at=NULL,created_at=? WHERE id=?",(int(units),now,existing['id']))
    else:
        connection.execute("""INSERT INTO trial_usage_events(
          event_key,event_type,reference_no,source_table,source_id,units,active,created_at
        ) VALUES(?,?,?,?,?,?,1,?)""",(
          str(event_key),str(event_type or 'TRANSACTION'),reference_no,source_table,
          str(source_id) if source_id is not None else None,int(units),now))
    return current_license_status(connection)


def release_transaction_usage(connection, *, source_table=None, source_id=None, event_key=None, units=None):
    status=current_license_status(connection)
    if WEB_MODE:
        return status
    if status['mode']!='TRIAL':
        return status
    clauses=['active=1']; params=[]
    if event_key is not None:
        clauses.append('event_key=?'); params.append(str(event_key))
    if source_table is not None:
        clauses.append('source_table=?'); params.append(str(source_table))
    if source_id is not None:
        clauses.append('source_id=?'); params.append(str(source_id))
    if len(clauses)==1:
        return status
    now=datetime.now(timezone.utc).isoformat()
    sql='UPDATE trial_usage_events SET active=0,released_at=? WHERE '+' AND '.join(clauses)
    params=[now]+params
    if units is None:
        connection.execute(sql,params)
    else:
        rows=connection.execute('SELECT id,units FROM trial_usage_events WHERE '+' AND '.join(clauses)+' ORDER BY id',params[1:]).fetchall()
        remaining=int(units)
        for row in rows:
            if remaining<=0: break
            connection.execute('UPDATE trial_usage_events SET active=0,released_at=? WHERE id=?',(now,row['id']))
            remaining-=int(row['units'] or 1)
    return current_license_status(connection)


def enforce_transaction_limit(connection):
    return enforce_transaction_capacity(connection, 1)


def enforce_user_limit(connection, activating_new_user=False):
    status = current_license_status(connection)
    if status.get("mode") == "DONGLE_REQUIRED":
        raise ValueError(status.get("error") or "Dongle lisensi wajib terpasang.")
    active = int(connection.execute("SELECT COUNT(*) FROM users WHERE is_active=1").fetchone()[0])
    projected = active + (1 if activating_new_user else 0)
    if projected > int(status["max_users"]):
        mode = 'trial/langganan' if WEB_MODE else ("trial" if status["mode"] == "TRIAL" else "lisensi lifetime")
        raise ValueError(f"Batas {mode} maksimal {status['max_users']} user aktif telah tercapai.")
    return status


def public_status(connection=None):
    return current_license_status(connection)
