# Generated by Django 4.1.7 on 2023-05-11 09:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_remove_data_user_age_data_user_nsfw_content'),
    ]

    operations = [
        migrations.AddField(
            model_name='data_user',
            name='description',
            field=models.CharField(max_length=500, null=True),
        ),
    ]