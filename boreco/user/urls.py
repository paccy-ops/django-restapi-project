from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from user import views

app_name = "user"

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name="register"),
    path('email-verify/', views.VerifyEmail.as_view(), name="email-verify"),
    path('login/', views.LoginAPIView.as_view(), name="login"),
    path('logout/', views.LogoutAPIView.as_view(), name="logout"),
    path('users-list', views.ListUsers.as_view(), name="list-users"),
    path('<int:id>', views.UsersActionsAPIView.as_view(), name="user-action"),
    path('me/', views.LoginUserDetails.as_view(), name="me"),
    # path('make-superuser/', views.MakeSuperuser.as_view(), name="make-superuser"),
    path('password-reset-email/', views.RequestPasswordResetEmail.as_view(), name="request-reset-email"),
    path('password-reset/<uidb64>/<token>/', views.PasswordTokenCheckAPIView.as_view(),
         name="password-reset-confirm"),
    path('password-reset-complete/', views.SetNewPasswordAPIView.as_view(),
         name="password-reset-complete"),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
