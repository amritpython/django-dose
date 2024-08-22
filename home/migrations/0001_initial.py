# Generated by Django 5.0.7 on 2024-07-31 11:03

import django.contrib.auth.models
import django.contrib.auth.validators
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='ShopifyUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('shopify_id', models.CharField(blank=True, max_length=255, null=True, unique=True)),
                ('email', models.CharField(blank=True, max_length=255, null=True)),
                ('created_at', models.CharField(blank=True, max_length=255, null=True)),
                ('updated_at', models.CharField(blank=True, max_length=255, null=True)),
                ('first_name', models.CharField(blank=True, max_length=255, null=True)),
                ('last_name', models.CharField(blank=True, max_length=255, null=True)),
                ('verified_email', models.BooleanField(default=False)),
                ('currency', models.CharField(blank=True, max_length=255, null=True)),
                ('phonenumber', models.CharField(blank=True, max_length=255, null=True)),
                ('address_id', models.CharField(blank=True, max_length=255, null=True)),
                ('address_firstname', models.CharField(blank=True, max_length=255, null=True)),
                ('address_lastname', models.CharField(blank=True, max_length=255, null=True)),
                ('address_company', models.CharField(blank=True, max_length=255, null=True)),
                ('address_address_one', models.CharField(blank=True, max_length=255, null=True)),
                ('address_address_two', models.CharField(blank=True, max_length=255, null=True)),
                ('address_city', models.CharField(blank=True, max_length=255, null=True)),
                ('address_province', models.CharField(blank=True, max_length=255, null=True)),
                ('address_country', models.CharField(blank=True, max_length=255, null=True)),
                ('address_zipcode', models.CharField(blank=True, max_length=255, null=True)),
                ('address_phone', models.CharField(blank=True, max_length=255, null=True)),
                ('address_provice_code', models.CharField(blank=True, max_length=255, null=True)),
                ('address_country_code', models.CharField(blank=True, max_length=255, null=True)),
                ('address_country_name', models.CharField(blank=True, max_length=255, null=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Form',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('form_type', models.CharField(blank=True, choices=[('female_pattern_hair_loss', 'female_pattern_hair_loss'), ('male_pattern_hair_loss', 'male_pattern_hair_loss'), ('beard', 'beard'), ('lashes', 'lashes'), ('brows', 'brows'), ('post_chemotheraphy_hair_loss', 'post_chemotheraphy_hair_loss'), ('traction_related_hair_loss', 'traction_related_hair_loss'), ('hair_shedding', 'hair_shedding')], max_length=255)),
                ('ongoing_question', models.IntegerField(default=1)),
                ('is_opened', models.BooleanField(default=False)),
                ('checkbox_1', models.BooleanField(default=False)),
                ('checkbox_2', models.BooleanField(default=False)),
                ('checkbox_3', models.BooleanField(default=False)),
                ('checkbox_4', models.BooleanField(default=False)),
                ('checkbox_5', models.BooleanField(default=False)),
                ('checkbox_6', models.BooleanField(default=False)),
                ('checkbox_7', models.BooleanField(default=False)),
                ('checkbox_8', models.BooleanField(default=False)),
                ('is_completed', models.BooleanField(default=False)),
                ('product_recommendation_message', models.TextField(blank=True, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question_no', models.IntegerField(blank=True)),
                ('question_value', models.TextField(blank=True)),
                ('is_answered', models.BooleanField(default=False)),
                ('answer_tag_used', models.CharField(blank=True, max_length=255, null=True)),
                ('answer_value', models.CharField(blank=True, max_length=255, null=True)),
                ('answer_description', models.TextField(null=True)),
                ('answer_raw_json', models.TextField(null=True)),
                ('form', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.form')),
            ],
        ),
    ]
