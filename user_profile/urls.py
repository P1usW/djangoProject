from django.urls import path
from . import views

urlpatterns = [
    path('register', views.register, name='register'),
    path('login', views.user_login, name='login'),
    path('logout', views.UserLogout.as_view(), name='logout'),
    path('recover_password_request', views.recover_password_request, name='recover_password_request'),
    path('password_reset_confirm/<uidb64>/<token>', views.RecoverPassword.as_view(), name='password_reset_confirm'),
    #path('password_recer_complite', views.RecoverPasswordConfirm.as_view(), name='password_reset_complete')
]