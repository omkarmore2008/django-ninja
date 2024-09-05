from ninja.security import HttpBasicAuth
from ninja.security import HttpBearer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed

class BasicAuth(HttpBearer):
    def authenticate(self, request, token):
        jwt_auth = JWTAuthentication()
        try:
            validated_token = jwt_auth.get_validated_token(token)
            user = jwt_auth.get_user(validated_token)
            return user
        except AuthenticationFailed as e:
            return None 

    # def authenticate(self, request, username, password):
    #     from django.contrib.auth import authenticate
    #     user = authenticate(username=username, password=password)
    #     if user is not None:
    #         return user