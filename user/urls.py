from django.urls import path
from .views import RegisterView, VerifyEmail, LoginView, RequestPasswordResetEmail, ResetPasswordEmailVerification,\
    SetNewPasswordAPIView, LogoutView


urlpatterns = [
    path('register/', RegisterView.as_view(), name="register"),
    path('login/', LoginView.as_view(), name="login"),
    path('email-verify/', VerifyEmail.as_view(), name="email-verify"),
    path('request-reset-email/', RequestPasswordResetEmail.as_view(),
         name="request-reset-email"),
    path('password-reset/<uidb64>/<token>/',
         ResetPasswordEmailVerification.as_view(), name='password-reset-confirm'),
    path('password-reset-complete', SetNewPasswordAPIView.as_view(),
         name='password-reset-complete'),
    path('logout/', LogoutView.as_view(), name="logout"),
]
