from django.urls import path,include
from .views import LoginView, RegistrationView,WorkOrderAPIView

urlpatterns = [
    path('register/', RegistrationView.as_view(), name='register'),
    path('signin/', LoginView.as_view(), name='login'),
    # path('submitForm/', submitForm.as_view(), ),
    path('work-order/', WorkOrderAPIView.as_view()), 
    path('work-order/<int:id>/', WorkOrderAPIView.as_view()),
]
