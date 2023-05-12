from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .serializers import UserSerializer, RegisterSerializer
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth import login
from knox.models import AuthToken
from knox.auth import TokenAuthentication
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.views import LoginView as KnoxLoginView
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
# from .serializers import ChangePasswordSerializer


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


class LoginAPI(KnoxLoginView):

    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):

        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        user_name = user.username
        user_nsfw = user.data_user.nsfw_content
        user_image_profile = user.data_user.image_profile.url

        login(request, user)
        temp_list = super(LoginAPI, self).post(request, format=None)
        temp_list.data["username"] = user_name
        temp_list.data["user_nsfw"] = user_nsfw

        print(user_image_profile)

        temp_list.data["image_profile"] = user_image_profile

        return Response(temp_list.data)


class VerifyTokenView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        return Response({'success': 'El token es válido.'})


class EditProfileView(generics.RetrieveUpdateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def update(self, request, *args, **kwargs):
        user = request.user
        serializer = self.serializer_class(
            user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
