# Generated by Django 4.2.3 on 2023-07-14 17:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_amenity_image_roomimage'),
    ]

    operations = [
        migrations.DeleteModel(
            name='RoomPrice',
        ),
    ]