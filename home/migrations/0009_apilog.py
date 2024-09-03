# Generated by Django 5.0.7 on 2024-08-31 12:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0008_alter_extra_field_value'),
    ]

    operations = [
        migrations.CreateModel(
            name='ApiLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customer_id', models.CharField(blank=True, max_length=255, null=True)),
                ('order_id', models.CharField(blank=True, max_length=255)),
                ('server', models.CharField(blank=True, max_length=255, null=True)),
                ('date_time', models.DateTimeField(auto_now_add=True)),
                ('error', models.TextField(blank=True, null=True)),
            ],
        ),
    ]
