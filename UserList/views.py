from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from knox.auth import TokenAuthentication
from rest_framework import status
from .models import UserLists
from .serializers import UserListsSerializer
# Create your views here.

class createList(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        # Verificar si el token es válido
        if request.auth:
            # Obtener los datos que se van a guardar en el modelo UserLists

            list_name = request.POST['list_name']
            # list_id = request.POST['list_id']
            #list_content = request.POST['list_content']

            # Crear una instancia del modelo UserLists y guardarla en la base de datos
            user_list = UserLists(list_name=list_name, author=request.user)
            user_list.save()

            return Response({'success': 'Los datos se han guardado correctamente.'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'error': 'El token es inválido.'}, status=status.HTTP_401_UNAUTHORIZED)


class getUserLists(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        # Verificar si el token es válido
        if request.auth:
            # Obtener todas las listas creadas por el usuario autenticado
            user_lists = UserLists.objects.filter(author=request.user)
            
            # Serializar las listas obtenidas para poder enviarlas como respuesta
            serializer = UserListsSerializer(user_lists, many=True)

            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'El token es inválido.'}, status=status.HTTP_401_UNAUTHORIZED)
