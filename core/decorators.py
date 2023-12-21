from django.contrib import messages
from django.shortcuts import redirect
from django.utils.translation import gettext_lazy as _


def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            if "next" in request.POST or "next" in request.GET:
                return redirect(request.POST.get("next") or request.GET.get("next"))
            messages.warning(request, _("Vous ne pouvez pas vous connecter ou vous insrire à nouveau car vous êtes déjà en ligne"))
            return redirect("/")
        return view_func(request, *args, **kwargs)
    return wrapper_func
