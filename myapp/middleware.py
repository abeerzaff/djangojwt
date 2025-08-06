

from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from django.utils.deprecation import MiddlewareMixin
from django.http import JsonResponse
from datetime import datetime


class RefreshTokenMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # Skip token checks for public endpoints
        if request.path in ['/api/auth/register/', '/api/auth/login/']:
            return None

        access_token = request.COOKIES.get('access_token')
        refresh_token = request.COOKIES.get('refresh_token')

        if access_token:
            try:
                AccessToken(access_token)
                return None
            except Exception:
                if refresh_token:
                    try:
                        new_token = RefreshToken(refresh_token).access_token
                        request.new_access_token = str(new_token)
                        request.new_access_token_exp = new_token['exp']
                        return None
                    except Exception:
                        pass  # Refresh token invalid

        return JsonResponse({'error': 'Authentication failed'}, status=401)

    def process_response(self, request, response):
        if hasattr(request, 'new_access_token'):
            # Convert UNIX timestamp to datetime for cookie expiry
            expires_at = datetime.fromtimestamp(request.new_access_token_exp)

            response.set_cookie(
                key='access_token',
                value=request.new_access_token,
                httponly=True,
                secure=False,  # Set to True in production
                samesite='Lax',
                expires=expires_at  # Set cookie expiry to match token expiry
            )
        return response
        