from ninja.security import HttpBearer
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.authentication import JWTAuthentication


class BasicAuth(HttpBearer):
    def authenticate(self, request, token):
        jwt_auth = JWTAuthentication()
        try:
            validated_token = jwt_auth.get_validated_token(token)
            return jwt_auth.get_user(validated_token)
        except AuthenticationFailed:
            return None
