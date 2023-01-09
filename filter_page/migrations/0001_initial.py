# Generated by Django 4.1.5 on 2023-01-09 11:46

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='App',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_app', models.CharField(max_length=200, unique=True)),
                ('company', models.CharField(max_length=200)),
                ('email', models.EmailField(max_length=254, null=True)),
                ('release', models.DateTimeField()),
            ],
        ),
    ]