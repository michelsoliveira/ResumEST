import json
import falcon
from marshmallow import Schema, fields, ValidationError
from ....application.services.resume_service import ResumeService

class ResumeSchema(Schema):
    title = fields.Str(required=True)
    contact = fields.Dict(required=True)
    summary = fields.Str(required=True)

class ResumeResource:
    def __init__(self, resume_service: ResumeService):
        self.resume_service = resume_service
        self.schema = ResumeSchema()

    def on_get(self, req, resp, resume_id=None):
        if resume_id:
            resume = self.resume_service.get_resume(resume_id)
            if not resume:
                raise falcon.HTTPNotFound()
            resp.media = self._serialize_resume(resume)
        else:
            user_id = req.get_param('user_id')
            if not user_id:
                raise falcon.HTTPBadRequest(description="user_id parameter is required")
            resumes = self.resume_service.get_user_resumes(user_id)
            resp.media = [self._serialize_resume(resume) for resume in resumes]

    def on_post(self, req, resp):
        try:
            data = self.schema.load(req.media)
            user_id = req.get_param('user_id')
            if not user_id:
                raise falcon.HTTPBadRequest(description="user_id parameter is required")
            
            resume = self.resume_service.create_resume(
                user_id=user_id,
                title=data['title'],
                contact=data['contact'],
                summary=data['summary']
            )
            resp.status = falcon.HTTP_201
            resp.media = self._serialize_resume(resume)
        except ValidationError as e:
            raise falcon.HTTPBadRequest(description=str(e))

    def on_put(self, req, resp, resume_id):
        try:
            data = self.schema.load(req.media)
            resume = self.resume_service.update_resume(resume_id, data)
            if not resume:
                raise falcon.HTTPNotFound()
            resp.media = self._serialize_resume(resume)
        except ValidationError as e:
            raise falcon.HTTPBadRequest(description=str(e))

    def on_delete(self, req, resp, resume_id):
        success = self.resume_service.delete_resume(resume_id)
        if not success:
            raise falcon.HTTPNotFound()
        resp.status = falcon.HTTP_204

    def _serialize_resume(self, resume):
        return {
            'id': resume.id,
            'user_id': resume.user_id,
            'title': resume.title,
            'contact': resume.contact.__dict__,
            'summary': resume.summary,
            'education': [edu.__dict__ for edu in resume.education],
            'experience': [exp.__dict__ for exp in resume.experience],
            'skills': [skill.__dict__ for skill in resume.skills],
            'created_at': resume.created_at.isoformat(),
            'updated_at': resume.updated_at.isoformat()
        } 