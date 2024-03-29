# Generated by Django 4.1.7 on 2023-03-23 02:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Seller',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=30)),
                ('firstname', models.CharField(max_length=20)),
                ('lastname', models.CharField(max_length=20)),
                ('emailid', models.EmailField(max_length=254)),
                ('profilepic', models.FileField(default='anonymous.png', upload_to='profile_pic/')),
            ],
        ),
        migrations.CreateModel(
            name='Products',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_name', models.CharField(max_length=50)),
                ('product_desc', models.TextField()),
                ('product_price', models.IntegerField()),
                ('product_seller', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_seller.seller')),
            ],
        ),
    ]
