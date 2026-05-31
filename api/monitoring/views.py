from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from monitoring.models import Website, CheckLog
from .serializers import WebsiteSerializer, CheckLogSerializer

class WebsiteListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        websites = Website.objects.filter(user=request.user).order_by('-created_at')
        serializer = WebsiteSerializer(websites, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = WebsiteSerializer(data=request.data)
        if serializer.is_valid():
            if not request.data.get('name') or not request.data.get('url') or not request.data.get('email1'):
                return Response({'message': 'Name, URL, and at least one email are required'}, status=status.HTTP_400_BAD_REQUEST)
            
            website = serializer.save(user=request.user)
            return Response({
                'message': 'Website added successfully',
                'id': website.id
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class WebsiteDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk, user):
        try:
            return Website.objects.get(pk=pk, user=user)
        except Website.DoesNotExist:
            return None

    def get(self, request, pk):
        website = self.get_object(pk, request.user)
        if not website:
            return Response({'message': 'Website not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = WebsiteSerializer(website)
        return Response(serializer.data)

    def put(self, request, pk):
        website = self.get_object(pk, request.user)
        if not website:
            return Response({'message': 'Website not found or unauthorized'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = WebsiteSerializer(website, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Website updated successfully'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        website = self.get_object(pk, request.user)
        if not website:
            return Response({'message': 'Website not found or unauthorized'}, status=status.HTTP_404_NOT_FOUND)
        website.delete()
        return Response({'message': 'Website deleted successfully'})

class TogglePauseView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            website = Website.objects.get(pk=pk, user=request.user)
        except Website.DoesNotExist:
            return Response({'message': 'Website not found'}, status=status.HTTP_404_NOT_FOUND)
        
        website.is_paused = not website.is_paused
        website.save()
        status_text = 'paused' if website.is_paused else 'resumed'
        return Response({
            'message': f'Monitoring {status_text}',
            'is_paused': website.is_paused
        })

class ActivityLogView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        logs = CheckLog.objects.filter(website__user=request.user).order_by('-check_time')[:10]
        serializer = CheckLogSerializer(logs, many=True)
        return Response(serializer.data)
