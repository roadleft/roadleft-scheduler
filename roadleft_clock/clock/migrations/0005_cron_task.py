# Generated by Django 3.1 on 2020-08-21 03:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clock', '0004_auto_20200821_1032'),
    ]

    operations = [
        migrations.AddField(
            model_name='cron',
            name='task',
            field=models.CharField(choices=[('helloworld', 'helloworld')], default=1, max_length=20),
            preserve_default=False,
        ),
    ]
