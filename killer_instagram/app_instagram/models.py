import os
from uuid import uuid4
from django.db import models
from django.contrib.auth.models import User


def update_filename(instance, filename):
    upload_to = "uploads"
    ext = filename.split(".")[-1]
    filename = f"{uuid4().hex}.{ext}"
    return os.path.join(upload_to, filename)


# Create your models here.
class Picture(models.Model):
    description = models.TextField()
    path = models.ImageField(upload_to=update_filename)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    additional_description = models.CharField(max_length=100)  # Дополнительное текстовое описание
    tags = models.CharField(max_length=200, blank=True)  # Список тегов (можно использовать CharField или ArrayField из django.contrib.postgres.fields)



    def __str__(self):
        return f'{self.user.username}({self.user.email}): {self.path}'