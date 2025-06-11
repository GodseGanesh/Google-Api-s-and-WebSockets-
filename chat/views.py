from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from rest_framework.generics import ListAPIView,GenericAPIView
from rest_framework.views import APIView
from .models import ChatRoom
from .serilizers import ChatRoomSerializer,CustomTokenObtainPairSerializer,RegisterSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.status import HTTP_200_OK,HTTP_201_CREATED,HTTP_400_BAD_REQUEST

@login_required(login_url='login')
def chat(request):
    return render(request,'chat/chat.html')


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class Register(APIView):
    def post(self,request,*agrs,**kwargs):

        serilalizer = RegisterSerializer(data=request.data)

        if serilalizer.is_valid():
            user = serilalizer.save()
            refersh = RefreshToken.for_user(user)
            return Response({
            'access': refersh.access_token,
            'refresh': str(refersh), 
            'username': user.username,
            'email': user.email,
            'id': user.id
        }, status=HTTP_201_CREATED)

        return Response({
            'deatil':serilalizer.errors
        },status=HTTP_400_BAD_REQUEST)

class CreateRoom(GenericAPIView):
    permission_classes = [IsAuthenticated]
    queryset = ChatRoom.objects.all()
    serializer_class = ChatRoomSerializer

    def post(self, request, *args, **kwargs):
        room_name = request.data.get('room_name')
        description = request.data.get('description', '')  # optional field

        if not room_name:
            return Response({'error': 'Room name is required'}, status=400)

        # Check if room already exists
        if ChatRoom.objects.filter(name=room_name).exists():
            return Response({'message': 'Room already exists'}, status=200)

        # Create room with creator
        room = ChatRoom.objects.create(
            name=room_name,
            created_by=request.user,
            description=description
        )
        # Add creator to the room's users
        room.users.add(request.user)

        return Response({
            'message': 'Room created',
            'room_name': room.name,
            'created_by': request.user.username,
        }, status=201)

    
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


        
class GetRoomsOfUser(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ChatRoomSerializer

    def get_queryset(self):
        return ChatRoom.objects.filter(users=self.request.user)
    
    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if queryset.exists():
            serializer = self.get_serializer(queryset, many=True)
            return Response(
                {
                    'message': 'Rooms for user fetched successfully!',
                    'data': serializer.data
                },
                status=200
            )
        
        return Response({'message': 'No rooms found'}, status=404)
    

class GetRooms(ListAPIView):
    model = ChatRoom
    serializer_class = ChatRoomSerializer
    queryset = ChatRoom.objects.all()

class FilterRooms(GenericAPIView):
    serializer_class = ChatRoomSerializer
    queryset = ChatRoom.objects.all()
    def get(self,request,*agrs,**kwargs):
        name = request.query_params.get('q','')
        queryset = self.get_queryset().filter(name__icontains=name)
        serializer = self.get_serializer(queryset,many=True)

        return Response(
            {
            'status':'sucess',
                'message':'data fetched sucessfully ',
                'data':serializer.data
                },
                status=status.HTTP_200_OK
        )
        
        


    


    


    


   
