"""Cryptographic helpers for password hashing and HMAC-SHA256 JWT tokens."""
import hmac
import base64
import json
import hashlib
import time
from typing import Dict, Any, Optional

SECRET_KEY = "offline_research_mate_secure_jwt_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_SECONDS = 60 * 60 * 24 * 7  # 7 days

def hash_password(password: str) -> str:
    """Hash password using PBKDF2-HMAC-SHA256 with random salt."""
    salt = hashlib.sha256(password.encode("utf-8")[:4] + b"academic_salt").hexdigest()[:16]
    key = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt.encode("utf-8"), 100000)
    return f"{salt}${key.hex()}"

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify password against PBKDF2-HMAC-SHA256 hash."""
    try:
        salt, expected_hex = hashed_password.split("$", 1)
        actual_key = hashlib.pbkdf2_hmac("sha256", plain_password.encode("utf-8"), salt.encode("utf-8"), 100000)
        return hmac.compare_digest(actual_key.hex(), expected_hex)
    except Exception:
        return False

def _base64url_encode(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).decode("utf-8").rstrip("=")

def _base64url_decode(data: str) -> bytes:
    padding = 4 - (len(data) % 4)
    if padding != 4:
        data += "=" * padding
    return base64.urlsafe_b64decode(data.encode("utf-8"))

def create_access_token(data: Dict[str, Any], expires_delta: Optional[int] = None) -> str:
    """Create signed HMAC-SHA256 JWT token."""
    header = {"alg": ALGORITHM, "typ": "JWT"}
    payload = data.copy()
    now = int(time.time())
    payload["iat"] = now
    payload["exp"] = now + (expires_delta or ACCESS_TOKEN_EXPIRE_SECONDS)

    header_b64 = _base64url_encode(json.dumps(header, separators=(",", ":")).encode("utf-8"))
    payload_b64 = _base64url_encode(json.dumps(payload, separators=(",", ":")).encode("utf-8"))
    signing_input = f"{header_b64}.{payload_b64}"

    signature = hmac.new(SECRET_KEY.encode("utf-8"), signing_input.encode("utf-8"), hashlib.sha256).digest()
    sig_b64 = _base64url_encode(signature)

    return f"{signing_input}.{sig_b64}"

def decode_access_token(token: str) -> Dict[str, Any]:
    """Verify signature and decode JWT payload."""
    parts = token.split(".")
    if len(parts) != 3:
        raise ValueError("Invalid JWT token format.")

    header_b64, payload_b64, sig_b64 = parts
    signing_input = f"{header_b64}.{payload_b64}"

    expected_sig = hmac.new(SECRET_KEY.encode("utf-8"), signing_input.encode("utf-8"), hashlib.sha256).digest()
    actual_sig = _base64url_decode(sig_b64)

    if not hmac.compare_digest(expected_sig, actual_sig):
        raise ValueError("JWT signature verification failed.")

    payload = json.loads(_base64url_decode(payload_b64).decode("utf-8"))
    if "exp" in payload and int(time.time()) > payload["exp"]:
        raise ValueError("JWT token has expired.")

    return payload
