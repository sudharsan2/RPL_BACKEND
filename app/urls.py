from django.urls import path,include
from .views import LoginView, RegistrationView,CreateWorkOrderAPIView,WorkOrderDetailAPIView,workOrderHeadersList

urlpatterns = [
    path('register/', RegistrationView.as_view(), name='register'),
    path('signin/', LoginView.as_view(), name='login'),
    path('formsubmit/', CreateWorkOrderAPIView.as_view(), name='WorkOrderCreateView'),
    path('formsubmit/<int:id>', WorkOrderDetailAPIView.as_view(), name='WorkOrderCreateView'),
    path('formslist', workOrderHeadersList.as_view(), name='workOrderHeadersList'),
    

    # path('submitForm/', submitForm.as_view(), ),
    # path('work-order/', WorkOrderAPIView.as_view()), 
    # path('work-order/<int:id>/', WorkOrderAPIView.as_view()),
]
