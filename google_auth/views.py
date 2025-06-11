from django.shortcuts import redirect,render
from django.contrib.auth import logout
from django.http import FileResponse
from django.contrib.auth.decorators import login_required
from allauth.socialaccount.models import SocialAccount,SocialToken
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .helper import upload_file_to_drive, list_drive_files, download_file_from_drive
from rest_framework.parsers import MultiPartParser, FormParser
import os
import requests
from rest_framework.generics import GenericAPIView
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.models import User
from django.middleware.csrf import get_token
from rest_framework.views import APIView
@api_view(['GET'])
def home(request):
   
    """API to provide basic app information, including Google Drive endpoints."""
    base_url = request.build_absolute_uri("/")
    
    if request.user.is_authenticated:
        return Response({
            "message": "Welcome to the Google Auth API!",
            "user": {
                "username": request.user.username,
                "email": request.user.email,
            },
            "actions": {
                "logout_url": request.build_absolute_uri("/logout/"),
                "user_data_url": request.build_absolute_uri("/api/google/user/"),
                "connect_drive": request.build_absolute_uri("/connect-drive/"),
                "upload_file": request.build_absolute_uri("/upload-file/"),
                "list_files": request.build_absolute_uri("/fetch-files/"),
                "download_file": request.build_absolute_uri("/download-file/<FILE_ID>/")
            }
        })
    else:
        return Response({
            "message": "Welcome to the Google Auth API!",
            "actions": {
                "login_url": request.build_absolute_uri("/accounts/google/login/")
            }
        })

@api_view(['GET'])
def login_user(request):
    """Redirects user to Google OAuth login"""
    google_login_url = "/accounts/google/login/"  # No need for `next=`
    return Response({"redirect_url": request.build_absolute_uri(google_login_url)})

@api_view(['GET'])
def register_user(request):
    """Redirects user to Google OAuth registration"""
    google_login_url = "/accounts/google/login/"  # No need for `next=`
    return Response({"redirect_url": request.build_absolute_uri(google_login_url)})


@api_view(['GET','POST'])
@permission_classes([IsAuthenticated])
def logout_user(request):
    """API for user logout"""
    logout(request)
    return Response({"message": "Logged out successfully"})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def fetch_google_data(request):
    """API to fetch Google user data via allauth"""
    user = request.user

    try:
        social_account = SocialAccount.objects.filter(user=user, provider="google").first()
        if not social_account:
            return Response({"error": "No Google account linked"}, status=400)

        extra_data = social_account.extra_data  

        return Response({
            "basic_info": {
                "username": user.username,
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "is_superuser": user.is_superuser,  
            },
            "google_user_info": {
                "id": extra_data.get("sub"),
                "email": extra_data.get("email"),
                "verified_email": extra_data.get("email_verified"),
                "name": extra_data.get("name"),
                "given_name": extra_data.get("given_name"),
                "family_name": extra_data.get("family_name"),
                "picture": extra_data.get("picture"),
                "locale": extra_data.get("locale"),  
            },
        })

    except Exception as e:
        return Response({"error": str(e)}, status=500)


# GOOGLE DRIVE 

def refresh_google_token(user):
    """Refresh the Google OAuth token if expired."""
    try:
        token = SocialToken.objects.get(account__user=user, account__provider='google')
        response = requests.post(
            "https://oauth2.googleapis.com/token",
            data={
                "client_id": "YOUR_GOOGLE_CLIENT_ID",
                "client_secret": "YOUR_GOOGLE_CLIENT_SECRET",
                "refresh_token": token.token_secret,  # Ensure this is stored!
                "grant_type": "refresh_token",
            }
        )
        new_token = response.json()
        if "access_token" in new_token:
            token.token = new_token["access_token"]
            token.save()
            return new_token["access_token"]
    except SocialToken.DoesNotExist:
        return None
    return None

