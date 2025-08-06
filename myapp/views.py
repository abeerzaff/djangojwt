from rest_framework import generics
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
#from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny 
from .serializers import RegisterSerializer, LoginSerializer, UserSerializer
from django.contrib.auth import get_user_model
#from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status 


# Create your views here.
class RegisterView(generics.CreateAPIView):
    queryset = get_user_model().objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response({"message": "User created successfully"}, status=status.HTTP_201_CREATED)


class LoginView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        password = serializer.validated_data['password']
        User = get_user_model()

        try:
            user_exists = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'detail': 'Invalid email'}, status=401)
        

        
        user = authenticate(request, username=email, password=password)


        if user:
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)

            response = Response({
                "message": "Login successful",
                #"user": UserSerializer(user).data
            })

            # Set short-lived access token
            response.set_cookie(
                key='access_token',
                value=access_token,
                httponly=True,
                secure=True,  # Set False in dev if needed
                samesite='Lax',
                max_age=1800
                

            )

            # Set long-lived refresh token
            response.set_cookie(
                key='refresh_token',
                value=refresh_token,
                httponly=True,
                secure=True,
                samesite='Lax',
                max_age=30 * 24 * 60 * 60  # 30 days
            )

            return response

        else:
            
            return Response({'detail': 'Invalid password'}, status=401)

class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
    
