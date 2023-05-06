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


class addToListContent(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):

         # Verificar si el token es válido
         if request.auth:

            # Obtener los datos que se van a añadir a la lista
            obj_id = request.POST['obj_id']
            obj_type = request.POST['obj_type']
            list_id = request.POST['list_id']

            # Obtener la instancia del modelo UserLists correspondiente a list_id
            try:
                user_list = UserLists.objects.get(author=request.user, list_id=list_id)
            except UserLists.DoesNotExist:
                return Response({'error': 'La lista no existe.'}, status=status.HTTP_404_NOT_FOUND)

            # Verificar que no esta ya en la lista
            if object_in_list(obj_id, obj_type, user_list.list_content):
               return Response({'error': 'El objeto ya está en la lista.'}, status=status.HTTP_400_BAD_REQUEST)

            # Verificar que se recibieron los datos correctos
            if not obj_id or not obj_type:
                return Response({'error': 'Los datos son incorrectos o están incompletos.'}, status=status.HTTP_400_BAD_REQUEST)

            # Añadir el objeto a la lista
            user_list.add_to_list_content(obj_id, obj_type)

            return Response({'success': 'Los datos se han guardado correctamente.'}, status=status.HTTP_201_CREATED)

         else:
             return Response({'error': 'El token es inválido.'}, status=status.HTTP_401_UNAUTHORIZED)


def object_in_list(obj_id, obj_type, list_content):
    for item in list_content:
        if item['id'] == obj_id and item['type'] == obj_type:
            return True
    return False



class removeFromListContent(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):

         # Verificar si el token es válido
         if request.auth:

            # Obtener los valores necesarios para eliminar el objeto de la lista
            list_id = request.POST.get('list_id')
            obj_id = request.POST.get('obj_id')
            obj_type = request.POST.get('obj_type')

            try:
                # Buscar la lista correspondiente al id y autor proporcionados
                user_list = UserLists.objects.get(list_id=list_id, author=request.user)

                # Buscar el objeto en la lista
                object_in_list = next((item for item in user_list.list_content if item["id"] == obj_id and item["type"] == obj_type), None)
                if object_in_list:
                    # Si el objeto se encuentra en la lista, eliminarlo
                    user_list.list_content.remove(object_in_list)
                    user_list.save()

                    return Response({'success': 'El objeto se ha eliminado de la lista correctamente.'}, status=status.HTTP_200_OK)
                else:
                    # Si el objeto no se encuentra en la lista, devolver un error
                    return Response({'error': 'El objeto no se encuentra en la lista.'}, status=status.HTTP_404_NOT_FOUND)

            except UserLists.DoesNotExist:
                # Si la lista no se encuentra, devolver un error
                return Response({'error': 'La lista no existe.'}, status=status.HTTP_404_NOT_FOUND)

         else:
             return Response({'error': 'El token es inválido.'}, status=status.HTTP_401_UNAUTHORIZED)
