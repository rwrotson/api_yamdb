from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import get_object_or_404

from .models import Review, Title
from .serializers import ReviewSerializer, CommentSerializer


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
