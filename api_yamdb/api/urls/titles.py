from django.urls import path, include

from ..views import TitleListAPIView, TitleDetailAPIView

app_name = 'objects'

urlpatterns = [
    path('', TitleListAPIView.as_view(), name='title_list'),
    path('<int:pk>/', TitleDetailAPIView.as_view(), name='title_detail'),
    path('<int:title_id>/reviews/', include('apps.reviews.urls')),
]
