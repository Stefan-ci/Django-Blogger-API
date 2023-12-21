import uuid
from django.db import models
from accounts.managers import UserManager
from django_countries.fields import CountryField
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.validators import UnicodeUsernameValidator



class User(AbstractUser):
    class GenderChoices(models.TextChoices):
        MALE = ("male", _("Masculin"))
        FEMALE = ("female", _("Féminin"))
        UNDEFINED = ("undefined", _("Non défini"))
    
    
    username_validator = UnicodeUsernameValidator()
    first_name = models.CharField(max_length=255, verbose_name=_("Prénom(s)"), null=True, blank=True)
    last_name = models.CharField(max_length=255, verbose_name=_("Nom de famille"), null=True, blank=True)
    username = models.CharField(
            max_length=150,
            unique=True,
            verbose_name=_("Nom d'utilisateur"),
            validators=[username_validator],
            error_messages={
                "unique": _("Un utilisateur avec ce pseudo existe déjà. Veuillez choisir un autre s'il vous plaît !"),
            },
            help_text=_( "Requis. 150 caractères ou moins. Ne peut contenir des lettres, des chiffres et @/./+/-/_"),
        )
    email = models.EmailField(max_length=100, unique=True, verbose_name=_("Adresse électronique"),
            error_messages={
                "unique": _("Un utilisateur avec cette adresse existe déjà."),
            },
        )
    is_staff = models.BooleanField(default=False, verbose_name=_("Membre de l'équipe"),
        help_text=_("Désigne si un utilisateur peut se connecter à ce site d'administration."))
    is_active = models.BooleanField(default=True, verbose_name=_("Actif"),
        help_text=_("Désigne si un utilisateur est toujours actif ou pas. Décochez au lieu de le supprimer."))
    is_superuser = models.BooleanField(default=False, verbose_name=_("Utilisateur root"))
    account_confirmed = models.BooleanField(default=False, verbose_name=_("Compte confirmé"))
    phone_number = PhoneNumberField(verbose_name=_("Nº de téléphone"), null=True, blank=True)
    gender = models.CharField(choices=GenderChoices.choices, null=True, blank=True, max_length=10, verbose_name=_("Genre"))
    country = CountryField(verbose_name=_("Pays"), null=True, blank=True)
    region = models.CharField(max_length=100, verbose_name=_("Région"), null=True, blank=True)
    city = models.CharField(max_length=100, verbose_name=_("Ville"), null=True, blank=True)
    address = models.CharField(max_length=100, verbose_name=_("Adresse"), null=True, blank=True)
    address_2 = models.CharField(max_length=100, verbose_name=_("2e adresse"), null=True, blank=True)
    zip_code = models.CharField(max_length=5, verbose_name=_("Code postal"), null=True, blank=True)
    age = models.IntegerField(null=True, blank=True, verbose_name=_("Âge"))
    bio = models.TextField(max_length=500, verbose_name=_("Bio"), null=True, blank=True)
    website = models.URLField(null=True, blank=True, verbose_name=_("Site web"))
    avatar = models.ImageField(upload_to="accounts/avatars/%Y/", null=True, blank=True, verbose_name=_("Avatar"))
    uuid = models.UUIDField(default=uuid.uuid4, verbose_name="UUID", unique=True)
    updated_on = models.DateTimeField(auto_now=True, verbose_name=_("Date de modification"))
    extra_data = models.JSONField(null=True, blank=True, verbose_name=_("Données supplémentaires"))
    
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]
    
    objects = UserManager()
    
    class Meta:
        verbose_name = _("Utilisateur")
        verbose_name_plural = _("Utilisateurs")
        ordering = ["-date_joined", "email", "first_name", "last_name", "gender", "age", "username", "country"]

    def __str__(self):
        return f"{self.email}"
    
    def is_male(self) -> bool:
        return self.gender == User.GenderChoices.MALE
    
    def is_female(self) -> bool:
        return self.gender == User.GenderChoices.FEMALE
    
    def is_undefined(self) -> bool:
        return self.gender == User.GenderChoices.UNDEFINED
    
    def get_full_address(self) -> str|None:
        full_address = None
        if self.address:
            full_address = self.address
        if self.address and self.city:
            full_address = f"{self.address}, {self.city}"
        if self.address and self.city and self.zip_code:
            full_address = f"{self.address}, {self.city} {self.zip_code}"
        if self.address and self.city and self.zip_code and self.country:
            full_address = f"{self.address}, {self.city} {self.zip_code}, {self.country.code}"
        return full_address
