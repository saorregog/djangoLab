# Generated by Django 5.0 on 2023-12-21 13:33

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Posts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='created at')),
                ('is_active', models.BooleanField(default=True, verbose_name='active')),
                ('title', models.CharField(max_length=100)),
                ('content', models.TextField()),
                ('read_permission', models.CharField(choices=[('owner', 'Owner'), ('team', 'Team'), ('authenticated', 'Authenticated'), ('public', 'Public')], default='owner', max_length=13)),
                ('edit_permission', models.CharField(choices=[('owner', 'Owner'), ('team', 'Team'), ('authenticated', 'Authenticated'), ('public', 'Public')], default='owner', max_length=13)),
            ],
            options={
                'ordering': ['created_at'],
                'abstract': False,
            },
        ),
    ]
