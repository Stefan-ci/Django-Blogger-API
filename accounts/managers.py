from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import BaseUserManager



class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None):
        if not email:
            raise ValidationError(_("Veuillez fournir une adresse mail s'il vous plaît!"), code="invalid")
        
        if not username:
            raise ValidationError(_("Veuillez fournir un nom d'utilisateur s'il vous plaît!"), code="invalid")
        
        if self.filter(email=str(email).lower()).exists():
            raise ValidationError(_("Email déjà en cours d'utilisation"), code="unique")
        
        if self.filter(username=str(username).lower()).exists():
            raise ValidationError(_("Nom d'utilisateur déjà en cours d'utilisation"), code="unique")
        
        
        user = self.model(
            email=self.normalize_email(email),
            username = username,
        )
        user.is_active = True
        user.confirmed = False
        user.set_password(password)
        user.save(using=self._db)
        return user


    def create_superuser(self, username, email, password=None):
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            password=password,
        )
        user.is_active = True
        user.is_staff = True
        user.confirmed = True
        user.is_superuser = True
        user.save(using=self._db)
        return user
