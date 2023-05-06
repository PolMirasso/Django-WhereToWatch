from django.db import models
from django.contrib.auth.models import User
from django.db.models import JSONField

# Create your models here.

class UserLists(models.Model):
    
    list_name = models.CharField(max_length=50, null=False, unique=True)
    list_id = models.IntegerField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    list_content = JSONField(default=list)

    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    class Meta:
        # Agregar una clave primaria compuesta para author y list_id
        # Esto garantiza que cada author tenga un list_id único
        constraints = [
            models.UniqueConstraint(fields=['author', 'list_id'], name='unique_list_id'),
            models.UniqueConstraint(fields=['list_id'], name='unique_list_id2')
        ]

    def __str__(self):
        return self.list_name
        