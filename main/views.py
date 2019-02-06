from django.core.exceptions import ValidationError
from django.shortcuts import redirect
from django.views.generic import ListView, CreateView
from .models import Pictures
from .forms import PicturesModelForm
from PIL import Image, ImageOps
from mimetypes import guess_type
from django.http import HttpResponse
from django.contrib.auth.decorators import user_passes_test


# Create your views here.

class PicturesCreateView(CreateView):
    queryset = Pictures.objects.all()
    form_class = PicturesModelForm
    template_name = "main/pictures_create.html"
    success_url = '/pictures'

    # TODO add download feature
    @staticmethod
    def download_photo(file_path):
        print(file_path)
        with open(file_path, 'rb') as f:
            response = HttpResponse(f, content_type=guess_type(file_path)[0])
            response['Content-Length'] = len(response.content)
            print(response)
            return response

    def form_valid(self, form):
        picture_object = form.save(commit=True)
        form_data = form.cleaned_data
        # picture_id = picture_object.id
        if not self.request.session.session_key:
            self.request.session.save()
        picture_object.session_key = self.request.session.session_key
        picture_object.save()
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
            # self.download_photo(picture_object.picture.url)
        return redirect(self.success_url)


class PicturesListView(ListView):
    template_name = "main/pictures_list.html"

    def get_queryset(self):
        if self.request.user.is_superuser:
            queryset = Pictures.objects.filter(confirmed_by_user=True)
        else:
            queryset = Pictures.objects.filter(confirmed_by_user=True, confirmed_by_admin=True)
        return queryset


@user_passes_test(lambda user: user.is_superuser)
def disconfirm_photo(request, id):
    if request.method is "GET":
        picture_object = Pictures.objects.get(id=id)
        picture_object.confirmed_by_admin = False
        picture_object.save()
        return redirect("main:pictures")
    else:
        print("False request sent")


@user_passes_test(lambda user: user.is_superuser)
def confirm_photo(request, id):
    if request.method is "GET":
        picture_object = Pictures.objects.get(id=id)
        picture_object.confirmed_by_admin = True
        picture_object.save()
        return redirect("main:pictures")
    else:
        print("False request sent")
