from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Perfil
from .forms import PerfilForm

@login_required
def editar_perfil(request):
    perfil, _ = Perfil.objects.get_or_create(user=request.user)

    if request.method == "POST":
        form = PerfilForm(request.POST, request.FILES, instance=perfil)
        if form.is_valid():
            form.save()
            return redirect("perfil")  # sua página /perfil/
    else:
        form = PerfilForm(instance=perfil)

    return render(request, "editar_perfil.html", {"form": form})
