from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken, Token

from .models import CustomUser


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if not email:
            raise serializers.ValidationError('email is required')
        if not password:
            raise serializers.ValidationError('Password is required')
        return attrs



class UserSerializerWithName(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'email')


class UserSerializerWithToken(serializers.ModelSerializer):
    access = serializers.SerializerMethodField(read_only=True)
    refresh = serializers.SerializerMethodField(read_only=True)
    isAdmin = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = CustomUser
        fields = (
            'id', 'first_name', 'role', 'email',
            'is_superuser', 'access', 'refresh',
            'isAdmin'
        )

    def get_access(self, user: CustomUser):
        token: Token = RefreshToken.for_user(user)
        return str(token.access_token)

    def get_refresh(self, user: CustomUser):
        token: Token = RefreshToken.for_user(user)
        return str(token)

    def get_isAdmin(self, user: CustomUser):
        return user.is_staff