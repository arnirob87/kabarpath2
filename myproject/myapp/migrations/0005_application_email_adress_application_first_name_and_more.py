# Generated by Django 5.0.6 on 2024-07-08 15:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0004_application'),
    ]

    operations = [
        migrations.AddField(
            model_name='application',
            name='email_adress',
            field=models.EmailField(blank=True, max_length=15, null=True),
        ),
        migrations.AddField(
            model_name='application',
            name='first_name',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='application',
            name='last_name',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='application',
            name='phone_number',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
    ]