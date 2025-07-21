from werkzeug.security import generate_password_hash, check_password_hash

class AuthService:
    def hash_password(self, plain_password: str) -> str:
        return generate_password_hash(plain_password)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return check_password_hash(hashed_password, plain_password)
