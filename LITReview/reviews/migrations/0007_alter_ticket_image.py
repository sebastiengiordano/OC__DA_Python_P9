# Generated by Django 3.2.6 on 2021-10-08 16:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0006_merge_0003_auto_20211008_1709_0005_alter_ticket_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='image',
            field=models.ImageField(blank=True, default='pictures/no-img.jpg', null=True, upload_to='pictures'),
        ),
    ]