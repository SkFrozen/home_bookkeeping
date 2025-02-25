import bcrypt


def get_password_hash(password: str) -> str:
    b_pwd = password.encode("utf-8")
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(b_pwd, salt).decode("utf-8")


def verify_password(password: str, hashed_password: str) -> bool:
    b_pwd = password.encode("utf-8")
    b_hashed_pwd = hashed_password.encode("utf-8")
    return bcrypt.checkpw(b_pwd, b_hashed_pwd)
