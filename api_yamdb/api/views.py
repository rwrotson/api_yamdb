from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import get_object_or_404

from .models import CustomUser, Review, Title
from .serializers import UserSerializer, ReviewSerializer, CommentSerializer


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


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    pagination_class = PageNumberPagination

    def get_queryset(self):
        title = get_object_or_404(
            Title, id=self.kwargs.get('title_id')
        )
        return title.reviews

    def perform_create(self, serializer):
        title = get_object_or_404(
            Title, id=self.kwargs.get('title_id')
        )
        serializer.save(
            author=self.request.user, title=title
        )


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    pagination_class = PageNumberPagination

    def get_queryset(self):
        review = get_object_or_404(
            Review, title_id=self.kwargs.get('title_id'),
            review_id=self.kwargs.get('review_id')
        )
        return review.comments

    def perform_create(self, serializer):
        review = get_object_or_404(
            Review, title_id=self.kwargs.get('title_id'),
            review_id=self.kwargs.get('review_id')
        )
        serializer.save(
            author=self.request.user, review_id=review
        )
