import base64
import hashlib

import bcrypt


def _b64_sha256_encode(password: bytes) -> bytes:
    return base64.b64encode(
        hashlib.sha256(password).digest(),
    )


def get_password_hash(password: str) -> str:
    hashed = bcrypt.hashpw(
        password=_b64_sha256_encode(password.encode()),
        salt=bcrypt.gensalt(),
    )
    str_hashed: str = hashed.decode()
    return str_hashed


def verify_password(password: str, hashed_password: str) -> bool:
    is_correct: bool = bcrypt.checkpw(
        password=_b64_sha256_encode(password.encode()),
        hashed_password=hashed_password.encode(),
    )
    return is_correct
