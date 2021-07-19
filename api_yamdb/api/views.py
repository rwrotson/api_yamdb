from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action

from .models import CustomUser
from .serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    #permission_classes = [IsAdmin]
    queryset = CustomUser.objects.all().order_by('id')
    lookup_field = 'username'
    serializer_class = UserSerializer

    @action(detail=False, url_path='me', url_name='me')
    def profile_get(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

    @profile_get.mapping.patch
    @action(methods=['PATCH'], detail=False, url_path='me', url_name='me')
    def profile_patch(self, request):
        serializer = self.get_serializer(request.user, data=request.data,
                                        partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save(role=request.user.role, partial=True)
        return Response(serializer.data)