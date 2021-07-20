from django.urls import path

from ..views import CategoriesListAPIView, CategoriesDetailAPIView

app_name = 'titles'

urlpatterns = [
    path('', CategoriesListAPIView.as_view(), name='categories_list'),
    path('<slug:slug>/', CategoriesDetailAPIView.as_view(), name='categories_detail'),
]
