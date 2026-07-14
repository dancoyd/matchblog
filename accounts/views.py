from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .forms import ProfileUpdateForm, RegisterForm, UserUpdateForm
from .models import Profile


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save()
            Profile.objects.get_or_create(user=user)
            login(request, user)
            messages.success(request, "Tu cuenta fue creada correctamente.")
            return redirect("profile")
    else:
        form = RegisterForm()

    return render(request, "accounts/register.html", {
        "form": form
    })


@login_required
def profile(request):
    profile_obj, created = Profile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        user_form = UserUpdateForm(
            request.POST,
            instance=request.user,
            current_user=request.user
        )
        profile_form = ProfileUpdateForm(
            request.POST,
            request.FILES,
            instance=profile_obj
        )

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Tu perfil fue actualizado correctamente.")
            return redirect("profile")
    else:
        user_form = UserUpdateForm(
            instance=request.user,
            current_user=request.user
        )
        profile_form = ProfileUpdateForm(instance=profile_obj)

    return render(request, "accounts/profile.html", {
        "user_form": user_form,
        "profile_form": profile_form,
        "profile_obj": profile_obj,
    })


@login_required
def logout_user(request):
    if request.method == "POST":
        logout(request)
        messages.success(request, "Cerraste sesión correctamente.")
        return redirect("home")

    return redirect("home")