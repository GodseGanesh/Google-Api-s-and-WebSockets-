from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from rest_framework.generics import ListAPIView,GenericAPIView
from .models import ChatRoom
from .serilizers import ChatRoomSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

@login_required(login_url='login')
def chat(request):
    return render(request,'chat/chat.html')


class CreateRoom(GenericAPIView):
    permission_classes = [IsAuthenticated]
    queryset = ChatRoom.objects.all()
    serializer_class = ChatRoomSerializer

    def post(self,request,*args,**kwargs):
        room_name = request.data.get('room_name')
        if not room_name:
            return Response({'error': 'Room name is required'}, status=400)

        room, created = ChatRoom.objects.get_or_create(name=room_name)
        if not created:
            return Response({'message': 'Room already exists'}, status=200)
        
        return Response({'message': 'Room created', 'room_name': room.name},status=201)
    
class JoinRoom(GenericAPIView):
    permission_classes = [IsAuthenticated]
   
    def get(self,request,*agrs,**kwargs):
        room_name = request.query_params.get('room_name')

        if not room_name:
            return Response({'error': 'room_name is required'}, status=400)

        return Response(
            {
                'room_name':room_name,
                'username':request.user.username or request.user.email
            },
            status=200

        )

class Temp(GenericAPIView):

    def get(self,request,*agrs,**kwargs):
        return Response(
            {'message':"temp is called"},
            status=200
        )

        
class GetRoomsOfUser(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ChatRoomSerializer

    def get_queryset(self):
        return ChatRoom.objects.filter(user=self.request.user)
    
    def get(self,request,*agrs,**kwagrs):
        queryset = self.get_queryset()
        if queryset.exists():
            serializer = self.get_serializer(queryset,many=True)
            return Response(
                {'message':'rooms for user fetch successfully!',
                 'data': serializer.data},
                status=200
            )
        
        return Response(
            {'message':'no rooms found'},
            status=400
        )

    
    


   
