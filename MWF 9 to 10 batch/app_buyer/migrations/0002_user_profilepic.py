# Generated by Django 4.1.7 on 2023-04-12 05:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_buyer', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='profilepic',
            field=models.FileField(default='anonymous.jfif', upload_to='media/'),
        ),
    ]