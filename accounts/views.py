from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .serializers import UserSerializer, RegisterSerializer, ChangePasswordSerializer
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth import login
from knox.models import AuthToken
from knox.auth import TokenAuthentication
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.views import LoginView as KnoxLoginView
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .models import data_user
from django.contrib.auth.models import User
import os
import random
import string
from django.conf import settings

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
        description = user.data_user.description

        login(request, user)
        temp_list = super(LoginAPI, self).post(request, format=None)
        temp_list.data["username"] = user_name
        temp_list.data["user_nsfw"] = user_nsfw
        temp_list.data["image_profile"] = user_image_profile
        temp_list.data["description"] = description

        return Response(temp_list.data)




class VerifyTokenView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        return Response({'success': 'El token es válido.'})


class changeDescription(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        if request.auth:

            new_description = request.POST['new_description']

            try:
                if new_description:
                    user_list = data_user.objects.get(user=request.user)
                    user_list.description = new_description
                    user_list.save()
                    return Response({'success': 'Descripción actualizada correctamente'})
                else:
                    return Response({'error': 'No se proporcionó una nueva descripción'}, status=400)
                
            except data_user.DoesNotExist:
                return Response({'error': 'La lista no existe.'})

        
        else:
            return Response({'error': 'El token es inválido.'}, status=status.HTTP_401_UNAUTHORIZED)
        

class changeNSFW(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        if request.auth:

            new_nsfw_content = request.POST['new_nsfw_content']

            try:
                if new_nsfw_content:
                    user_list = data_user.objects.get(user=request.user)

                    if new_nsfw_content == 1 or new_nsfw_content == 0:
                        user_list.nsfw_content = new_nsfw_content
                        user_list.save()
                        return Response({'success': 'Descripción actualizada correctamente'})
                    else:
                        return Response({'error': 'Valor no valido'}, status=400)
               
                else:
                    return Response({'error': 'No se proporcionó una nueva descripción'}, status=400)
                
            except data_user.DoesNotExist:
                return Response({'error': 'La lista no existe.'})

        
        else:
            return Response({'error': 'El token es inválido.'}, status=status.HTTP_401_UNAUTHORIZED)
        
class changeUserImage(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        if request.auth:
            new_image_profile = request.FILES.get('new_image_profile')
            if new_image_profile:
                user_list = data_user.objects.get(user=request.user)
                ext = os.path.splitext(new_image_profile.name)[1]
                id_str = str(request.user.id)
                new_name = f"{id_str.join(random.choices(string.ascii_letters, k=8))}{ext}"
                user_list.image_profile.save(new_name, new_image_profile)
                return Response({'success': 'Imagen de perfil actualizada correctamente'})
            else:
                return Response({'error': 'No se proporcionó una nueva imagen de perfil'}, status=400)
        else:
            return Response({'error': 'El token es inválido.'}, status=status.HTTP_401_UNAUTHORIZED)
        
        
class changeDescription(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        if request.auth:

            new_description = request.POST['new_description']

            try:
                if new_description:
                    user_list = data_user.objects.get(user=request.user)
                    user_list.list_name = new_description
                    user_list.save()
                    # Actualizar la descripción del objeto data_user
                    user_list.description = new_description
                    user_list.save()
                    return Response({'success': 'Descripción actualizada correctamente'})
                else:
                    return Response({'error': 'No se proporcionó una nueva descripción'}, status=400)
                
            except data_user.DoesNotExist:
                return Response({'error': 'La lista no existe.'})

        
        else:
            return Response({'error': 'El token es inválido.'}, status=status.HTTP_401_UNAUTHORIZED)
        


class changePassword(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        if request.auth:

            serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
            serializer.is_valid(raise_exception=True)

            user = request.user
            old_password = serializer.validated_data['old_password']
            new_password = serializer.validated_data['new_password']
            confirm_password = serializer.validated_data['confirm_password']

            if not user.check_password(old_password):
                return Response({"error": "La contraseña anterior es incorrecta."}, status=status.HTTP_400_BAD_REQUEST)

            if new_password != confirm_password:
                return Response({"error": "La nueva contraseña y la confirmación no coinciden."}, status=status.HTTP_400_BAD_REQUEST)

            user.set_password(new_password)
            user.save()
            update_session_auth_hash(request, user)

            return Response({"success": "Contraseña actualizada correctamente."}, status=status.HTTP_200_OK)
                    
        else:
            return Response({'error': 'El token es inválido.'}, status=status.HTTP_401_UNAUTHORIZED)
        