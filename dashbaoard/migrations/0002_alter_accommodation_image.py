# Generated by Django 4.2.3 on 2023-07-17 04:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("dashbaoard", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="accommodation",
            name="image",
            field=models.FileField(upload_to="product_files/"),
        ),
    ]
