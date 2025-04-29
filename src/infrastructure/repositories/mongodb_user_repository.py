from typing import Optional
from pymongo import MongoClient
from ...domain.models.user import User, UserRole
from ...domain.repositories.user_repository import UserRepository

class MongoDBUserRepository(UserRepository):
    def __init__(self, mongo_client: MongoClient, database_name: str):
        self.db = mongo_client[database_name]
        self.collection = self.db.users

    def save(self, user: User) -> User:
        user_dict = {
            "email": user.email,
            "password_hash": user.password_hash,
            "role": user.role,
            "created_at": user.created_at,
            "updated_at": user.updated_at
        }

        if user.id:
            self.collection.update_one({"_id": user.id}, {"$set": user_dict})
        else:
            result = self.collection.insert_one(user_dict)
            user.id = str(result.inserted_id)

        return user

    def find_by_email(self, email: str) -> Optional[User]:
        user_dict = self.collection.find_one({"email": email})
        if user_dict:
            return self._dict_to_user(user_dict)
        return None

    def find_by_id(self, user_id: str) -> Optional[User]:
        user_dict = self.collection.find_one({"_id": user_id})
        if user_dict:
            return self._dict_to_user(user_dict)
        return None

    def _dict_to_user(self, user_dict: dict) -> User:
        return User(
            id=str(user_dict["_id"]),
            email=user_dict["email"],
            password_hash=user_dict["password_hash"],
            role=UserRole(user_dict["role"]),
            created_at=user_dict["created_at"],
            updated_at=user_dict["updated_at"]
        ) 