def get_user_access_token(user):
    """Retrieve the user's Google OAuth token from Allauth."""
    try:
        token = SocialToken.objects.get(account__user=user, account__provider='google')
        return token.token
    except SocialToken.DoesNotExist:
        return None

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def connect_drive(request):
    """Check if the user is authenticated with Google Drive."""
    access_token = get_user_access_token(request.user)
    if not access_token:
        return Response({"error": "Google authentication required."}, status=401)
    print("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
    return Response({"message": "Google Drive connected successfully!"})

def upload(request):
    return render(request,'google_auth/upload.html')

import tempfile  


@api_view(["POST"])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser])
def upload_file(request):
    """Upload a file to Google Drive."""
    access_token = get_user_access_token(request.user)
    if not access_token:
        return Response({"error": "Google authentication required."}, status=401)

    if "file" not in request.FILES:
        return Response({"error": "File is required."}, status=400)

    file = request.FILES["file"]

    # ✅ Create a valid temporary file path
    with tempfile.NamedTemporaryFile(delete=False, suffix=f"_{file.name}") as temp_file:
        file_path = temp_file.name
        for chunk in file.chunks():
            temp_file.write(chunk)

    try:
        file_id = upload_file_to_drive(access_token, file_path, file.name, file.content_type)
        return Response({"message": "File uploaded successfully!", "file_id": file_id})
    finally:
        os.remove(file_path)  # ✅ Cleanup temp file



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def fetch_files(request):
    """Fetch the list of files from Google Drive."""
    access_token = get_user_access_token(request.user)
    if not access_token:
        return Response({"error": "Google authentication required."}, status=401)

    files = list_drive_files(access_token)
    return Response({"files": files})


from django.http import StreamingHttpResponse

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def download_file(request, file_id):
    """Download a file from Google Drive and stream it to the user."""
    access_token = get_user_access_token(request.user)
    if not access_token:
        return Response({"error": "Google authentication required."}, status=401)

    url = f"https://www.googleapis.com/drive/v3/files/{file_id}?alt=media"
    headers = {"Authorization": f"Bearer {access_token}"}

    response = requests.get(url, headers=headers, stream=True)

    if response.status_code == 200:
        file_name = f"{file_id}.pdf"  # Change the extension accordingly
        res = StreamingHttpResponse(response.iter_content(chunk_size=8192), content_type=response.headers["Content-Type"])
        res["Content-Disposition"] = f'attachment; filename="{file_name}"'
        return res

    return Response({"error": "Failed to download the file."}, status=response.status_code)

class UserLogin(APIView):
    def post(self,request,*args,**kwargs):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(request,username=username,password=password)
        

        if user is not None:
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            login(request,user)

            return Response({
                'message': 'Logged in successfully!',
                'username': user.username,
                'id': user.id,
                'email': user.email,
                'authenticated': user.is_authenticated,
            }, status=200)
        return Response(
            {
                'message':'Invalid Creadentials!',
                
            },status=400

        )

class UserRegisteration(APIView):
    def post(self,request,*args,**kwargs):
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')

        if User.objects.filter(username=username).exists():
           return Response({'message': 'Username already taken!'}, status=400)

        user = User.objects.create_user(username=username,password=password,email=email)
        user.save()

        if user is not None:
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            login(request,user)

            return Response({
                'message': 'Logged in successfully!',
                'username': user.username,
                'id': user.id,
                'email': user.email,
                'authenticated': user.is_authenticated,
            }, status=200)
        
        return Response(
            {
                'message':'Invalid Creadentials!',
                
            },status=400

        )


class UserLogout(APIView):
    def post(self, request):
        logout(request)
        return Response({'message': 'Logged out successfully!'},status=200)

class GoogleLogin(APIView):
    def post(self, request, *args, **kwargs):
        user = request.user
        if user.is_authenticated:
            return Response({
                'message': 'Logged in successfully!',
                'username': user.username,
                'id': user.id,
                'email': user.email,
                'authenticated': user.is_authenticated,
            }, status=200)
        else:
            return Response({
                'message': 'Google login failed!',
            }, status=401)

    


class Temp(GenericAPIView):
    permission_classes = [IsAuthenticated]
    def get(self,request):
        return Response({
    'user': request.user.username if request.user.is_authenticated else None,
    'authenticated': request.user.is_authenticated
})
    

class GetCSRFToken(GenericAPIView):
    def get(self, request, *args, **kwargs):
        token = get_token(request)
        return Response({'csrfToken': token})
