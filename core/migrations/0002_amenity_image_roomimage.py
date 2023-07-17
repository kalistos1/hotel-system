# Generated by Django 4.2.3 on 2023-07-14 17:08

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='amenity',
            name='image',
            field=models.ImageField(default=django.utils.timezone.now, upload_to='room_images/'),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='RoomImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image1', models.ImageField(upload_to='room_images/')),
                ('image2', models.ImageField(upload_to='room_images/')),
                ('image3', models.ImageField(upload_to='room_images/')),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.room')),
            ],
        ),
    ]