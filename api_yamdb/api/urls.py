from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import UserViewSet, auth_user, get_token
from .views import CategoriesListAPIView, CategoriesDetailAPIView
from .views import GenreListAPIView, GenreDetailAPIView
from .views import TitleListAPIView, TitleDetailAPIView
from .views import ReviewViewSet, CommentViewSet

router = DefaultRouter()
REVIEW_PATH = r'titles/(?P<title_id>\d+)/reviews'
COMMENT_PATH = r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments'

router.register('users', UserViewSet, basename='user')
router.register(REVIEW_PATH, ReviewViewSet, basename='reviews')
router.register(COMMENT_PATH, CommentViewSet, basename='comments')

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
]
