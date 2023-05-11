from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class data_user(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nsfw_content = models.BooleanField(blank=True)
    image_profile = models.ImageField(blank=True)
    description = models.CharField(max_length=500, null=True)

    def __str__(self):
        return self.user.username
