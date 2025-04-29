import falcon
from marshmallow import Schema, fields, ValidationError
from ....application.services.resume_service import ResumeService

class EducationSchema(Schema):
    institution = fields.Str(required=True)
    degree = fields.Str(required=True)
    field_of_study = fields.Str(required=True)
    start_date = fields.DateTime(required=True)
    end_date = fields.DateTime(allow_none=True)
    description = fields.Str(allow_none=True)

class EducationResource:
    def __init__(self, resume_service: ResumeService):
        self.resume_service = resume_service
        self.schema = EducationSchema()

    def on_get(self, req, resp, resume_id):
        resume = self.resume_service.get_resume(resume_id)
        if not resume:
            raise falcon.HTTPNotFound()
        resp.media = [edu.__dict__ for edu in resume.education]

    def on_post(self, req, resp, resume_id):
        try:
            data = self.schema.load(req.media)
            resume = self.resume_service.get_resume(resume_id)
            if not resume:
                raise falcon.HTTPNotFound()

            resume.education.append(data)
            updated_resume = self.resume_service.update_resume(resume_id, {"education": resume.education})
            resp.status = falcon.HTTP_201
            resp.media = updated_resume.education[-1].__dict__
        except ValidationError as e:
            raise falcon.HTTPBadRequest(description=str(e))

    def on_patch(self, req, resp, resume_id, education_id):
        try:
            data = self.schema.load(req.media, partial=True)
            resume = self.resume_service.get_resume(resume_id)
            if not resume:
                raise falcon.HTTPNotFound()

            try:
                education_id = int(education_id)
                if education_id >= len(resume.education):
                    raise falcon.HTTPNotFound()
            except ValueError:
                raise falcon.HTTPBadRequest(description="Invalid education ID")

            # Update education fields
            for key, value in data.items():
                setattr(resume.education[education_id], key, value)

            updated_resume = self.resume_service.update_resume(resume_id, {"education": resume.education})
            resp.media = updated_resume.education[education_id].__dict__
        except ValidationError as e:
            raise falcon.HTTPBadRequest(description=str(e))

    def on_delete(self, req, resp, resume_id, education_id):
        resume = self.resume_service.get_resume(resume_id)
        if not resume:
            raise falcon.HTTPNotFound()

        try:
            education_id = int(education_id)
            if education_id >= len(resume.education):
                raise falcon.HTTPNotFound()
        except ValueError:
            raise falcon.HTTPBadRequest(description="Invalid education ID")

        resume.education.pop(education_id)
        self.resume_service.update_resume(resume_id, {"education": resume.education})
        resp.status = falcon.HTTP_204 