# Generated by Django 3.1.7 on 2021-03-18 22:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='news',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='news'),
        ),
    ]