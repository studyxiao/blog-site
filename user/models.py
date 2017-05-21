from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    portrait = models.ImageField(upload_to='portrait', blank=True)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = "用户"
        verbose_name_plural = verbose_name
