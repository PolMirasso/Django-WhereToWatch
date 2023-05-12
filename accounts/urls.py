from .views import RegisterAPI, LoginAPI, VerifyTokenView, EditProfileView
from knox import views as knox_views
from django.urls import path

urlpatterns = [
    path('api/register/', RegisterAPI.as_view(), name='register'),
    path('api/login/', LoginAPI.as_view(), name='login'),
    path('api/logout/', knox_views.LogoutView.as_view(), name='logout'),
    path('api/verify-token/', VerifyTokenView.as_view(), name='verify_token'),
    path('api/logoutAll/', knox_views.LogoutAllView.as_view(), name='logoutall'),
    path('api/edit-profile/', EditProfileView.as_view(), name='edit-profile'),
    # path('api/change_password/', ChangePasswordView.as_view(),
    #      name='change_password'),
]
