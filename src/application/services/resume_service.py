from typing import List, Optional
from datetime import datetime, UTC
from ..domain.models.resume import Resume
from ..domain.repositories.resume_repository import ResumeRepository

class ResumeService:
    def __init__(self, resume_repository: ResumeRepository):
        self.resume_repository = resume_repository

    def create_resume(self, user_id: str, title: str, contact: dict, summary: str) -> Resume:
        now = datetime.now(UTC)
        resume = Resume(
            id=None,
            user_id=user_id,
            title=title,
            contact=contact,
            summary=summary,
            education=[],
            experience=[],
            skills=[],
            created_at=now,
            updated_at=now
        )
        return self.resume_repository.save(resume)

    def get_resume(self, resume_id: str) -> Optional[Resume]:
        return self.resume_repository.find_by_id(resume_id)

    def get_user_resumes(self, user_id: str) -> List[Resume]:
        return self.resume_repository.find_by_user_id(user_id)

    def update_resume(self, resume_id: str, updates: dict) -> Optional[Resume]:
        resume = self.resume_repository.find_by_id(resume_id)
        if not resume:
            return None

        for key, value in updates.items():
            if hasattr(resume, key):
                setattr(resume, key, value)

        resume.updated_at = datetime.now(UTC)
        return self.resume_repository.save(resume)

    def delete_resume(self, resume_id: str) -> bool:
        return self.resume_repository.delete(resume_id) 