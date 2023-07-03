from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . import api

urlpatterns = [
    path('me/', api.me, name='me'),
    path('get_graduates/', api.get_graduates, name='get_graduates'),
    path('get_users/', api.get_users, name='get_users'),
    path('user/<uuid:pk>/', api.get_user, name='get_user'),
    path('signup/', api.signup, name='signup'),
    path('delete/<uuid:pk>/', api.delete_user, name='delete_user'),
    path('update/<uuid:pk>/', api.update_user, name='update_user'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('graduates_per_major/', api.graduates_per_major, name='graduates_per_major'),
    path('percentage_of_grad_workers/', api.percentage_of_grad_workers, name='percentage_of_grad_workers'),

    
    ]
