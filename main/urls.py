from django.urls import path
from .views import PicturesCreateView, PicturesListView

app_name = 'main'

urlpatterns = [
    path('pictures/', PicturesListView.as_view(), name='pictures'),
    path('pictures/add/', PicturesCreateView.as_view(), name='add_picture'),
]
