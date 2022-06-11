import jwt
from core.models import User
from core.passwordGenerator import user_generated_password
from core.renderers import UserRender
from core.utils import Util
from django.conf import settings
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.utils.encoding import smart_bytes, smart_str, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics
from rest_framework import permissions
from rest_framework import status
from rest_framework import views
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from user import serializers


class RegisterView(generics.GenericAPIView):
    """Register user"""
    serializer_class = serializers.RegisterSerializer
    permission_classes = (permissions.IsAdminUser,)
    renderer_classes = (UserRender,)

    def post(self, request):
        data = request.data
        data['password'] = user_generated_password
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data = serializer.data
        user = User.objects.get(email=user_data['email'])
        token = RefreshToken.for_user(user).access_token
        relative_link = reverse("user:email-verify")
        domain = get_current_site(request).domain
        absurl = f'http://{domain}{relative_link}?token={str(token)}'
        subject = "Verify account"
        email_body = f"Admin registered your account with\n" \
                     f" email: {user.email} and temporary password: {data['password']} \n" \
                     f"If this is not your email please ignore the message.\n" \
                     f"Otherwise use the link below to verify your email.\n" \
                     f"{absurl}\n"
        email_data_to_send = {'subject': subject, "body": email_body, "to_email": user.email}
        Util.send_email(email_data_to_send)
        res = {
            # "user": user_data,
            "message": f"message sent to {user.email}"
        }
        return Response(res, status=status.HTTP_201_CREATED)


class VerifyEmail(views.APIView):
    """email verification view"""
    serializer_class = serializers.EmailVerificationSerializer
    renderer_classes = (UserRender,)

    token_param = openapi.Parameter(
        'token', in_=openapi.IN_QUERY, type=openapi.TYPE_STRING, description="Description"
    )

    @swagger_auto_schema(manual_parameters=[token_param])
    def get(self, request):
        token = request.GET.get('token')
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            user = User.objects.get(id=payload['user_id'])
            if not user.is_verified:
                user.is_verified = True
                user.save()
                subject = "Thank you"
                email_body = "Thank you for verifying your account."
                email_data_to_send = {'subject': subject, 'body': email_body, 'to_email': user.email}
                Util.send_email(email_data_to_send)
            return Response({'email': 'successfully activated'}, status=status.HTTP_200_OK)

        except jwt.ExpiredSignatureError:
            return Response({'error': 'activation link expired'}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError:
            return Response({'error': 'invalid token'}, status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(generics.GenericAPIView):
    """Login user with email and password"""

    serializer_class = serializers.LoginSerializer
    renderer_classes = (UserRender,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ListUsers(generics.ListAPIView):
    """Get list of users"""
    serializer_class = serializers.UsersListSerializer
    permission_classes = (permissions.IsAdminUser,)
    renderer_classes = (UserRender,)

    def get_queryset(self):
        return User.objects.filter(is_verified=True)


class LoginUserDetails(generics.RetrieveAPIView):
    serializer_class = serializers.UsersListSerializer
    permission_classes = (permissions.IsAuthenticated,)
    renderer_classes = (UserRender,)

    def get_object(self):
        return self.request.user


class RequestPasswordResetEmail(generics.GenericAPIView):
    serializer_class = serializers.ResetPasswordRequestSerializer
    renderer_classes = (UserRender,)

    def post(self, request):
        self.serializer_class(data=request.data)
        email = request.data['email']
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            relativelink = reverse('user:password-reset-confirm',
                                   kwargs={'uidb64': uidb64, 'token': token})
            domain = get_current_site(request).domain
            absurl = f'http://{domain}{relativelink}'
            subject = "Reset your password"
            email_body = f"User link below to reset your password\n" \
                         f"{absurl}"
            email_data_send = {'subject': subject, 'body': email_body, 'to_email': user.email}
            Util.send_email(email_data_send)
        return Response({'success': 'We have sent you a link to reset your password'})


class PasswordTokenCheckAPIView(generics.GenericAPIView):
    serializer_class = serializers.ResetPasswordRequestSerializer
    renderer_classes = (UserRender,)

    @staticmethod
    def get(request, uidb64, token):
        try:
            user_id = smart_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=user_id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                return Response({'error': 'Token is not valid, please request a new one'},
                                status=status.HTTP_401_UNAUTHORIZED)
            return Response({
                'success': True,
                'message': 'Credentials Valid',
                'uidb64': uidb64,
                'token': token
            }, status=status.HTTP_200_OK)
        except DjangoUnicodeDecodeError:
            return Response({'error': 'Token is not valid, please request a new one'},
                            status=status.HTTP_401_UNAUTHORIZED)


class SetNewPasswordAPIView(generics.GenericAPIView):
    serializer_class = serializers.SetNewPasswordSerializer
    renderer_classes = (UserRender,)

    def patch(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        # subject = " expense notification"
        # email_body = f"admin has permission to staff."
        # email_data_to_send = {'subject': subject, 'body': email_body, 'to_email': user.email}
        # Util.send_email(email_data_to_send)
        return Response({'success': True, 'message': 'password reset success'}, status=status.HTTP_200_OK)


class UsersActionsAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = serializers.UsersListSerializer
    queryset = User.objects.all()
    permission_classes = (permissions.IsAdminUser,)
    lookup_field = "id"

    def get_queryset(self):
        return self.queryset.filter(is_verified=True)


class LogoutAPIView(generics.GenericAPIView):
    serializer_class = serializers.LogoutSerializer
    permission_class = (permissions.IsAuthenticated,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(status=status.HTTP_204_NO_CONTENT)
