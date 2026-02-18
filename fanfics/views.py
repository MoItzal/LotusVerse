from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.utils.http import url_has_allowed_host_and_scheme
from django.contrib import messages
from .forms import FanficForm
from .models import Fanfic, Capitulo, Comentario, Tag, Like, Lista
from accounts.models import Profile
from .forms import PerfilForm

# HOME
def home(request):
    fanfic_da_semana = Fanfic.objects.filter(visibilidade="published").order_by('-likes').first()
    historias_populares = Fanfic.objects.filter(visibilidade="published").order_by('-likes')[:3]

    return render(request, 'home.html', {
        'fanfic_da_semana': fanfic_da_semana,
        'historias_populares': historias_populares
    })


# EXPLORAR
def explorar(request):
    tag_slug = request.GET.get("tag")

    fanfics = Fanfic.objects.filter(visibilidade="published")

    tags = Tag.objects.all()

    if tag_slug:
        fanfics = fanfics.filter(tags__nome=tag_slug)

    context = {
        "fanfics": fanfics,
        "tags": tags,
        "tag_ativa": tag_slug,
    }

    return render(request, "explorar.html", context)

# DETALHE
def fanfic_detail(request, id):
    fanfic = get_object_or_404(Fanfic, id=id)

    # Se for rascunho, só o autor pode ver
    if fanfic.visibilidade == "draft" and fanfic.autor != request.user:
        return redirect("explorar")  # ou pode retornar 404 se preferir

    return render(request, 'ver_fanfic.html', {'fanfic': fanfic})

def ler_agora(request, fanfic_id):
    fanfic = get_object_or_404(Fanfic, id=fanfic_id)

    # não deixar acessar rascunho de outra pessoa
    if fanfic.visibilidade == "draft" and fanfic.autor != request.user:
        return redirect("explorar")

    primeiro = fanfic.capitulos.order_by("ordem").first()

    if not primeiro:
        messages.info(request, "Essa fanfic ainda não tem capítulos publicados. 📌")
        return redirect("fanfic_detail", id=fanfic.id)

    return redirect("ler_capitulo", fanfic_id=fanfic.id, ordem=primeiro.ordem)

# LOGIN
def login_page(request):
    next_url = request.GET.get('next') or request.POST.get('next') or '/'

    if request.method == "POST":
        user = authenticate(
            request,
            username=request.POST.get("username"),
            password=request.POST.get("password")
        )

        if user:
            login(request, user)
            if url_has_allowed_host_and_scheme(next_url, {request.get_host()}):
                return redirect(next_url)
            return redirect('home')

        return render(request, "login.html", {"erro": "Usuário ou senha incorretos"})

    return render(request, "login.html")


# REGISTRO
def register_page(request):
    if request.method == "POST":
        if request.POST["password1"] != request.POST["password2"]:
            return render(request, "register.html", {"erro": "Senhas não coincidem"})

        User.objects.create_user(
            username=request.POST["username"],
            email=request.POST["email"],
            password=request.POST["password1"]
        )
        return redirect("login")

    return render(request, "register.html")


# CRIAR FANFIC
@login_required
def criar_fanfic(request):
    if request.method == "POST":
        fanfic = Fanfic.objects.create(
            titulo=request.POST.get("titulo") or  "História sem título",
            descricao=request.POST.get("descricao") or "",
            conteudo="",
            autor=request.user,
            estado="andamento",
            visibilidade="draft",
        )

        return redirect("editar_fanfic", fanfic_id=fanfic.id)

    return render(request, "fanfics/criar_fanfic.html")

@login_required
def criar_capitulo(request, fanfic_id):
    fanfic = get_object_or_404(
        Fanfic,
        id=fanfic_id,
        autor=request.user
    )

    if request.method == "POST":
        total_capitulos = fanfic.capitulos.count()

        Capitulo.objects.create(
            fanfic=fanfic,
            titulo=request.POST.get("titulo"),
            conteudo=request.POST.get("conteudo"),
            ordem=total_capitulos + 1
        )

        return redirect("editar_fanfic", fanfic_id=fanfic.id)

    return render(request, "fanfics/criar_capitulo.html", {
        "fanfic": fanfic
    })


# COMENTAR
def comentar(request, id):
    fanfic = get_object_or_404(Fanfic, id=id)

    if request.method == "POST":
        Comentario.objects.create(
            fanfic=fanfic,
            autor=request.user.username if request.user.is_authenticated else "Anônimo",
            texto=request.POST["texto"]
        )

    return redirect("fanfic_detail", id=id)


# LIKE
def dar_like(request, id):
    fanfic = get_object_or_404(Fanfic, id=id)
    fanfic.likes += 1
    fanfic.save()
    return redirect("fanfic_detail", id=fanfic.id)


# PERFIL LOGADO
@login_required
def perfil(request):
    perfil, _ = Profile.objects.get_or_create(user=request.user)

    rascunhos = Fanfic.objects.filter(autor=request.user, visibilidade="draft")
    publicadas = Fanfic.objects.filter(autor=request.user, visibilidade="published")

    tab = request.GET.get("tab", "publicadas")  

    return render(request, "perfil.html", {
        "perfil": perfil,
        "rascunhos": rascunhos,
        "publicadas": publicadas,
        "tab": tab,  
    })


