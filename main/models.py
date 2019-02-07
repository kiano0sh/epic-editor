import os
import uuid
from django.db import models
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator


class SessionKeys(models.Model):
    session_key = models.CharField(max_length=40, null=True, blank=True)
    created_time = models.DateTimeField(auto_now_add=True)


class Pictures(models.Model):
    def upload_path(self, filename):
        return os.path.join(self.full_name, filename)

    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    session_key = models.ForeignKey(SessionKeys, on_delete=models.CASCADE, null=True, blank=True)
    picture = models.ImageField(upload_to=upload_path)
    full_name = models.CharField(max_length=30)
    rotations_degree = models.IntegerField(
        validators=[MaxValueValidator(360, message="The maximum rotation degree is '360'"),
                    MinValueValidator(-360, message="The minimum rotation degree is '-360'")],
        null=True, blank=True)
    picture_size = models.CharField(max_length=9, null=True, blank=True)
    mode_l = models.BooleanField(default=False)
    crop_amount = models.PositiveIntegerField(null=True, blank=True)
    confirmed_by_user = models.BooleanField(default=False)
    confirmed_by_admin = models.BooleanField(default=True)
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(default=None, blank=True)

    def save(self, *args, **kwargs):
        self.updated_time = timezone.now()
        super(Pictures, self).save(*args, **kwargs)
