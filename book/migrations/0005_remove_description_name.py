# Generated by Django 3.2.6 on 2021-08-19 13:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0004_description_title'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='description',
            name='name',
        ),
    ]
