from sqlite3 import IntegrityError

from django.contrib.auth import authenticate

from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.views import APIView

from .permissions import IsInstructor
from .models import Users

from .serializers import UserSerializer, LoginUserSerializer

class UserView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsInstructor]

    def post(self, request: Request):
        try:
            serializer = UserSerializer(data = request.data)
            serializer.is_valid(raise_exception = True)

            isEmailTaken = Users.objects.filter(
                email = serializer.validated_data["email"]
            ).exists()

            if isEmailTaken:
                return Response({"message": "User already exists"}, 422)

            newUser = Users.objects.create(**serializer.validated_data)

            newUser.set_password(serializer.validated_data['password'])
            newUser.save()

            userSerialized = UserSerializer(newUser)

            return Response( userSerialized.data, 201 )

        except IntegrityError as error:
            return Response(str(error), 400)

    def get(self, request: Request):
        serializedUsers = UserSerializer(Users.objects.all(), many = True)
        return Response(serializedUsers.data, 200)

@api_view(['POST'])
def loginView(request: Request):
    serializer = LoginUserSerializer(data = request.data)
    serializer.is_valid(raise_exception = True)

    user = authenticate(
        username = serializer.validated_data["email"],
        password = serializer.validated_data["password"],
    )

    if not user:
        return Response({"message": "Invalid credentials"}, 401)

    token, _ = Token.objects.get_or_create(user = user)

    return Response({"token": token.key})

