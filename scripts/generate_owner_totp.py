import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from server.hardening import generate_totp_secret
from urllib.parse import quote
secret=generate_totp_secret(); label='StokLedger Online Owner Admin'; issuer='StokLedger Online'
print('STOKLEDGER_OWNER_TOTP_SECRET='+secret)
print(f'otpauth://totp/{quote(label)}?secret={secret}&issuer={quote(issuer)}&digits=6&period=30')
