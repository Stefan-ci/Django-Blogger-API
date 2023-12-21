from newsletter.models import Newsletter
from django.contrib.auth.models import User
from django.db.models.signals import post_save


def add_to_newsletter(sender, instance, created, **kwargs):
    if created:
        try:
            Newsletter.objects.get_or_create(email=instance.email)
        except:
            pass

post_save.connect(add_to_newsletter, sender=User)
