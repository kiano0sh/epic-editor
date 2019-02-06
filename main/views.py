from django.core.exceptions import ValidationError
from django.shortcuts import redirect
from django.views.generic import ListView, CreateView
from .models import Pictures
from .forms import PicturesModelForm
from PIL import Image, ImageOps


# Create your views here.

class PicturesCreateView(CreateView):
    queryset = Pictures.objects.all()
    form_class = PicturesModelForm
    template_name = "main/pictures_create.html"
    success_url = '/pictures'

    def form_valid(self, form):
        picture_object = form.save(commit=True)
        form_data = form.cleaned_data
        cleaned_picture = form_data.get('picture')
        cleaned_rotations_degree = form_data.get('rotations_degree')
        cleaned_picture_size = form_data.get('picture_size')
        cleaned_mode_l = form_data.get('mode_l')
        cleaned_crop_amount = form_data.get('crop_amount')

        if cleaned_picture:
            picture_name = picture_object.picture.name
            picture_path = 'media/{picture_name}'.format(picture_name=picture_name)

            def save_pic(pic_object):
                pic_object.save(picture_path)

            def open_pic():
                return Image.open(picture_path)

            if cleaned_rotations_degree:
                save_pic(open_pic().rotate(cleaned_rotations_degree))

            if cleaned_picture_size:
                sizes_lst = cleaned_picture_size.lower().split('x')
                sizes_int = (int(sizes_lst[0]), int(sizes_lst[1]))
                save_pic(open_pic().resize(sizes_int))

            if cleaned_mode_l:
                save_pic(open_pic().convert(mode='L'))

            if cleaned_crop_amount:
                try:
                    save_pic(ImageOps.crop(open_pic(), cleaned_crop_amount))
                except OSError:
                    raise ValidationError("Re-upload the file")

        return redirect(self.success_url)


class PicturesListView(ListView):
    queryset = Pictures.objects.all()
    template_name = "main/pictures_list.html"
