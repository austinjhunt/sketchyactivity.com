
from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser
from ..serializers import *
from rest_framework.response import Response



class UserProfileView(viewsets.ModelViewSet):
    serializer_class = UserProfileSerializer
    queryset = UserProfile.objects.all()
    permission_classes = [IsAdminUser]
