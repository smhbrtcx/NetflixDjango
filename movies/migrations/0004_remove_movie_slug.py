# Generated by Django 3.2.15 on 2022-09-27 06:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0003_movie_slug'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='movie',
            name='slug',
        ),
    ]