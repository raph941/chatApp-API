# Generated by Django 3.0 on 2020-10-17 12:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='image_url',
        ),
    ]
