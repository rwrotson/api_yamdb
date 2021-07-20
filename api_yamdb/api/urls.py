from django.urls import path, include
from rest_framework.routers import DefaultRouter, SimpleRouter

from .views import UserViewSet, ReviewViewSet, CommentViewSet


router = DefaultRouter()
router = SimpleRouter()

router.register('users', UserViewSet, basename='user')
router.register(
    r'titles/(?P<title_id>\d+)/reviews', ReviewViewSet, basename='reviews'
)
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet, basename='comments'
)

urlpatterns = [
    path('v1/', include(router.urls))
]
