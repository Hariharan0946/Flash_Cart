from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import generics, permissions
from .serializers import MyTokenObtainPairSerializer, RegisterSerializer

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

class RegisterView(generics.CreateAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = RegisterSerializer
