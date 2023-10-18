# Create your models here.
from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from django.contrib.auth.models import AbstractUser
import uuid
# Create your models here.

from django.conf import settings


class ListDetails(models.Model):

    PRIORTY_LEVEL = [("High", "High"), ("Medium", "Medium"), ("Low", "Low")]

    desc = models.CharField(max_length=300)
    slug = models.SlugField(unique=True)
    updateDate = models.DateField(default=timezone.now)
    due_date = models.DateField(default=timezone.now, null=True, blank=True)
    is_finished = models.BooleanField(default=False)
    fileUpload = models.FileField(upload_to="uploads/", default=None)
    priority = models.CharField(choices=PRIORTY_LEVEL, max_length=30)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,
                              on_delete=models.CASCADE)

    def __str__(self):
        return self.desc

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.desc)
        super(ListDetails, self).save(*args, **kwargs)

    def delete(self):
        self.fileUpload.delete()
        super().delete()


class CustomUser(AbstractUser):
    userIMG = models.ImageField(upload_to="uploads")
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
