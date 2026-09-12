from __future__ import annotations
import base64, hashlib, hmac, os, secrets, struct, time
from urllib.parse import urlparse

def normalize_origin(value: str) -> str:
    value=str(value or '').strip()
    if not value:return ''
    try:
        p=urlparse(value)
        if not p.scheme or not p.netloc:return ''
        return f"{p.scheme.lower()}://{p.netloc.lower()}"
    except Exception:return ''

def allowed_origins(host: str = '', forwarded_proto: str = 'https') -> set[str]:
    configured=str(os.environ.get('STOKLEDGER_ALLOWED_ORIGINS','')).strip()
    origins={normalize_origin(x) for x in configured.split(',') if normalize_origin(x)}
    if origins:return origins
    if host:
        proto=(str(forwarded_proto or '').split(',')[0].strip().lower() or 'https')
        if proto not in ('http','https'):proto='https'
        origins.add(f"{proto}://{str(host).strip().lower()}")
    return origins

def origin_is_allowed(origin: str, referer: str, host: str, forwarded_proto: str='https') -> bool:
    candidate=normalize_origin(origin)
    if not candidate and referer:candidate=normalize_origin(referer)
    if not candidate:return True
    return candidate in allowed_origins(host,forwarded_proto)

def generate_totp_secret(bytes_len: int=20) -> str:return base64.b32encode(secrets.token_bytes(max(10,int(bytes_len)))).decode().rstrip('=')
def _totp_key(secret: str) -> bytes:
    cleaned=''.join(str(secret or '').upper().split()).replace('-','')
    if not cleaned:return b''
    cleaned += '='*((8-len(cleaned)%8)%8)
    try:return base64.b32decode(cleaned,casefold=True)
    except Exception:return b''
def totp_code(secret: str,timestamp=None,step:int=30,digits:int=6)->str:
    key=_totp_key(secret)
    if not key:raise ValueError('TOTP secret tidak valid.')
    counter=int((time.time() if timestamp is None else timestamp)//step); msg=struct.pack('>Q',counter); digest=hmac.new(key,msg,hashlib.sha1).digest(); offset=digest[-1]&0x0F; value=(struct.unpack('>I',digest[offset:offset+4])[0]&0x7fffffff)%(10**digits); return str(value).zfill(digits)
def verify_totp(secret: str,code: str,timestamp=None,window:int=1)->bool:
    code=''.join(ch for ch in str(code or '') if ch.isdigit())
    if len(code)!=6:return False
    now=time.time() if timestamp is None else float(timestamp)
    for delta in range(-abs(int(window)),abs(int(window))+1):
        try:
            if hmac.compare_digest(totp_code(secret,now+delta*30),code):return True
        except Exception:return False
    return False
def owner_totp_configured()->bool:return bool(_totp_key(os.environ.get('STOKLEDGER_OWNER_TOTP_SECRET','')))
def verify_owner_totp(code: str)->bool:
    secret=str(os.environ.get('STOKLEDGER_OWNER_TOTP_SECRET','')).strip();return bool(secret and verify_totp(secret,code))
