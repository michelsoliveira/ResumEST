import falcon
from marshmallow import Schema, fields, ValidationError
from ....application.services.resume_service import ResumeService

class SkillSchema(Schema):
    name = fields.Str(required=True)
    level = fields.Str(required=True, validate=lambda x: x in ["Beginner", "Intermediate", "Advanced", "Expert"])

class SkillResource:
    def __init__(self, resume_service: ResumeService):
        self.resume_service = resume_service
        self.schema = SkillSchema()

    def on_get(self, req, resp, resume_id):
        resume = self.resume_service.get_resume(resume_id)
        if not resume:
            raise falcon.HTTPNotFound()
        resp.media = [skill.__dict__ for skill in resume.skills]

    def on_post(self, req, resp, resume_id):
        try:
            data = self.schema.load(req.media)
            resume = self.resume_service.get_resume(resume_id)
            if not resume:
                raise falcon.HTTPNotFound()

            resume.skills.append(data)
            updated_resume = self.resume_service.update_resume(resume_id, {"skills": resume.skills})
            resp.status = falcon.HTTP_201
            resp.media = updated_resume.skills[-1].__dict__
        except ValidationError as e:
            raise falcon.HTTPBadRequest(description=str(e))

    def on_patch(self, req, resp, resume_id, skill_id):
        try:
            data = self.schema.load(req.media, partial=True)
            resume = self.resume_service.get_resume(resume_id)
            if not resume:
                raise falcon.HTTPNotFound()

            try:
                skill_id = int(skill_id)
                if skill_id >= len(resume.skills):
                    raise falcon.HTTPNotFound()
            except ValueError:
                raise falcon.HTTPBadRequest(description="Invalid skill ID")

            # Update skill fields
            for key, value in data.items():
                setattr(resume.skills[skill_id], key, value)

            updated_resume = self.resume_service.update_resume(resume_id, {"skills": resume.skills})
            resp.media = updated_resume.skills[skill_id].__dict__
        except ValidationError as e:
            raise falcon.HTTPBadRequest(description=str(e))

    def on_delete(self, req, resp, resume_id, skill_id):
        resume = self.resume_service.get_resume(resume_id)
        if not resume:
            raise falcon.HTTPNotFound()

        try:
            skill_id = int(skill_id)
            if skill_id >= len(resume.skills):
                raise falcon.HTTPNotFound()
        except ValueError:
            raise falcon.HTTPBadRequest(description="Invalid skill ID")

        resume.skills.pop(skill_id)
        self.resume_service.update_resume(resume_id, {"skills": resume.skills})
        resp.status = falcon.HTTP_204 