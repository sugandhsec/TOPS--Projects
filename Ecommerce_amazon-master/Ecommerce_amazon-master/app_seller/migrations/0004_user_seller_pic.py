# Generated by Django 4.0.4 on 2022-06-02 06:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_seller', '0003_alter_products_pic'),
    ]

    operations = [
        migrations.AddField(
            model_name='user_seller',
            name='pic',
            field=models.FileField(default='anonymous.jpg', upload_to='seller_images'),
        ),
    ]
