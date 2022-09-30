from django.urls import path
from . import views

urlpatterns = [
    path('<int:pk>/', views.Profile.as_view(), name='profile'),
    path('edit', views.RecoverUserProfile.as_view(), name='edit'),
    path('password', views.RecoverUserPassword.as_view(), name='edit_password'),
    path('register', views.Register.as_view(), name='register'),
    path('login', views.UserLogin.as_view(), name='login'),
    path('logout', views.UserLogout.as_view(), name='logout'),
    path('password_reset', views.RecoverPasswordRequest.as_view(), name='password_reset'),
    path('password_reset_confirm/<uidb64>/<token>', views.RecoverPassword.as_view(), name='password_reset_confirm'),
]