# Generated by Django 4.0.3 on 2022-07-09 18:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Profile', '0002_alter_user_course'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='total_books_due',
            field=models.IntegerField(default=0),
        ),
    ]
