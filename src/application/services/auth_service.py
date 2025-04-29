from datetime import datetime, timedelta, UTC
import jwt
from domain.models.user import User, UserRole
from domain.repositories.user_repository import UserRepository

class AuthService:
    def __init__(self, user_repository: UserRepository, secret_key: str):
        self.user_repository = user_repository
        self.secret_key = secret_key

    def create_user(self, email: str, role: UserRole = UserRole.GUEST) -> User:
        if self.user_repository.find_by_email(email):
            raise ValueError("Email already registered")

        now = datetime.now(UTC)
        user = User(
            id=None,
            email=email,
            role=role,
            created_at=now,
            updated_at=now
        )
        return self.user_repository.save(user)

    def authenticate_user(self, email: str) -> str:
        user = self.user_repository.find_by_email(email)
        if not user:
            # Create user if not exists
            user = self.create_user(email)

        return self._create_access_token(user)

    def _create_access_token(self, user: User) -> str:
        expires_delta = timedelta(days=1)
        expire = datetime.now(UTC) + expires_delta

        to_encode = {
            "sub": user.id,
            "email": user.email,
            "role": user.role,
            "exp": expire
        }
        return jwt.encode(to_encode, self.secret_key, algorithm="HS256") 