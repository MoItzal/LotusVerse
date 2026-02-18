from django.contrib import admin
from .models import Fanfic, Tag, Capitulo, Comentario
from .models import Lista


# ===============================
# CAPÍTULOS (INLINE)
# ===============================
class CapituloInline(admin.TabularInline):
    model = Capitulo
    extra = 1


# ===============================
# FANFIC
# ===============================
@admin.register(Fanfic)
class FanficAdmin(admin.ModelAdmin):
    list_display = (
        "titulo",
        "autor",
        "estado",
        "visibilidade",
        "likes",
        "criado_em",
    )

    list_filter = (
        "estado",
        "visibilidade",
        "criado_em",
        "tags",
    )

    search_fields = (
        "titulo",
        "descricao",
        "conteudo",
    )

    filter_horizontal = ("tags",)

    inlines = [CapituloInline]

    ordering = ("-criado_em",)

# ===============================
# TAGS
# ===============================
@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("nome",)
    search_fields = ("nome",)


# ===============================
# COMENTÁRIOS
# ===============================
@admin.register(Comentario)
class ComentarioAdmin(admin.ModelAdmin):
    list_display = (
        "autor",
        "fanfic",
        "criado_em",
    )

    search_fields = (
        "autor",
        "texto",
    )

    list_filter = ("criado_em",)

@admin.register(Lista)
class ListaAdmin(admin.ModelAdmin):
    list_display = ("usuario", "fanfic", "tipo", "criado_em")
    list_filter = ("tipo",)
