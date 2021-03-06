# Generated by Django 3.0.6 on 2020-06-03 17:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('secureX_site', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='RequestService',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fname', models.CharField(max_length=42)),
                ('lname', models.CharField(max_length=42)),
                ('email', models.EmailField(max_length=75)),
                ('contact', models.CharField(max_length=20)),
                ('purpose', models.TextField()),
                ('created_on', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('information', models.TextField()),
                ('contact', models.CharField(max_length=20)),
                ('cost', models.CharField(max_length=20)),
            ],
        ),
        migrations.DeleteModel(
            name='Comment',
        ),
        migrations.DeleteModel(
            name='Post',
        ),
        migrations.AddField(
            model_name='requestservice',
            name='service',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='secureX_site.Service'),
        ),
    ]
