# Generated by Django 3.1.2 on 2022-05-22 15:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App_Accounts', '0014_auto_20220522_2040'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='latestName',
            field=models.CharField(blank=True, max_length=500),
        ),
    ]
