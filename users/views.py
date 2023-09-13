from rest_framework.decorators import api_view, permission_classes, authentication_classes
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
import firebase_admin
from firebase_admin import credentials
from firebase_admin import auth
from django.conf import settings
from .custom_authentication import FirebaseAuthentication


User = get_user_model()
firebase_credentials = credentials.Certificate(settings.FIREBASE_CONFIG)
firebase_app = firebase_admin.initialize_app(firebase_credentials)


@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    data = request.data
    email = data.get('email')
    password = data.get('password')

    if User.objects.filter(email=email).exists():
        return Response({"message": "User already exist"}, status=400)

    user = User.objects.create_user(
        email=email,
        password=password,
        is_active=True,
        account_status="Active"
    )
    user.set_password(password)
    user.save()
    auth.create_user(email=email, password=password, uid=str(user.id))
    return Response({"message": "created successfully"}, status=201)


@api_view(["GET"])
@authentication_classes([FirebaseAuthentication])
@permission_classes([IsAuthenticated])
def home(request):
    return Response({"message": f"User authenticated as {request.user.email}"}, status=200)
# Create your views here.
