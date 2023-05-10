from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class data_user(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nsfw_content = models.BooleanField(blank=True)
    image_profile = models.ImageField(blank=True)
    email = models.EmailField(max_length=100, unique=True)
    description = models.CharField(max_length=500, null=True)
    token = models.CharField(max_length=40, unique=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.token = self.generate_token()
        return super(data_user, self).save(*args, **kwargs)

    def generate_token(self):
        token = User.objects.make_random_password(length=40)
        while data_user.objects.filter(token=token).exists():
            token = User.objects.make_random_password(length=40)
        return token

    def __str__(self):
        return self.user.username

    def get_token(self):
        return self.token  # Return the token value directly
