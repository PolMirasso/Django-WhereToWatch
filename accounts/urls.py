from .views import RegisterAPI, LoginAPI, VerifyTokenView
from knox import views as knox_views
from django.urls import path
from . import views

urlpatterns = [
    path('api/register/', RegisterAPI.as_view(), name='register'),
    path('api/login/', LoginAPI.as_view(), name='login'),
    path('api/logout/', knox_views.LogoutView.as_view(), name='logout'),
    path('api/verify-token/', VerifyTokenView.as_view(), name='verify_token'),
    path('api/logoutAll/', knox_views.LogoutAllView.as_view(), name='logoutall'),
    path('api/changeDescription/', views.changeDescription.as_view(), name='changeDescription'),
    path('api/changePassword/', views.changePassword.as_view(), name='changePassword'),
    path('api/changeNSFW/', views.changeNSFW.as_view(), name='changeNSFW'),
    path('api/changeUserImage/', views.changeUserImage.as_view(), name='changeUserImage'),

]
