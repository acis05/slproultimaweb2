import hashlib, hmac, secrets
from datetime import datetime, timedelta, timezone
PBKDF2_ITERATIONS = 240_000
def hash_password(password):
    if len(password) < 8: raise ValueError("Password minimal 8 karakter.")
    salt = secrets.token_bytes(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, PBKDF2_ITERATIONS)
    return f"pbkdf2_sha256${PBKDF2_ITERATIONS}${salt.hex()}${digest.hex()}"
def verify_password(password, encoded):
    try:
        alg, it, salt, digest = encoded.split("$", 3)
        actual = hashlib.pbkdf2_hmac("sha256", password.encode(), bytes.fromhex(salt), int(it))
        return alg == "pbkdf2_sha256" and hmac.compare_digest(actual.hex(), digest)
    except Exception: return False
def new_token(): return secrets.token_urlsafe(36)
def utc_now(): return datetime.now(timezone.utc).isoformat()
def expires_at(hours): return (datetime.now(timezone.utc)+timedelta(hours=hours)).isoformat()
def is_expired(value):
    try: return datetime.fromisoformat(value) <= datetime.now(timezone.utc)
    except Exception: return True
