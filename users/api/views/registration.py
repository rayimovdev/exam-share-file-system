from django.core import exceptions
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated

from utils import render_data, render_message

from ...models import CustomUser
from ...serializers import LoginSerializer, UserSerializerWithToken


class CustomUserGenericAPIView(GenericAPIView):
    queryset = CustomUser
    serializer_class = UserSerializerWithToken


class SignUpView(CustomUserGenericAPIView):

    def post(self, request):
        try:
            first_name = request.data['first_name']
            role = request.data['role']
            email = request.data['email']
            password = request.data['password']

            custom_user = self.queryset.objects.create_user(
                first_name=first_name, role=role,
                email=email, password=password,
            )

            user_serializer = self.serializer_class(custom_user, many=False)

            return Response(
                render_data(data=user_serializer.data, success='true'),
                status = status.HTTP_201_CREATED
            )
        except Exception as error:
            return Response(
                render_message(message=str(error), success='false'),
                status = status.HTTP_400_BAD_REQUEST
            )


class LoginView(APIView):
    queryset = CustomUser

    def post(self, request):
        try:
            serializer = LoginSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']

            try:
                user = self.queryset.objects.get(email=email)
            except exceptions.ObjectDoesNotExist:
                return Response(
                    render_message(message='User not found', success='false'),
                    status = status.HTTP_404_NOT_FOUND
                )

            if not user.check_password(password):
                return Response(
                    render_message(message='Incorrect password', success='false'),
                    status = status.HTTP_400_BAD_REQUEST
                )
            if not user.is_active:
                return Response(
                    render_message(message='Inactive account', success='false'),
                    status = status.HTTP_400_BAD_REQUEST
                )

            serializer = UserSerializerWithToken(user)

            return Response(
                render_data(data=serializer.data, success='true'),
                status = status.HTTP_200_OK
            )
        except Exception as error:
            return Response(
                render_message(message=str(error), success='false'),
                status = status.HTTP_400_BAD_REQUEST
            )


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data['refresh']
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(
                render_message(message='Logged out successfully', success='true'),
                status = status.HTTP_205_RESET_CONTENT
            )
        except Exception as error:
            return Response(
                render_message(message=str(error), success='false'),
                status = status.HTTP_400_BAD_REQUEST
            )