# Generated by Django 3.2.6 on 2021-08-20 12:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0007_auto_20210819_1834'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='book',
            name='description',
        ),
        migrations.AddField(
            model_name='book',
            name='description',
            field=models.ManyToManyField(blank=True, related_name='books', to='book.Description'),
        ),
    ]
