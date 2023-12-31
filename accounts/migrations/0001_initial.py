# Generated by Django 4.2.8 on 2023-12-20 13:44

import django.contrib.auth.validators
from django.db import migrations, models
import django.utils.timezone
import django_countries.fields
import phonenumber_field.modelfields
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('first_name', models.CharField(blank=True, max_length=255, null=True, verbose_name='Prénom(s)')),
                ('last_name', models.CharField(blank=True, max_length=255, null=True, verbose_name='Nom de famille')),
                ('username', models.CharField(error_messages={'unique': "Un utilisateur avec ce pseudo existe déjà. Veuillez choisir un autre s'il vous plaît !"}, help_text='Requis. 150 caractères ou moins. Ne peut contenir des lettres, des chiffres et @/./+/-/_', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name="Nom d'utilisateur")),
                ('email', models.EmailField(error_messages={'unique': 'Un utilisateur avec cette adresse existe déjà.'}, max_length=100, unique=True, verbose_name='Adresse électronique')),
                ('is_staff', models.BooleanField(default=False, help_text="Désigne si un utilisateur peut se connecter à ce site d'administration.", verbose_name="Membre de l'équipe")),
                ('is_active', models.BooleanField(default=True, help_text='Désigne si un utilisateur est toujours actif ou pas. Décochez au lieu de le supprimer.', verbose_name='Actif')),
                ('is_superuser', models.BooleanField(default=False, verbose_name='Utilisateur root')),
                ('account_confirmed', models.BooleanField(default=False, verbose_name='Compte confirmé')),
                ('phone_number', phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, null=True, region=None, verbose_name='Nº de téléphone')),
                ('gender', models.CharField(blank=True, choices=[('male', 'Masculin'), ('female', 'Féminin'), ('undefined', 'Non défini')], max_length=10, null=True, verbose_name='Genre')),
                ('country', django_countries.fields.CountryField(blank=True, max_length=2, null=True, verbose_name='Pays')),
                ('region', models.CharField(blank=True, max_length=100, null=True, verbose_name='Région')),
                ('city', models.CharField(blank=True, max_length=100, null=True, verbose_name='Ville')),
                ('address', models.CharField(blank=True, max_length=100, null=True, verbose_name='Adresse')),
                ('address_2', models.CharField(blank=True, max_length=100, null=True, verbose_name='2e adresse')),
                ('zip_code', models.CharField(blank=True, max_length=5, null=True, verbose_name='Code postal')),
                ('age', models.IntegerField(blank=True, null=True, verbose_name='Âge')),
                ('bio', models.TextField(blank=True, max_length=500, null=True, verbose_name='Bio')),
                ('website', models.URLField(blank=True, null=True, verbose_name='Site web')),
                ('avatar', models.ImageField(blank=True, null=True, upload_to='accounts/avatars/%Y/', verbose_name='Avatar')),
                ('uuid', models.UUIDField(default=uuid.uuid4, unique=True, verbose_name='UUID')),
                ('updated_on', models.DateTimeField(auto_now=True, verbose_name='Date de modification')),
                ('extra_data', models.JSONField(blank=True, null=True, verbose_name='Données supplémentaires')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'Utilisateur',
                'verbose_name_plural': 'Utilisateurs',
                'ordering': ['-date_joined', 'email', 'first_name', 'last_name', 'gender', 'age', 'username', 'country'],
            },
        ),
    ]
