import jwt
from core.models import User
from django.conf import settings
from rest_framework import authentication, exceptions


class JWTAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        auth_data = authentication.get_authorization_header(request)
        if not auth_data:
            return None
        prefix, token = auth_data.decode('utf-8').split(' ')
        try:
            payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=['HS256'])
            user = User.objects.get(email=payload['email'])
            return [user, token]
        except jwt.DecodeError:
            raise exceptions.AuthenticationFailed('Invalid Token')
        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed('Token expired')

        return super(JWTAuthentication, self).authenticate(request)
