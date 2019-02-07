import re
from django import forms
from django.core.exceptions import ValidationError

from .models import Pictures
from PIL import Image


class PicturesModelForm(forms.ModelForm):
    class Meta:
        model = Pictures
        fields = [
            'picture',
            'full_name',
            'picture_size',
            'rotations_degree',
            'crop_amount',
            'mode_l',
            'confirmed_by_user'
        ]

        labels = {
            'mode_l': "Black & White filter",
            'confirmed_by_user': "Share it!",
            'picture': "Choose a picture"
        }

        help_texts = {
            'crop_amount': "The amount of pixels that are going to remove from all four sides of picture",
            'picture_size': "Exp: 200x200",
            'rotations_degree': "From -360 to 360 are allowed"
        }

    def clean_picture_size(self):
        picture_size = self.cleaned_data.get('picture_size')
        if picture_size:
            if not re.match(r'^\d+[xX]\d+$', picture_size):
                raise ValidationError("The format of this value should be like '000x000'\n")
        return picture_size

    def clean(self):
        form_data = self.cleaned_data
        picture = form_data.get('picture')
        crop_amount = form_data.get('crop_amount')
        picture_size = form_data.get('picture_size')

        if crop_amount and picture_size:
            sizes_lst = picture_size.lower().split('x')
            min_side = min(int(sizes_lst[0]), int(sizes_lst[1]))
            if crop_amount >= min_side / 2:
                raise ValidationError(
                    "Crop amount is too high! The maximum value is: {}".format(((min_side / 2) - 1)))
        if crop_amount and picture:
            picture_object = Image.open(picture)
            min_side = min(picture_object.width, picture_object.height)
            if crop_amount >= min_side / 2:
                raise ValidationError(
                    "Crop amount is too high! The maximum value is: {}".format(((min_side / 2) - 1)))

        return form_data
