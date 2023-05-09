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
from .serializers import ChangePasswordSerializer


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


# Change Password

class ChangePasswordView(generics.UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def put(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = request.user

        # Check old password
        if not user.check_password(serializer.validated_data['old_password']):
            return Response({'old_password': ['Wrong password.']},
                            status=status.HTTP_400_BAD_REQUEST)

        # Set new password
        user.set_password(serializer.validated_data['new_password'])
        user.save()

        # Update session authentication hash
        update_session_auth_hash(request, user)

        # Delete old tokens
        AuthToken.objects.filter(user=user).delete()

        # Create new token
        token = AuthToken.objects.create(user).get_token()

        return Response({'token': token.token},
                        status=status.HTTP_200_OK)
