from typing import List, Optional
from pymongo import MongoClient
from datetime import datetime
from ...domain.models.resume import Resume, Education, Experience, Skill, Contact
from ...domain.repositories.resume_repository import ResumeRepository

class MongoDBResumeRepository(ResumeRepository):
    def __init__(self, mongo_client: MongoClient, database_name: str):
        self.db = mongo_client[database_name]
        self.resumes = self.db.resumes
        self.education = self.db.education
        self.experience = self.db.experience
        self.skills = self.db.skills

    def save(self, resume: Resume) -> Resume:
        resume_dict = {
            "user_id": resume.user_id,
            "title": resume.title,
            "contact": resume.contact.__dict__,
            "summary": resume.summary,
            "created_at": resume.created_at,
            "updated_at": resume.updated_at
        }

        if resume.id:
            self.resumes.update_one({"_id": resume.id}, {"$set": resume_dict})
        else:
            result = self.resumes.insert_one(resume_dict)
            resume.id = str(result.inserted_id)

        # Save education records
        for edu in resume.education:
            edu_dict = edu.__dict__
            edu_dict["resume_id"] = resume.id
            if hasattr(edu, "id") and edu.id:
                self.education.update_one({"_id": edu.id}, {"$set": edu_dict})
            else:
                result = self.education.insert_one(edu_dict)
                edu.id = str(result.inserted_id)

        # Save experience records
        for exp in resume.experience:
            exp_dict = exp.__dict__
            exp_dict["resume_id"] = resume.id
            if hasattr(exp, "id") and exp.id:
                self.experience.update_one({"_id": exp.id}, {"$set": exp_dict})
            else:
                result = self.experience.insert_one(exp_dict)
                exp.id = str(result.inserted_id)

        # Save skills records
        for skill in resume.skills:
            skill_dict = skill.__dict__
            skill_dict["resume_id"] = resume.id
            if hasattr(skill, "id") and skill.id:
                self.skills.update_one({"_id": skill.id}, {"$set": skill_dict})
            else:
                result = self.skills.insert_one(skill_dict)
                skill.id = str(result.inserted_id)

        return resume

    def find_by_id(self, resume_id: str) -> Optional[Resume]:
        resume_dict = self.resumes.find_one({"_id": resume_id})
        if not resume_dict:
            return None

        # Get related records
        education_records = list(self.education.find({"resume_id": resume_id}))
        experience_records = list(self.experience.find({"resume_id": resume_id}))
        skill_records = list(self.skills.find({"resume_id": resume_id}))

        return self._dict_to_resume(resume_dict, education_records, experience_records, skill_records)

    def find_by_user_id(self, user_id: str) -> List[Resume]:
        resumes = []
        for resume_dict in self.resumes.find({"user_id": user_id}):
            resume_id = str(resume_dict["_id"])
            education_records = list(self.education.find({"resume_id": resume_id}))
            experience_records = list(self.experience.find({"resume_id": resume_id}))
            skill_records = list(self.skills.find({"resume_id": resume_id}))
            resumes.append(self._dict_to_resume(resume_dict, education_records, experience_records, skill_records))
        return resumes

    def delete(self, resume_id: str) -> bool:
        # Delete related records first
        self.education.delete_many({"resume_id": resume_id})
        self.experience.delete_many({"resume_id": resume_id})
        self.skills.delete_many({"resume_id": resume_id})
        
        # Delete the resume
        result = self.resumes.delete_one({"_id": resume_id})
        return result.deleted_count > 0

    def _dict_to_resume(self, resume_dict: dict, education_records: List[dict], 
                       experience_records: List[dict], skill_records: List[dict]) -> Resume:
        return Resume(
            id=str(resume_dict["_id"]),
            user_id=resume_dict["user_id"],
            title=resume_dict["title"],
            contact=Contact(**resume_dict["contact"]),
            summary=resume_dict["summary"],
            education=[Education(**edu) for edu in education_records],
            experience=[Experience(**exp) for exp in experience_records],
            skills=[Skill(**skill) for skill in skill_records],
            created_at=resume_dict["created_at"],
            updated_at=resume_dict["updated_at"]
        ) 