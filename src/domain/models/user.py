from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from enum import Enum

class UserRole(str, Enum):
    OWNER = "owner"
    GUEST = "guest"

@dataclass
class User:
    id: Optional[str]
    email: str
    created_at: datetime
    updated_at: datetime
    password_hash: Optional[str] = ""
    role: UserRole = UserRole.GUEST 