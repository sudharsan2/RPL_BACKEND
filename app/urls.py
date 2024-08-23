from django.urls import path,include
from .views import LoginView, RegistrationView

urlpatterns = [
    path('register/', RegistrationView.as_view(), name='register'),
    path('signin/', LoginView.as_view(), name='login'),
]
