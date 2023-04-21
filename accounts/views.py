from rest_framework import generics, permissions
from rest_framework.response import Response
from knox.models import AuthToken
from .serializers import UserSerializer, RegisterSerializer
from django.contrib.auth import login
from rest_framework import permissions
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.views import LoginView as KnoxLoginView


# Register API
class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
        "user": UserSerializer(user, context=self.get_serializer_context()).data,
        "token": AuthToken.objects.create(user)[1]
        })
    
# class LoginAPI(KnoxLoginView):
#     permission_classes = (permissions.AllowAny,)

#     def post(self, request, format=None):
#         serializer = AuthTokenSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         user = serializer.validated_data['user']
#         login(request, user)
#         return super(LoginAPI, self).post(request, format=None)
    


class LoginAPI(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)
  
    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        user_name=user.username
        user_email=user.email
        user_age = getattr(user, 'age', None) 
        user_image_profile = getattr(user, 'image_profile', 'https://wheretowatch-vps.herokuapp.com/static/defaultImageProfile.png')  


        login(request, user)
        temp_list=super(LoginAPI, self).post(request, format=None)
        temp_list.data["username"]=user_name
        temp_list.data["email"]=user_email
        temp_list.data["age"]=user_age
        temp_list.data["image_profile"]=user_image_profile

        return Response({"user":temp_list.data})