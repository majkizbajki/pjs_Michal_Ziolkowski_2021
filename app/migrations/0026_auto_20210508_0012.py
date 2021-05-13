# Generated by Django 3.1.7 on 2021-05-07 22:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0025_remove_event_end_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='queue',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='event',
            name='start_date',
            field=models.DateField(),
        ),
    ]