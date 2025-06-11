
from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
    
    TokenRefreshView,
)


urlpatterns = [
    path('chat/', views.chat),
    path('create_room/',views.CreateRoom.as_view(),name='create_room'),
    path('join_room/',views.JoinRoom.as_view(),name='join_room'),
    path('get_rooms/',views.GetRoomsOfUser.as_view(),name='get_rooms'),
    path('temp_get_rooms/',views.GetRooms.as_view()),
    path('search_rooms/',views.FilterRooms.as_view()),
    path('token/',views.CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', views.Register.as_view()),
   
]