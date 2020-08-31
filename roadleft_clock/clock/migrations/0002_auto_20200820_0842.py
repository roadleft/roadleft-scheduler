# Generated by Django 3.1 on 2020-08-20 08:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clock', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Interval',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('weeks', models.SmallIntegerField(default=0, help_text='number of weeks to wait')),
                ('days', models.SmallIntegerField(default=0, help_text='number of days to wait')),
                ('hours', models.SmallIntegerField(default=0, help_text='umber of hours to wait')),
                ('minutes', models.SmallIntegerField(default=0, help_text='umber of minutes to wait')),
                ('seconds', models.SmallIntegerField(default=0, help_text='umber of seconds to wait')),
                ('start_date', models.DateTimeField(blank=True, help_text='starting point for the interval calculation', null=True)),
                ('end_date', models.DateTimeField(blank=True, help_text='latest possible date/time to trigger on', null=True)),
                ('jitter', models.SmallIntegerField(default=1, help_text='advance or delay the job execution by ``jitter`` seconds at most')),
            ],
        ),
        migrations.AlterField(
            model_name='date',
            name='task',
            field=models.CharField(choices=[('helloworld', 'helloworld')], max_length=20),
        ),
    ]
