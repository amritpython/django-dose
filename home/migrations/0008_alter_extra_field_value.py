# Generated by Django 5.0.7 on 2024-08-27 09:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0007_shopifyuser_last_access_session'),
    ]

    operations = [
        migrations.AlterField(
            model_name='extra',
            name='field_value',
            field=models.TextField(blank=True, null=True),
        ),
    ]
