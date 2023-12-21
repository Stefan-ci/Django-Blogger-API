import uuid
from django.db import models
from django.db.models import Q
from accounts.models import User
from django.utils.text import slugify
from django.contrib.postgres.fields import ArrayField
from django.utils.translation import gettext_lazy as _


class Category(models.Model):
    name = models.CharField(max_length=255, verbose_name=_("Nom"))
    slug = models.SlugField(max_length=500, null=True, blank=True, editable=False)
    is_active = models.BooleanField(default=True, verbose_name=_("Actif"))
    date = models.DateTimeField(auto_now_add=True, verbose_name=_("Date"))
    updated_on = models.DateTimeField(auto_now=True, verbose_name=_("Date de modification"))
    
    class Meta:
        verbose_name = _("Catégorie")
        verbose_name_plural = _("Catégories")
        ordering = ["name", "date"]

    def __str__(self):
        return str(self.name)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)
    
    def posts(self):
        return self.post_set.filter(is_public=True)




class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.SET_NULL, verbose_name=_("Auteur"), null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name=_("Catégorie"))
    title = models.CharField(max_length=255, verbose_name=_("Titre"))
    cover = models.ImageField(upload_to="blog/covers/%Y/", verbose_name=_("Couverture"))
    summary = models.TextField(verbose_name=_("Résumé"), max_length=400, help_text=_("Maximum 400 caractères"))
    description = models.TextField(verbose_name=_("Contenu"))
    tags = ArrayField(models.CharField(max_length=200), null=True, blank=True, verbose_name=_("Mots clés"), size=8)
    slug = models.SlugField(max_length=500, null=True, blank=True, editable=False)
    is_public = models.BooleanField(default=False, verbose_name=_("Public"))
    uuid = models.UUIDField(default=uuid.uuid4, null=True, blank=True, unique=False, verbose_name=_("UUID"))
    date = models.DateTimeField(auto_now_add=True, verbose_name=_("Date"))
    updated_on = models.DateTimeField(auto_now=True, verbose_name=_("Date de modification"))
    extra_data = models.JSONField(null=True, blank=True, verbose_name=_("Données supplémentaires"))
    
    
    class Meta:
        verbose_name = _("Poste")
        verbose_name_plural = _("Postes")
        ordering = ["-date", "title", "is_public"]

    def __str__(self):
        return str(self.title)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Post, self).save(*args, **kwargs)
    
    def similar_posts(self):
        posts = Post.objects.filter(
            Q(category=self.category) |
            Q(title__icontains=self.title) |
            Q(tags__overlap=self.tags)
        ).exclude(id=self.pk).order_by("-date")[:6]
        return posts

    def comments(self):
        return self.comment_set.all()


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name=_("Publication"))
    user = models.ForeignKey(User, on_delete=models.SET_NULL, verbose_name=_("Utilisateur"), null=True, blank=True)
    comment = models.TextField(verbose_name=_("Contenu"))
    is_public = models.BooleanField(default=True, verbose_name=_("Public"))
    uuid = models.UUIDField(default=uuid.uuid4, null=True, blank=True, unique=False, verbose_name=_("UUID"))
    date = models.DateTimeField(auto_now_add=True, verbose_name=_("Date"))
    updated_on = models.DateTimeField(auto_now=True, verbose_name=_("Date de modification"))
    extra_data = models.JSONField(null=True, blank=True, verbose_name=_("Données supplémentaires"))
    
    class Meta:
        verbose_name = _("Commentaire")
        verbose_name_plural = _("Commentaires")
        ordering = ["user", "post", "-date"]

    
    def __str__(self):
        return str(self.post.title)
