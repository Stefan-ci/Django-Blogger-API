from django.db import models
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField


class Contact(models.Model):
    subject = models.CharField(max_length=150, verbose_name=_("Sujet"))
    name = models.CharField(max_length=150, verbose_name=_("Nom complet"))
    email = models.EmailField(verbose_name=_("Email"))
    phone_number = PhoneNumberField(verbose_name=_("Nº de téléphone"), null=True, blank=True)
    is_answered = models.BooleanField(default=False, verbose_name=_("Répondu"))
    message = models.TextField(verbose_name=_("Message"))
    date = models.DateTimeField(auto_now_add=True, verbose_name=_("Date"))
    updated_on = models.DateTimeField(auto_now=True, verbose_name=_("Date de modification"))
    extra_data = models.JSONField(null=True, blank=True, verbose_name=_("Données supplémentaires"))

    class Meta:
        ordering = ["is_answered", "name", "email", "subject", "date"]
        verbose_name = _("Message")
        verbose_name_plural = _("Messages")

    def __str__(self):
        return f"{self.subject}, {self.email}"
