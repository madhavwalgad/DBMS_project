# Generated by Django 3.0.6 on 2020-06-16 00:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('secureX_site', '0010_auto_20200616_0407'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='address',
        ),
        migrations.RemoveField(
            model_name='order',
            name='city',
        ),
        migrations.RemoveField(
            model_name='order',
            name='pincode',
        ),
        migrations.RemoveField(
            model_name='order',
            name='state',
        ),
    ]
