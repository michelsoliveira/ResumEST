from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime

@dataclass
class Education:
    id: Optional[str]
    institution: str
    degree: str
    field_of_study: str
    start_date: datetime
    end_date: Optional[datetime]
    description: Optional[str]

@dataclass
class Experience:
    id: Optional[str]
    company: str
    position: str
    start_date: datetime
    end_date: Optional[datetime]
    description: str
    achievements: List[str]

@dataclass
class Skill:
    id: Optional[str]
    name: str
    level: str  # e.g., "Beginner", "Intermediate", "Advanced", "Expert"

@dataclass
class Contact:
    email: str
    phone: Optional[str]
    location: Optional[str]
    linkedin: Optional[str]
    github: Optional[str]

@dataclass
class Resume:
    id: Optional[str]
    user_id: str
    title: str
    contact: Contact
    summary: str
    education: List[Education]
    experience: List[Experience]
    skills: List[Skill]
    created_at: datetime
    updated_at: datetime 