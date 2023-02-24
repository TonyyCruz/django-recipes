# Generated by Django 4.1.7 on 2023-02-24 22:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("recipes", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="recipe",
            name="cover",
            field=models.ImageField(
                default="recipes/covers/util_image/No-Image-Placeholder.svg.png",
                upload_to="recipes/covers/%Y/%m/%d",
            ),
        ),
    ]
