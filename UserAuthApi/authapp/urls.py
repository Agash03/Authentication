from django.contrib import admin
from django.urls import path
from authapp.views import *
urlpatterns = [
    path('registration/',UserRegistrationView.as_view(), name = 'registration' ),
    path('login/',UserLoginView.as_view(),name= 'login'),
    path('profile/',UserProfileView.as_view(),name='profile'),
    path('changepass/',UserChangepassword.as_view(),name='change_password'),
    path('sendresetpass/',SendPasswordResetEmailView.as_view(),name='send_reset_pass'),
    path('resetpass/<uid>/<token>/',UserPasswordResetView.as_view(),name='reset_pass'),
]                                    
                