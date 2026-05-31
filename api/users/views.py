from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from users.models import User
from .serializers import UserSerializer

class RegisterView(APIView):
    def post(self, request):
        email = request.data.get('email')
        if not email:
            return Response({'message': 'All fields are required'}, status=status.HTTP_400_BAD_REQUEST)

        # Check if user already exists
        if User.objects.filter(email=email).exists():
            return Response({'message': 'User already exists'}, status=status.HTTP_400_BAD_REQUEST)
        
        data = request.data.copy()
        data['username'] = email  # map email to username as required by AbstractUser
        
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                'message': 'User registered successfully',
                'userId': user.id
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        
        if not email or not password:
            return Response({'message': 'Email and password are required'}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(request, username=email, password=password)
        
        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response({
                'message': 'Login successful',
                'token': str(refresh.access_token),
                'user': {
                    'id': user.id,
                    'name': user.name,
                    'email': user.email,
                    'role': user.role.role_name if user.role else 'user'
                }
            })
        else:
            return Response({'message': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

class LogoutView(APIView):
    def post(self, request):
        return Response({'message': 'Logged out successfully. Please clear your token on client side.'})

class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response({
            'id': user.id,
            'name': user.name,
            'email': user.email,
            'dial_code': user.dial_code,
            'mobile': user.mobile,
            'role_id': user.role_id
        })

    def put(self, request):
        user = request.user
        name = request.data.get('name')
        dial_code = request.data.get('dial_code')
        mobile = request.data.get('mobile')

        if not name and not dial_code and not mobile:
            return Response({'message': 'Please provide name, dial_code, or mobile to update'}, status=status.HTTP_400_BAD_REQUEST)

        if name:
            user.name = name
        if dial_code:
            user.dial_code = dial_code
        if mobile is not None:
            user.mobile = mobile

        user.save()
        return Response({'message': 'Profile updated successfully'})
