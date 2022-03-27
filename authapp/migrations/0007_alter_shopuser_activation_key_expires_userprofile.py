# Generated by Django 4.0 on 2022-03-26 21:10

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('authapp', '0006_alter_shopuser_activation_key_expires_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shopuser',
            name='activation_key_expires',
            field=models.DateTimeField(default=datetime.datetime(2022, 3, 28, 21, 10, 3, 31494, tzinfo=utc), null=True),
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('about', models.TextField(blank=True, null=True, verbose_name='About yourself')),
                ('gender', models.CharField(blank=True, choices=[('M', 'Male'), ('W', 'Female')], max_length=2, verbose_name='Sex')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='authapp.shopuser')),
            ],
        ),
    ]
