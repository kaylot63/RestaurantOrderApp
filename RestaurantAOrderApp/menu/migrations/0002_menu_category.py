# Generated by Django 5.0.4 on 2024-05-03 16:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='menu',
            name='category',
            field=models.CharField(default='Food', max_length=50),
            preserve_default=False,
        ),
    ]