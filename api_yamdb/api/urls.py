from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import UserViewSet, auth_user, get_token
from .views import CategoriesListAPIView, CategoriesDetailAPIView
from .views import GenreListAPIView, GenreDetailAPIView
from .views import TitleListAPIView, TitleDetailAPIView
from .views import ReviewListAPIView, ReviewDetailAPIView
from .views import CommentListAPIView, CommentDetailAPIView

router = DefaultRouter()

router.register('users', UserViewSet, basename='user')

urlpatterns = [
    path('v1/auth/email/', auth_user),
    path('v1/auth/token/', get_token),
    path('v1/', include(router.urls)),
    path('v1/categories/',
         CategoriesListAPIView.as_view(), name='categories_list'),
    path('v1/categories/<slug:slug>/',
         CategoriesDetailAPIView.as_view(), name='categories_detail'),
    path('v1/genres/',
         GenreListAPIView.as_view(), name='genre_list'),
    path('v1/genres/<slug:slug>/',
         GenreDetailAPIView.as_view(), name='genre_detail'),
    path('v1/titles/',
         TitleListAPIView.as_view(), name='title_list'),
    path('v1/titles/<int:pk>/',
         TitleDetailAPIView.as_view(), name='title_detail'),
    path('v1/titles/<int:pk>/reviews/',
         ReviewListAPIView.as_view(), name='review_list'),
    path('v1/titles/<int:pk>/reviews/<int:rpk>/',
         ReviewDetailAPIView.as_view(), name='review_detail'),
    path('v1/titles/<int:pk>/reviews/<int:rpk>/comments/',
         CommentListAPIView.as_view(), name='comment_list'),
    path('v1/titles/<int:pk>/reviews/<int:rpk>/comments/<int:cpk>/',
         CommentDetailAPIView.as_view(), name='comment_detail'),
]
