# Generated by Django 2.2.7 on 2019-11-18 19:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appEball', '0005_auto_20191118_1934'),
    ]

    operations = [
        migrations.AddField(
            model_name='tournament',
            name='maxTeams',
            field=models.IntegerField(default=5),
            preserve_default=False,
        ),
    ]
