# Generated by Django 5.0.6 on 2024-05-11 17:48

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Dori',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=255)),
                ('ishlab_chiqaruvchi', models.CharField(max_length=255)),
                ('turi', models.CharField(max_length=255)),
                ('narx', models.FloatField(validators=[django.core.validators.MinValueValidator(0)])),
                ('miqdor', models.IntegerField(validators=[django.core.validators.MinValueValidator(0)])),
                ('kelgan_sana', models.DateField(auto_now_add=True)),
                ('muddat', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Sotuv',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('miqdor', models.IntegerField(validators=[django.core.validators.MinValueValidator(0)])),
                ('summa', models.FloatField(validators=[django.core.validators.MinValueValidator(0)])),
                ('sana', models.DateField(auto_now_add=True)),
                ('dori', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainApp.dori')),
            ],
        ),
    ]