# PERFIL AUTOR
def perfil_autor(request, username):
    autor = get_object_or_404(User, username=username)
    perfil, _ = Profile.objects.get_or_create(user=autor)
    fanfics = Fanfic.objects.filter(
        autor=autor,
        visibilidade="published"
        )

    return render(request, "fanfics/perfil_autor.html", {
        "autor": autor,
        "perfil": perfil,
        "fanfics": fanfics,
    })

@login_required
def adicionar_lista(request, fanfic_id, tipo):
    fanfic = get_object_or_404(Fanfic, id=fanfic_id)

    Lista.objects.get_or_create(
        usuario=request.user,
        fanfic=fanfic,
        tipo=tipo
    )

    return redirect("fanfic_detail", id=fanfic.id)



# SOBRE / CONTATO
def sobre(request):
    return render(request, "sobre.html")


def contato(request):
    return render(request, "contato.html")

@login_required
def toggle_like(request, id):
    fanfic = get_object_or_404(Fanfic, id=id)

    like, created = Like.objects.get_or_create(
        usuario=request.user,
        fanfic=fanfic
    )

    if not created:
        # usuário já curtiu → remover like
        like.delete()
        fanfic.likes -= 1
    else:
        # novo like
        fanfic.likes += 1

    fanfic.save()
    return redirect("fanfic_detail", id=fanfic.id)


@login_required
def editar_perfil(request):
    perfil, _ = Profile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        form = PerfilForm(request.POST, request.FILES, instance=perfil)
        if form.is_valid():
            form.save()
            messages.success(request, "Perfil atualizado! ✅")
            return redirect("perfil")  # volta pro /perfil/
        else:
            messages.error(request, "Não foi possível salvar. Veja os erros abaixo. ❌")
    else:
        form = PerfilForm(instance=perfil)

    return render(request, "accounts/editar_perfil.html", {"form": form})



@login_required
def editar_fanfic(request, fanfic_id):
    fanfic = get_object_or_404(
        Fanfic,
        id=fanfic_id,
        autor=request.user
    )

    if request.method == "POST":
        fanfic.titulo = request.POST.get("titulo")
        fanfic.descricao = request.POST.get("descricao")
        fanfic.conteudo = request.POST.get("conteudo")
        fanfic.save()

        return redirect("editar_fanfic", fanfic_id=fanfic.id)

    return render(request, "fanfics/editar_fanfic.html", {
        "fanfic": fanfic
    })

@login_required
def editar_capitulo(request, fanfic_id, capitulo_id):
    fanfic = get_object_or_404(Fanfic, id=fanfic_id, autor=request.user)
    capitulo = get_object_or_404(Capitulo, id=capitulo_id, fanfic=fanfic)

    if request.method == "POST":
        capitulo.titulo = request.POST.get("titulo", capitulo.titulo)
        capitulo.conteudo = request.POST.get("conteudo", capitulo.conteudo)
        capitulo.save()
        messages.success(request, "Capítulo salvo com sucesso! ✅")
        return redirect("editar_fanfic", fanfic_id=fanfic.id)

    return render(request, "editar_capitulo.html", {"fanfic": fanfic, "capitulo": capitulo})

@login_required
def publicar_fanfic(request, fanfic_id):
    fanfic = get_object_or_404(Fanfic, id=fanfic_id, autor=request.user)

    if request.method == "POST":
        fanfic.visibilidade = "published"
        fanfic.save()

    return redirect("editar_fanfic", fanfic_id=fanfic.id)

@login_required
def excluir_fanfic(request, fanfic_id):
    fanfic = get_object_or_404(Fanfic, id=fanfic_id, autor=request.user)

    if request.method == "POST":
        fanfic.delete()
        messages.success(request, "Fanfic excluída com sucesso.")
        return redirect("perfil")

    return redirect("editar_fanfic", fanfic_id=fanfic.id)

@login_required
def painel_fanfic(request, fanfic_id):
    fanfic = get_object_or_404(Fanfic, id=fanfic_id, autor=request.user)

    capitulos = fanfic.capitulos.order_by("ordem")

    return render(request, "fanfics/painel_fanfic.html", {
        "fanfic": fanfic,
        "capitulos": capitulos,
    })


def ler_capitulo(request, fanfic_id, ordem):
    fanfic = get_object_or_404(Fanfic, id=fanfic_id)

    capitulo = get_object_or_404(
        Capitulo,
        fanfic=fanfic,
        ordem=ordem
    )

    capitulo_anterior = Capitulo.objects.filter(
        fanfic=fanfic,
        ordem__lt=ordem
    ).last()

    proximo_capitulo = Capitulo.objects.filter(
        fanfic=fanfic,
        ordem__gt=ordem
    ).first()

    return render(request, "fanfics/ler_capitulo.html", {

        "fanfic": fanfic,
        "capitulo": capitulo,
        "capitulo_anterior": capitulo_anterior,
        "proximo_capitulo": proximo_capitulo,
    })

@login_required
def perfil_usuario(request):
    ultimas_leituras = []  # depois ligamos ao model
    return render(request, "fanfics/perfil_usuario.html", {
        "ultimas_leituras": ultimas_leituras,
    })