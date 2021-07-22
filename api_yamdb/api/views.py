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
from .models import (CustomUser, Review, Title, Category,
                     Genre, Category, Comment)
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
    permission_classes = [IsAdminPermission]
    queryset = CustomUser.objects.all().order_by('id')
    lookup_field = 'username'
    serializer_class = UserSerializer

    @action(detail=False, permission_classes=[IsAuthenticated],
            url_path='me', url_name='me')
    def profile_get(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

    @profile_get.mapping.patch
    @action(methods=['PATCH'], detail=False,
            permission_classes=[IsAuthenticated],
            url_path='me', url_name='me')
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
        return (TitleCreateSerializer if self.request.method == 'POST'
                else TitleSerializer)


class TitleDetailAPIView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminPermission | ReadOnlyPermission]
    queryset = Title.objects.all()

    def get_serializer_class(self):
        return (TitleCreateSerializer if self.request.method
                in ['PATCH', 'PUT'] else TitleSerializer)


class ReviewListAPIView(ListCreateAPIView):
    permission_classes = [IsAuthenticated | ReadOnlyPermission]
    serializer_class = ReviewSerializer

    def get_queryset(self):
        return Review.objects.filter(title=self.kwargs.get('pk'))

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs.get('pk'))
        serializer.save(title=title, author=self.request.user)


class ReviewDetailAPIView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminPermission | IsModeratorPermission]
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def get_object(self):
        return get_object_or_404(
            Review,
            title=self.kwargs.get('pk'),
            id=self.kwargs.get('rpk')
        )


class CommentListAPIView(ListCreateAPIView):
    permission_classes = [IsAuthenticated | ReadOnlyPermission]
    serializer_class = CommentSerializer

    def get_queryset(self):
        return Comment.objects.filter(review=self.kwargs.get('rpk'))

    def perform_create(self, serializer):
        review = get_object_or_404(Review, id=self.kwargs.get('rpk'))
        serializer.save(review=review, author=self.request.user)


class CommentDetailAPIView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminPermission | IsModeratorPermission]
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_object(self):
        return get_object_or_404(
            Comment,
            review=self.kwargs.get('rpk'),
            id=self.kwargs.get('cpk')
        )
