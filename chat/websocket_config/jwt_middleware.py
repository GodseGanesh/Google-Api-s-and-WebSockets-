from urllib.parse import parse_qs
from channels.middleware import BaseMiddleware
from django.contrib.auth.models import AnonymousUser
from rest_framework_simplejwt.tokens import AccessToken
from django.contrib.auth import get_user_model
from asgiref.sync import sync_to_async

User = get_user_model()

@sync_to_async
def get_user_from_token(token):
    try:
        access_token = AccessToken(token)
        user_id = access_token.get("user_id")
        return User.objects.get(id=user_id)
    except Exception as e:
        print(f"JWT Error: {e}")
        return AnonymousUser()

class JwtMiddleware(BaseMiddleware):
    async def __call__(self, scope, receive, send):
        try:
            query_string = scope.get("query_string", b"").decode()
            token_list = parse_qs(query_string).get("token")
            if token_list:
                token = token_list[0]
                scope["user"] = await get_user_from_token(token)
            else:
                scope["user"] = AnonymousUser()
        except Exception as e:
            print(f"Middleware failure: {e}")
            scope["user"] = AnonymousUser()

        return await super().__call__(scope, receive, send)
