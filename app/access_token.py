import bcrypt
import jwt
from config import AppConfig
from datetime import datetime, timezone

BCRYPT_MAX_PASSWORD_BYTES = 72

def hash_password(password: str) -> str:
  return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("ascii")

def verify_password(password: str, password_hash: str) -> bool:
    raw = password.encode("utf-8")
    if len(raw) > BCRYPT_MAX_PASSWORD_BYTES:
        return False
    try:
        return bcrypt.checkpw(raw, password_hash.encode("ascii"))
    except ValueError:  # stored value is not a valid bcrypt hash
        return False

def create_user_access_token(user_id: str, user_email: str, config: AppConfig):
  expires_in = config.jwt_expire_days * 24 * 60 * 60
  issued_at = int(datetime.now(timezone.utc).timestamp())
  user_payload = {
    "user_id": user_id,
    "user_email": user_email,
    "iat": issued_at,
    "exp": issued_at + expires_in,
  }

  token = jwt.encode(user_payload, config.jwt_secret, algorithm=config.jwt_algorithm)
  return token, expires_in
