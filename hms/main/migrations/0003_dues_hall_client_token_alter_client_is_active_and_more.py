# Generated by Django 5.0.3 on 2024-03-21 17:13

import datetime
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_alter_client_email_alter_client_password'),
    ]

    operations = [
        migrations.CreateModel(
            name='Dues',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Hall',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, unique=True, verbose_name='Name')),
                ('max_occupancy', models.IntegerField(default=0, verbose_name='max_occupancy')),
                ('current_occupancy', models.IntegerField(default=0, verbose_name='current_occupancy')),
                ('no_of_rooms', models.IntegerField(default=0, verbose_name='no_of_rooms')),
            ],
        ),
        migrations.AddField(
            model_name='client',
            name='token',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='client',
            name='is_active',
            field=models.BooleanField(default=False),
        ),
        migrations.CreateModel(
            name='Complaint',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('content', models.TextField(default='')),
                ('date_created', models.DateField(default=datetime.datetime.now)),
                ('hall', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='hall_complaints', to='main.hall')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.hall')),
            ],
            options={
                'verbose_name_plural': 'Complaint',
            },
        ),
        migrations.CreateModel(
            name='Notice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='', max_length=200)),
                ('content', models.TextField(default='')),
                ('date_created', models.DateTimeField(default=datetime.datetime.now)),
                ('image', models.ImageField(upload_to=None)),
                ('hall', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='hall_notices', to='main.hall')),
            ],
            options={
                'verbose_name_plural': 'Notices',
            },
        ),
    ]
