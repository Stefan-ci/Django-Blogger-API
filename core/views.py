from django.conf import settings
from django.contrib import messages
from django.urls import translate_url
from django.shortcuts import render, redirect
from django.utils.translation import gettext_lazy as _
from django.utils.translation import check_for_language
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, authenticate, login
from django.http import HttpResponse, HttpResponseRedirect, HttpRequest

from accounts.models import User
from core.forms import LoginForm, CreateUserForm
from core.decorators import unauthenticated_user


@login_required(login_url="templates-core:login")
def home_view(request):
    context = {}
    template_name = "home.html"
    return render(request, template_name, context)


def set_language_view(request: HttpRequest, lang_code: str):
    """Custom language setting view. Django default accepts only POST request. I don't want that.
        (It's not safe. Use at your own risks)

    Args:
        request (HttpRequest): Django HttpRequest
        lang_code (str): Code of the language to set (choices are in {settings.LANGUAGES})

    Returns:
        HttpResponse | HttpResponseRedirect: Return response or redirect to the previous page
    """
    try:
        next_url = request.META.get("HTTP_REFERER")
    except:
        next_url = "/"
    response = HttpResponseRedirect(next_url) if next_url else HttpResponse(status=204)
    if lang_code and check_for_language(lang_code):
        if next_url:
            next_trans = translate_url(next_url, lang_code)
            if next_trans != next_url:
                response = HttpResponseRedirect(next_trans)
        response.set_cookie(
            settings.LANGUAGE_COOKIE_NAME,
            lang_code,
            max_age=settings.LANGUAGE_COOKIE_AGE,
            path=settings.LANGUAGE_COOKIE_PATH,
            domain=settings.LANGUAGE_COOKIE_DOMAIN,
            secure=settings.LANGUAGE_COOKIE_SECURE,
            httponly=settings.LANGUAGE_COOKIE_HTTPONLY,
            samesite=settings.LANGUAGE_COOKIE_SAMESITE,
        )
    return response




@unauthenticated_user
def login_view(request):
    form = LoginForm()
    if request.method == "POST":
        form = LoginForm(request.POST) or None
        if form.is_valid():
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            
            user = authenticate(request, email=email, password=password)
            if user is not None and user.is_active:
                login(request, user)
                messages.success(request, _(f"Bon retour à vous, {str(user.username).capitalize()})"))
                
                # You may send login alert (using celery for example)

                if "next" in request.POST:
                    return redirect(request.POST.get("next"))
                try:
                    return redirect(user.dashboard_url())
                except:
                    return redirect("/")
            else: # user is None or inactive
                messages.warning(request, _("Mot de passe ou email incorrect!"))
        
        else:  # if not form.is_valid()
            errors = form.errors.as_data()
            for error in errors:
                msg = "".join(errors[error][0])
                messages.error(request, _(f"{error.capitalize()}: {msg}"))
            return redirect(".")
    
    context = {
        "form": form,
    }
    template_name = "login.html"
    return render(request, template_name, context)




@login_required(login_url="templates-core:login")
def logout_view(request):
    logout(request)
    messages.success(request, _("Vous vous êtes déconnecté(e) avec succès. À bientôt !"))
    try:
        return redirect(request.META.get("HTTP_REFERER"))
    except:
        return redirect("/")





@unauthenticated_user
def register_view(request):
    """ Register new users (all users created using this view are superuser by default) """
    form = CreateUserForm
    if request.method == "POST":
        form = CreateUserForm(request.POST) or None
        if form.is_valid():
            cleaned_data = form.cleaned_data
            created_user: User = form.save() # Create user object
            
            # Send welcome email to user (with confirmation link)
            
            
            # Sign in the current user
            user = authenticate(request, email=cleaned_data["email"], password=cleaned_data["password"])
            if user is not None and user.is_active:
                login(request, user)
                messages.success(request, _(f"Compte admin créé avec succès!"))
                if "next" in request.POST:
                    return redirect(request.POST.get("next"))
                return redirect("/")
            else:
                messages.info(request, _("Veuillez vous connecter pour accéder à votre tableau de bord !"))
                return redirect("core:login") # Return to login page if user is None or user is inactive
        
        else:  # if not form.is_valid()
            errors = form.errors.as_data()
            for error in errors:
                msg = "".join(errors[error][0])
                messages.error(request, _(f"{error.capitalize()}: {msg}"))
            return redirect(".")
            
    else: # request.method != "POST"
        form = CreateUserForm()
    
    context = {
        "form": form,
    }
    template_name = "register.html"
    return render(request, template_name, context)
