import falcon
from marshmallow import Schema, fields, ValidationError
from ....application.services.resume_service import ResumeService

class ExperienceSchema(Schema):
    company = fields.Str(required=True)
    position = fields.Str(required=True)
    start_date = fields.DateTime(required=True)
    end_date = fields.DateTime(allow_none=True)
    description = fields.Str(required=True)
    achievements = fields.List(fields.Str(), required=True)

class ExperienceResource:
    def __init__(self, resume_service: ResumeService):
        self.resume_service = resume_service
        self.schema = ExperienceSchema()

    def on_get(self, req, resp, resume_id):
        resume = self.resume_service.get_resume(resume_id)
        if not resume:
            raise falcon.HTTPNotFound()
        resp.media = [exp.__dict__ for exp in resume.experience]

    def on_post(self, req, resp, resume_id):
        try:
            data = self.schema.load(req.media)
            resume = self.resume_service.get_resume(resume_id)
            if not resume:
                raise falcon.HTTPNotFound()

            resume.experience.append(data)
            updated_resume = self.resume_service.update_resume(resume_id, {"experience": resume.experience})
            resp.status = falcon.HTTP_201
            resp.media = updated_resume.experience[-1].__dict__
        except ValidationError as e:
            raise falcon.HTTPBadRequest(description=str(e))

    def on_patch(self, req, resp, resume_id, experience_id):
        try:
            data = self.schema.load(req.media, partial=True)
            resume = self.resume_service.get_resume(resume_id)
            if not resume:
                raise falcon.HTTPNotFound()

            try:
                experience_id = int(experience_id)
                if experience_id >= len(resume.experience):
                    raise falcon.HTTPNotFound()
            except ValueError:
                raise falcon.HTTPBadRequest(description="Invalid experience ID")

            # Update experience fields
            for key, value in data.items():
                setattr(resume.experience[experience_id], key, value)

            updated_resume = self.resume_service.update_resume(resume_id, {"experience": resume.experience})
            resp.media = updated_resume.experience[experience_id].__dict__
        except ValidationError as e:
            raise falcon.HTTPBadRequest(description=str(e))

    def on_delete(self, req, resp, resume_id, experience_id):
        resume = self.resume_service.get_resume(resume_id)
        if not resume:
            raise falcon.HTTPNotFound()

        try:
            experience_id = int(experience_id)
            if experience_id >= len(resume.experience):
                raise falcon.HTTPNotFound()
        except ValueError:
            raise falcon.HTTPBadRequest(description="Invalid experience ID")

        resume.experience.pop(experience_id)
        self.resume_service.update_resume(resume_id, {"experience": resume.experience})
        resp.status = falcon.HTTP_204 