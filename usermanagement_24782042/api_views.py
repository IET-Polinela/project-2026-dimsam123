from rest_framework import generics, permissions
from django.contrib.auth import get_user_model
from usermanagement_24782042.serializers import RegisterSerializer

User = get_user_model()

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()  # Sekarang ini tidak akan error lagi
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]