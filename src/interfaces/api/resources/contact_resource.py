import falcon
from marshmallow import Schema, fields, ValidationError
from ....application.services.resume_service import ResumeService

class ContactSchema(Schema):
    email = fields.Email(required=True)
    phone = fields.Str(allow_none=True)
    location = fields.Str(allow_none=True)
    linkedin = fields.URL(allow_none=True)
    github = fields.URL(allow_none=True)

    class Meta:
        unknown = 'EXCLUDE'

class ContactResource:
    def __init__(self, resume_service: ResumeService):
        self.resume_service = resume_service
        self.schema = ContactSchema(partial=True)

    def on_get(self, req, resp, resume_id, contact_id=None):
        resume = self.resume_service.get_resume(resume_id)
        if not resume:
            raise falcon.HTTPNotFound()
        
        if contact_id:
            # Handle single contact retrieval
            if not resume.contact or str(resume.contact.id) != contact_id:
                raise falcon.HTTPNotFound()
            resp.media = resume.contact.__dict__
        else:
            # Handle contact retrieval for resume
            resp.media = resume.contact.__dict__ if resume.contact else {}

    def on_post(self, req, resp, resume_id):
        try:
            data = self.schema.load(req.media)
            resume = self.resume_service.get_resume(resume_id)
            if not resume:
                raise falcon.HTTPNotFound()

            # Create new contact
            resume.contact = data
            updated_resume = self.resume_service.update_resume(resume_id, {"contact": resume.contact})
            resp.media = updated_resume.contact.__dict__
            resp.status = falcon.HTTP_201
        except ValidationError as e:
            raise falcon.HTTPBadRequest(description=str(e))

    def on_put(self, req, resp, resume_id, contact_id):
        try:
            data = self.schema.load(req.media)
            resume = self.resume_service.get_resume(resume_id)
            if not resume or not resume.contact or str(resume.contact.id) != contact_id:
                raise falcon.HTTPNotFound()

            # Update contact
            for key, value in data.items():
                setattr(resume.contact, key, value)

            updated_resume = self.resume_service.update_resume(resume_id, {"contact": resume.contact})
            resp.media = updated_resume.contact.__dict__
        except ValidationError as e:
            raise falcon.HTTPBadRequest(description=str(e))

    def on_delete(self, req, resp, resume_id, contact_id):
        resume = self.resume_service.get_resume(resume_id)
        if not resume or not resume.contact or str(resume.contact.id) != contact_id:
            raise falcon.HTTPNotFound()

        # Remove contact
        resume.contact = None
        self.resume_service.update_resume(resume_id, {"contact": None})
        resp.status = falcon.HTTP_204

    def on_patch(self, req, resp, resume_id):
        try:
            data = self.schema.load(req.media)
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