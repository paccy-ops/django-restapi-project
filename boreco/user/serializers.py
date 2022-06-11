from xml.dom import ValidationErr

from core.models import User
from core.utils import Util
from django.contrib import auth
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.tokens import TokenError


class RegisterSerializer(serializers.ModelSerializer):
    # redirect_url = serializers.CharField(max_length=500, required=False)
    password = serializers.CharField(min_length=6,
                                     max_length=68,
                                     trim_whitespace=False)

    class Meta:
        model = User
        fields = ['email', 'password']

    def validate(self, attrs):
        # attrs.pop('redirect_url')
        email = attrs.get('email', '')
        if not email:
            raise serializers.ValidationError("a user should have an email")

        return attrs

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class EmailVerificationSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=555)

    class Meta:
        model = User
        fields = ['token']


class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255, min_length=5)
    password = serializers.CharField(min_length=6, max_length=68, write_only=True, trim_whitespace=False)
    tokens = serializers.SerializerMethodField()
    active = serializers.BooleanField(read_only=True)
    verified = serializers.BooleanField(read_only=True)
    staff = serializers.BooleanField(read_only=True)
    superuser = serializers.BooleanField(read_only=True)

    class Meta:
        model = User
        fields = ['email', 'password', 'active', 'verified', 'staff', 'superuser', 'tokens']

    def get_active(self):
        return self.instance.is_active

    def get_staff(self):
        return self.instance.is_staff

    def get_verified(self):
        return self.instance.is_verified

    def get_superuser(self):
        return self.instance.is_superuser

    def get_tokens(self, obj):
        user = User.objects.get(email=obj['email'])
        return {
            "access": user.tokens()['access'],
            "refresh": user.tokens()['refresh']
        }

    def validate(self, attrs):
        email = attrs.get('email', '')
        password = attrs.get('password', ' ')
        user = auth.authenticate(email=email, password=password)
        if not user:
            raise AuthenticationFailed('Invalid credentials,try again')
        elif not user.is_active:
            raise AuthenticationFailed('Account disabled,contact admin')
        elif not user.is_verified:
            raise AuthenticationFailed("Email is not  verified")
        attrs['email'] = user.email
        attrs['active'] = user.is_active
        attrs['verified'] = user.is_verified
        attrs['staff'] = user.is_staff
        attrs['superuser'] = user.is_superuser
        attrs['tokens'] = user.tokens
        return attrs


class UsersListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'full_name', 'is_active', 'is_verified', 'is_staff', 'is_superuser']


class ResetPasswordRequestSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=4)

    # redirect_url = serializers.CharField(max_length=500, required=False)

    class Meta:
        model = User
        fields = ['email']


class SetNewPasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=68, min_length=6, write_only=True)
    token = serializers.CharField(min_length=1, write_only=True)
    uidb64 = serializers.CharField(min_length=1, write_only=True)

    class Meta:
        model = User
        fields = ['password', 'token', 'uidb64']

    def validate(self, attrs):
        try:
            password = attrs.get('password')
            token = attrs.get('token')
            uidb64 = attrs.get('uidb64')
            user_id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=user_id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                raise AuthenticationFailed('The reset link is invalid', 401)
            user.set_password(password)
            user.save()
            return user
        except Exception:
            raise AuthenticationFailed('The reset link is invalid', 401)


class MakeSuperUserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(min_length=1, write_only=True)

    class Meta:
        model = User
        fields = ['email']

    def validate(self, attrs):
        email = attrs.get('email')
        if not User.objects.filter(email=email).exists():
            raise AuthenticationFailed('Invalid credentials')
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            if user.is_superuser:
                raise AuthenticationFailed('user is already a superuser')
            user.is_superuser = True
            user.is_staff = True
            user.save()
            subject = " boreco notification"
            email_body = "Admin has pointed your account to staff."
            email_data_to_send = {'subject': subject, 'body': email_body, 'to_email': user.email}
            Util.send_email(email_data_to_send)
            return user


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    default_error_message = {
        'bad_token': ('Token is expired or invalid',)
    }

    def validate(self, attrs):
        self.token = attrs['refresh']
        return attrs

    def save(self, **kwargs):
        try:
            token = RefreshToken(self.token)
            token.blacklist()

        except TokenError:
            raise ValidationErr('bad_token')
