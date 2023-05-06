from django.db import models
from django.contrib.auth.models import User
from django.db.models import JSONField

# Create your models here.

class UserLists(models.Model):
    list_name = models.CharField(max_length=50, null=False)
    list_id = models.AutoField(primary_key=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    list_content = JSONField(default=list)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['author', 'list_id'], name='unique_list_id')
        ]

    def __str__(self):
        return self.list_name

    def add_to_list_content(self, obj_id, obj_type):
        self.list_content.append({'id': obj_id, 'type': obj_type})
        self.save()

    def object_in_list(obj_id, obj_type, list_content):

        for item in list_content:
            if item['id'] == obj_id and item['type'] == obj_type:
                return True
        return False
