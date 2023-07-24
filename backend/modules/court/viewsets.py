from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status, viewsets

from .models import Court
from .serializers import CourtSerializer
from modules.user.permissions import UserPermission


class CourtViewSet(viewsets.ModelViewSet):
    http_method_names = ('post', 'get', 'put', 'delete', 'patch')
    serializer_class = CourtSerializer
    permission_classes = (UserPermission, )
    
    def get_queryset(self):
        return Court.objects.all()
    
    def get_object(self):
        obj = Court.objects.get_object_by_public_id(self.kwargs['pk'])
        self.check_object_permissions(self.request, obj)
        return obj
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    @action(methods=['post'], detail=True)
    def like_court (self, request, *args, **kwargs):
        court = self.get_object()
        user = self.request.user
        
        user.like_court(court)
        
        serializer = self.serializer_class(court)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=['post'], detail=True)
    def remove_liked_court (self, request, *args, **kwargs):
        court = self.get_object()
        user = self.request.user
        
        user.remove_liked_court(court)
        
        serializer = self.serializer_class(court)
        return Response(serializer.data, status=status.HTTP_200_OK)           