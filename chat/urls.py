
from django.urls import path
from . import views

urlpatterns = [
    path('chat/', views.chat),
    path('create_room/',views.CreateRoom.as_view(),name='create_room'),
    path('join_room/',views.JoinRoom.as_view(),name='join_room'),
    path('temp/',views.Temp.as_view(),name='temp'),
    path('get_rooms/',views.GetRoomsOfUser.as_view(),name='get_rooms'),
   
]