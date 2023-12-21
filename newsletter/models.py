from django.db import models
from django.utils.translation import gettext_lazy as _


class Newsletter(models.Model):
    email = models.EmailField(unique=True, verbose_name=_("Adresse électronique"))
    is_subscribed = models.BooleanField(default=True, verbose_name=_("Inscrit"))
    is_deleted = models.BooleanField(default=False, verbose_name=_("Supprimé"))
    date = models.DateTimeField(auto_now_add=True, verbose_name=_("Date"))
    updated_on = models.DateTimeField(auto_now=True, verbose_name=_("Date de modification"))
    extra_data = models.JSONField(null=True, blank=True, verbose_name=_("Données supplémentaires"))
    
    class Meta:
        ordering = ["-date", "email"]
        verbose_name = _("Newsletter")
        verbose_name_plural = _("Newsletter")

    def __str__(self):
        return str(self.email)
    
    def save(self, *args, **kwargs):
        if self.is_deleted:
            self.is_subscribed = False
        super(Newsletter, self).save(*args, **kwargs)
