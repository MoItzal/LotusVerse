from django.db import models
from django.conf import settings
from django.contrib.auth.models import User


# ===============================
# TAG
# ===============================
class Tag(models.Model):
    nome = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.nome


# ===============================
# FANFIC
# ===============================

class Fanfic(models.Model):
    ESTADO_CHOICES = (
        ("andamento", "Em andamento"),
        ("completa", "Completa"),
    )

    VISIBILIDADE_CHOICES = (
        ("draft", "Rascunho"),
        ("published", "Publicado"),
    )

    titulo = models.CharField(max_length=200)
    descricao = models.TextField()
    conteudo = models.TextField()

    autor = models.ForeignKey(User, on_delete=models.CASCADE, related_name="fanfics")

    tags = models.ManyToManyField(Tag, blank=True, related_name="fanfics")

    likes = models.IntegerField(default=0)

    estado = models.CharField(
        max_length=20,
        choices=ESTADO_CHOICES,
        default="andamento"
    )

    visibilidade = models.CharField(
        max_length=10,
        choices=VISIBILIDADE_CHOICES,
        default="draft"
    )

    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titulo


# ===============================
# CAPÍTULO
# ===============================
class Capitulo(models.Model):
    fanfic = models.ForeignKey(
        Fanfic,
        on_delete=models.CASCADE,
        related_name="capitulos"
    )
    titulo = models.CharField(max_length=200)
    conteudo = models.TextField()
    ordem = models.PositiveIntegerField()

    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.ordem} - {self.titulo}"



# ===============================
# COMENTÁRIO
# ===============================
class Comentario(models.Model):
    fanfic = models.ForeignKey(
        Fanfic,
        related_name="comentarios",
        on_delete=models.CASCADE
    )

    autor = models.CharField(max_length=100)
    texto = models.TextField()
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.autor

class Lista(models.Model):
    TIPO_CHOICES = (
        ("favoritos", "Favoritos"),
        ("ler_depois", "Ler depois"),
    )

    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    fanfic = models.ForeignKey(
        Fanfic,
        on_delete=models.CASCADE,
        related_name="listas"
    )

    tipo = models.CharField(
        max_length=20,
        choices=TIPO_CHOICES
    )

    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("usuario", "fanfic", "tipo")

    def __str__(self):
        return f"{self.usuario} • {self.fanfic} • {self.tipo}"

class Like(models.Model):
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    fanfic = models.ForeignKey(
        Fanfic,
        on_delete=models.CASCADE,
        related_name="likes_usuarios"
    )

    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("usuario", "fanfic")

    def __str__(self):
        return f"{self.usuario} curtiu {self.fanfic}"

class Perfil(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="perfil"
    )

    avatar = models.ImageField(
        upload_to="avatars/",
        blank=True,
        null=True
    )

    bio = models.TextField(
        blank=True,
        max_length=300
    )

    def __str__(self):
        return self.user.username
