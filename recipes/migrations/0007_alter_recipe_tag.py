# Generated by Django 4.0 on 2023-06-29 00:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tag', '0002_remove_tag_content_type_remove_tag_object_id'),
        ('recipes', '0006_alter_recipe_tag'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='tag',
            field=models.ManyToManyField(blank=True, default='', to='tag.Tag'),
        ),
    ]
