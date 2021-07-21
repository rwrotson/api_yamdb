from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import get_object_or_404
from rest_framework.filters import SearchFilter
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, DestroyAPIView

#from .permissions import IsAdminPermission, ReadOnlyPermission
from .filters import TitleFilterBackend
from .models import CustomUser, Review, Comment
from .models import Category, Genre, Title
from .serializers import UserSerializer, ReviewSerializer 
from .serializers import CommentSerializer
from .serializers import CategorySerializer, TitleSerializer, GenreSerializer, TitleCreateSerializer


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
    #permission_classes = [IsAdminPermission | ReadOnlyPermission]
    filter_backends = [SearchFilter]
    search_fields = ('name',)


class CategoriesListAPIView(CommonListAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()


class CategoriesDetailAPIView(DestroyAPIView):
    #permission_classes = [IsAdminPermission]

    def get_object(self):
        return get_object_or_404(Category, slug=self.kwargs['slug'])


class GenreListAPIView(CommonListAPIView):
    serializer_class = GenreSerializer
    queryset = Genre.objects.all()


class GenreDetailAPIView(DestroyAPIView):
    #permission_classes = [IsAdminPermission]

    def get_object(self):
        return get_object_or_404(Genre, slug=self.kwargs['slug'])


class TitleListAPIView(ListCreateAPIView):
    #permission_classes = [IsAdminPermission | ReadOnlyPermission]
    queryset = Title.objects.all()
    filter_backends = [TitleFilterBackend]

    def get_serializer_class(self):
        return TitleCreateSerializer if self.request.method == 'POST' else TitleSerializer


class TitleDetailAPIView(RetrieveUpdateDestroyAPIView):
    #permission_classes = [IsAdminPermission | ReadOnlyPermission]
    queryset = Title.objects.all()

    def get_serializer_class(self):
        return TitleCreateSerializer if self.request.method in ['PATCH', 'PUT'] else TitleSerializer


class ReviewListAPIView(ListCreateAPIView):
    #permission_classes = [IsAdminPermission | ReadOnlyPermission]
    serializer_class = ReviewSerializer

    def get_queryset(self):
        return Review.objects.filter(title=self.kwargs.get('pk'))

    def perform_create(self, serializer):
        title = Title.objects.get(id=self.kwargs.get('pk'))
        serializer.save(title=title, author=self.request.user)


class ReviewDetailAPIView(RetrieveUpdateDestroyAPIView):
    #permission_classes = [IsAdminPermission | ReadOnlyPermission]
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def get_object(self):
        return get_object_or_404(Review, title=self.kwargs.get('pk'), id=self.kwargs.get('rpk'))


class CommentListAPIView(ListCreateAPIView):
    #permission_classes = [IsAdminPermission | ReadOnlyPermission]
    serializer_class = CommentSerializer

    def get_queryset(self):
        return Comment.objects.filter(review=self.kwargs.get('rpk'))

    def perform_create(self, serializer):
        review = Review.objects.get(id=self.kwargs.get('rpk'))
        serializer.save(review=review, author=self.request.user)


class CommentDetailAPIView(RetrieveUpdateDestroyAPIView):
    #permission_classes = [IsAdminPermission | ReadOnlyPermission]
    serializer_class = CommentSerializer
    
    def get_queryset(self):
        return Comment.objects.filter(review=self.kwargs.get('rpk'), id=self.kwargs.get('cpk'))
