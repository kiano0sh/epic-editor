from django.core.exceptions import ValidationError
from django.shortcuts import redirect
from django.views.generic import ListView, CreateView
from .models import Pictures, SessionKeys
from .forms import PicturesModelForm
from PIL import Image, ImageOps
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import user_passes_test


class PicturesCreateView(CreateView):
    queryset = Pictures.objects.all()
    form_class = PicturesModelForm
    template_name = "main/pictures_create.html"
    success_url = '/pictures'

    def form_valid(self, form):
        picture_object = form.save(commit=True)
        form_data = form.cleaned_data
        if not self.request.session.session_key:
            self.request.session.save()
        session_key = self.request.session.session_key
        if SessionKeys.objects.filter(session_key=session_key).exists():
            session_key_object = SessionKeys.objects.get(session_key=session_key)
        else:
            session_key_object = SessionKeys.objects.create(session_key=session_key)
        picture_object.session_key = session_key_object
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
        if picture_object.confirmed_by_user:
            return redirect(self.success_url)
        return HttpResponseRedirect("{picture_path}".format(picture_path=picture_object.picture.url))


class PicturesListView(ListView):
    template_name = "main/pictures_list.html"

    def get_queryset(self):
        if self.request.user.is_superuser:
            queryset = Pictures.objects.filter(confirmed_by_user=True)
        else:
            queryset = Pictures.objects.filter(confirmed_by_user=True, confirmed_by_admin=True)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_superuser:
            sessions = SessionKeys.objects.all()
            needed_sessions = list()
            for session in sessions:
                if Pictures.objects.filter(session_key=session, confirmed_by_user=True).exists():
                    needed_sessions.append(session)
            context['sessions'] = needed_sessions
        return context


@user_passes_test(lambda user: user.is_superuser)
def disconfirm_photo(request, id):
    if request.method == "GET":
        picture_object = Pictures.objects.get(id=id)
        picture_object.confirmed_by_admin = False
        picture_object.save()
        return redirect("main:pictures")
    else:
        print("False request was sent!")
        return redirect("main:pictures")


@user_passes_test(lambda user: user.is_superuser)
def confirm_photo(request, id):
    if request.method == "GET":
        picture_object = Pictures.objects.get(id=id)
        picture_object.confirmed_by_admin = True
        picture_object.save()
        return redirect("main:pictures")
    else:
        print("False request was sent!")
        return redirect("main:pictures")
