from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action, api_view
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import get_object_or_404
from rest_framework.filters import SearchFilter
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, DestroyAPIView

from apps.account.permissions import IsAdminPermission, ReadOnlyPermission
from .filters import TitleFilterBackend
from .models import CustomUser, Review, Title, Category, Genre
from .serializers import (UserSerializer, ReviewSerializer, 
                          CommentSerializer, EmailSerializer,
                          CategorySerializer, TitleSerializer, 
                          GenreSerializer, TitleCreateSerializer)

@api_view(['POST'])
def auth_user(request):
    serializer = EmailSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    email = serializer.data.get('email')
    username = email.rsplit('@')


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


class CommonListAPIView(ListCreateAPIView):
    permission_classes = [IsAdminPermission | ReadOnlyPermission]
    filter_backends = [SearchFilter]
    search_fields = ('name',)


class CategoriesListAPIView(CommonListAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()


class CategoriesDetailAPIView(DestroyAPIView):
    permission_classes = [IsAdminPermission]

    def get_object(self):
        return get_object_or_404(Category, slug=self.kwargs['slug'])


class GenreListAPIView(CommonListAPIView):
    serializer_class = GenreSerializer
    queryset = Genre.objects.all()


class GenreDetailAPIView(DestroyAPIView):
    permission_classes = [IsAdminPermission]

    def get_object(self):
        return get_object_or_404(Genre, slug=self.kwargs['slug'])


class TitleListAPIView(ListCreateAPIView):
    permission_classes = [IsAdminPermission | ReadOnlyPermission]
    queryset = Title.objects.all()
    filter_backends = [TitleFilterBackend]

    def get_serializer_class(self):
        return TitleCreateSerializer if self.request.method == 'POST' else TitleSerializer


class TitleDetailAPIView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminPermission | ReadOnlyPermission]
    queryset = Title.objects.all()

    def get_serializer_class(self):
        return TitleCreateSerializer if self.request.method in ['PATCH', 'PUT'] else TitleSerializer


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
