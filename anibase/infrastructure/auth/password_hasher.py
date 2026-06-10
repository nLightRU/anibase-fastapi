from argon2 import PasswordHasher as Ph
from argon2.exceptions import VerifyMismatchError

class PasswordHasher:
    def __init__(self):
        self.hasher = Ph()

    def get_password_hash(self, password: str) -> str:
        return self.hasher.hash(password)

    def verify_password(self, password: str, hashed_password: str) -> bool:
        try:
            return self.hasher.verify(hashed_password, password)
        except VerifyMismatchError:
            return False
