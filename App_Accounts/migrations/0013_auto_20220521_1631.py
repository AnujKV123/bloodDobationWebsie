# Generated by Django 3.1.2 on 2022-05-21 11:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App_Accounts', '0012_auto_20220420_1131'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user_apportionment',
            name='apportionment_date',
            field=models.DateField(max_length=120),
        ),
    ]