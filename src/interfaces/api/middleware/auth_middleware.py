import jwt
from falcon import Request, Response, HTTPUnauthorized, HTTPForbidden
from ..domain.models.user import UserRole

class AuthMiddleware:
    def __init__(self, secret_key: str):
        self.secret_key = secret_key

    def process_request(self, req: Request, resp: Response):
        if req.path == "/auth" and req.method == "POST":
            return

        auth_header = req.get_header("Authorization")
        if not auth_header:
            raise HTTPUnauthorized(description="Missing Authorization header")

        try:
            token = auth_header.split(" ")[1]
            payload = jwt.decode(token, self.secret_key, algorithms=["HS256"])
            req.context["user_id"] = payload["sub"]
            req.context["user_email"] = payload["email"]
            req.context["user_role"] = payload["role"]

            # Check if user has permission for the requested method
            if payload["role"] == UserRole.GUEST and req.method not in ["GET", "HEAD", "OPTIONS"]:
                raise HTTPForbidden(description="Guest users can only perform GET requests")
        except jwt.ExpiredSignatureError:
            raise HTTPUnauthorized(description="Token has expired")
        except jwt.InvalidTokenError:
            raise HTTPUnauthorized(description="Invalid token") 