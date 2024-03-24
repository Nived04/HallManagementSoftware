# Generated by Django 5.0.3 on 2024-03-24 18:13

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='menu',
            name='id',
        ),
        migrations.RemoveField(
            model_name='ration',
            name='id',
        ),
        migrations.AddField(
            model_name='messexpenditure',
            name='type',
            field=models.CharField(choices=[('salaries', 'Salaries'), ('rations', 'Rations')], default='rations', max_length=40, verbose_name='Type'),
        ),
        migrations.AlterField(
            model_name='menu',
            name='hall',
            field=models.OneToOneField(default=None, on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='hall_menu', serialize=False, to='main.hall'),
        ),
        migrations.AlterField(
            model_name='ration',
            name='hall',
            field=models.OneToOneField(default=None, on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='hall_ration', serialize=False, to='main.hall'),
        ),
        migrations.AlterField(
            model_name='ration',
            name='rate1',
            field=models.IntegerField(blank=True, verbose_name='rt1'),
        ),
    ]