from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from notifications.models import NotificationPreference, NotificationHistory
from .serializers import NotificationPreferenceSerializer, NotificationHistorySerializer

class NotificationPreferenceView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        pref, created = NotificationPreference.objects.get_or_create(user=request.user)
        serializer = NotificationPreferenceSerializer(pref)
        return Response(serializer.data)

    def put(self, request):
        pref, created = NotificationPreference.objects.get_or_create(user=request.user)
        serializer = NotificationPreferenceSerializer(pref, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class NotificationHistoryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        history = NotificationHistory.objects.filter(user=request.user).order_by('-created_at')
        serializer = NotificationHistorySerializer(history, many=True)
        return Response(serializer.data)
