from rest_framework import viewsets, status, serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action, api_view
from rest_framework_simplejwt.tokens import AccessToken
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework.filters import SearchFilter
from rest_framework.generics import (ListCreateAPIView, DestroyAPIView,
                                     RetrieveUpdateDestroyAPIView)

from .permissions import (IsAdminPermission,
                          IsModeratorPermission,
                          ReadOnlyPermission)
from api_yamdb.settings import DEFAULT_FROM_EMAIL
from .filters import TitleFilterBackend
from .models import (CustomUser, Review, Title,
                     Category, Genre, Category)
from .serializers import (UserSerializer, ReviewSerializer,
                          CommentSerializer, EmailSerializer,
                          CategorySerializer, TitleSerializer,
                          GenreSerializer, TitleCreateSerializer)


@api_view(['POST'])
def auth_user(request):
    serializer = EmailSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    email = serializer.data.get('email')
    username = email.rsplit('@')[0]
    user = CustomUser.objects.get_or_create(email=email, username=username)
    confirmation_code = default_token_generator.make_token(user[0])
    send_mail(
        'Привет! Лови код!',
        confirmation_code,
        DEFAULT_FROM_EMAIL,
        [email],
        fail_silently=False)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
def get_token(request):
    serializer = KodSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    email = serializer.data.get('email')
    confirmation_code = serializer.data.get('confirmation_code')
    user = get_object_or_404(CustomUser, email=email, is_active=True)
    if default_token_generator.check_token(user, confirmation_code):
        token = AccessToken.for_user(user)
        return Response(
            {'token': str(token)},
            status=status.HTTP_200_OK)
    return Response(status=status.HTTP_400_BAD_REQUEST)


class KodSerializer(serializers.Serializer):
    email = serializers.EmailField()
    confirmation_code = serializers.CharField()


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAdminPermission, )
    queryset = CustomUser.objects.all().order_by('id')
    lookup_field = 'username'
    serializer_class = UserSerializer

    @action(detail=False, permission_classes=(IsAuthenticated, ),
            url_path='me', url_name='me')
    def profile_get(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

    @profile_get.mapping.patch
    @action(methods=['PATCH'], detail=False,
            permission_classes=(IsAuthenticated, ),
            url_path='me', url_name='me')
    def profile_patch(self, request):
        serializer = self.get_serializer(request.user, data=request.data,
                                         partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save(role=request.user.role, partial=True)
        return Response(serializer.data)


class CommonListAPIView(ListCreateAPIView):
    permission_classes = (IsAdminPermission | ReadOnlyPermission, )
    filter_backends = (SearchFilter,)
    search_fields = ('name',)


class CategoriesListAPIView(CommonListAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()


class CategoriesDetailAPIView(DestroyAPIView):
    permission_classes = (IsAdminPermission, )

    def get_object(self):
        return get_object_or_404(Category, slug=self.kwargs.get('slug'))


class GenreListAPIView(CommonListAPIView):
    serializer_class = GenreSerializer
    queryset = Genre.objects.all()


class GenreDetailAPIView(DestroyAPIView):
    permission_classes = (IsAdminPermission, )

    def get_object(self):
        return get_object_or_404(Genre, slug=self.kwargs['slug'])


class TitleListAPIView(ListCreateAPIView):
    permission_classes = (IsAdminPermission | ReadOnlyPermission, )
    queryset = Title.objects.all()
    filter_backends = (TitleFilterBackend,)

    def get_serializer_class(self):
        return (TitleCreateSerializer if self.request.method == 'POST'
                else TitleSerializer)


class TitleDetailAPIView(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAdminPermission | ReadOnlyPermission, )
    queryset = Title.objects.all()

    def get_serializer_class(self):
        return (TitleCreateSerializer if self.request.method
                in ['PATCH', 'PUT'] else TitleSerializer)


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (IsModeratorPermission,
                          IsAuthenticated | ReadOnlyPermission)

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsModeratorPermission,
                          IsAuthenticated | ReadOnlyPermission)

    def get_queryset(self):
        review = get_object_or_404(
            Review, id=self.kwargs.get('review_id'),
            title=self.kwargs.get('title_id'))
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(
            Review, id=self.kwargs.get('review_id'),
            title=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, review=review)
