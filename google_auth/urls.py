from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name='home'),
    path('api/google/user/', views.fetch_google_data, name='fetch_google_data'),
    path('login/',views.login_user,name='login'),
    path('register/',views.register_user,name='register'),
    path('logout/',views.logout_user,name='logout'),
    path('connect-drive/', views.connect_drive, name='connect-drive'),
    path('upload-file/', views.upload_file, name='upload-file'),
    path('fetch-files/', views.fetch_files, name='fetch-files'),
    path('refresh_google_token/', views.refresh_google_token, name='refresh_google_token'),
    path('download-file/<str:file_id>/', views.download_file, name='download-file'),
    path('upload/',views.upload,name="upload"),
    path('basic_login/',views.UserLogin.as_view(),name="basic_login"),
    path('basic_register/',views.UserRegisteration.as_view(),name="basic_register"),
    path('logout/',views.UserLogout.as_view(),name="logout"),
    path('get_csrf_token/',views.GetCSRFToken.as_view(),name="get_csrf_token"),
    path('google_login/',views.GoogleLogin.as_view(),name="google_login")

   
    
]