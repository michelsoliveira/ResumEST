import falcon
from marshmallow import Schema, fields, ValidationError
from ....application.services.resume_service import ResumeService

class ContactSchema(Schema):
    email = fields.Email(required=True)
    phone = fields.Str(allow_none=True)
    location = fields.Str(allow_none=True)
    linkedin = fields.URL(allow_none=True)
    github = fields.URL(allow_none=True)

class ContactResource:
    def __init__(self, resume_service: ResumeService):
        self.resume_service = resume_service
        self.schema = ContactSchema()

    def on_get(self, req, resp, resume_id):
        resume = self.resume_service.get_resume(resume_id)
        if not resume:
            raise falcon.HTTPNotFound()
        resp.media = resume.contact.__dict__

    def on_patch(self, req, resp, resume_id):
        try:
            data = self.schema.load(req.media, partial=True)
            resume = self.resume_service.get_resume(resume_id)
            if not resume:
                raise falcon.HTTPNotFound()

            # Update contact fields
            for key, value in data.items():
                setattr(resume.contact, key, value)

            updated_resume = self.resume_service.update_resume(resume_id, {"contact": resume.contact})
            resp.media = updated_resume.contact.__dict__
        except ValidationError as e:
            raise falcon.HTTPBadRequest(description=str(e)) 