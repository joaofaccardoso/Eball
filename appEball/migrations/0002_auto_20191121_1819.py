# Generated by Django 2.2.7 on 2019-11-21 18:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('appEball', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='team',
            name='tactic',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appEball.Tactic'),
        ),
    ]