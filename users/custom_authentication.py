from rest_framework import authentication
from rest_framework.exceptions import AuthenticationFailed
import uuid
from firebase_admin import auth
from django.contrib.auth import get_user_model


User = get_user_model()


class FirebaseAuthentication(authentication.BaseAuthentication):

    def authenticate(self, request):
        firebase_id_token = request.META.get('HTTP_AUTHORIZATION')
        print(firebase_id_token)
        try:
            decoded_token = auth.verify_id_token(firebase_id_token)
            print(decoded_token)
            uid = decoded_token['uid']
        except auth.ExpiredIdTokenError:
            raise AuthenticationFailed('Auth token Expired')
        except auth.InvalidIdTokenError:
            raise AuthenticationFailed('Invalid Auth token')

        try:
            user, created = User.objects.get_or_create(email=decoded_token['email'])
            print(user)
            return user, None
        except Exception as e:
            print(e)
            return None
