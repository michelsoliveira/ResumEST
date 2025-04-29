from abc import ABC, abstractmethod
from typing import List, Optional
from ..models.resume import Resume

class ResumeRepository(ABC):
    @abstractmethod
    def save(self, resume: Resume) -> Resume:
        pass

    @abstractmethod
    def find_by_id(self, resume_id: str) -> Optional[Resume]:
        pass

    @abstractmethod
    def find_by_user_id(self, user_id: str) -> List[Resume]:
        pass

    @abstractmethod
    def delete(self, resume_id: str) -> bool:
        pass 