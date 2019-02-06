from django.urls import path
from .views import PicturesCreateView, PicturesListView, disconfirm_photo, confirm_photo

app_name = 'main'

urlpatterns = [
    path('pictures/', PicturesListView.as_view(), name='pictures'),
    path('pictures/add/', PicturesCreateView.as_view(), name='add_picture'),
    path('disconfirm_photo=<id>', disconfirm_photo, name='disconfirm_photo'),
    path('confirm_photo=<id>', confirm_photo, name='confirm_photo'),
]
