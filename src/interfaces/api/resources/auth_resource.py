import falcon
from marshmallow import Schema, fields, ValidationError
from ....application.services.auth_service import AuthService

class AuthSchema(Schema):
    email = fields.Email(required=True)

class AuthResource:
    def __init__(self, auth_service: AuthService):
        self.auth_service = auth_service
        self.schema = AuthSchema()

    def on_post(self, req, resp):
        try:
            data = self.schema.load(req.media)
            token = self.auth_service.authenticate_user(data["email"])
            resp.media = {"access_token": token, "token_type": "bearer"}
        except (ValidationError, ValueError) as e:
            raise falcon.HTTPBadRequest(description=str(e)) 