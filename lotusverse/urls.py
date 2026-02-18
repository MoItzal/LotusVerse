from django.contrib import admin
from django.urls import path
from fanfics import views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', views.home, name='home'),
    path('explorar/', views.explorar, name='explorar'),

    path('fanfic/<int:id>/', views.fanfic_detail, name='fanfic_detail'),

    path('login/', views.login_page, name='login'),
    path('register/', views.register_page, name='register'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),

    path('criar/', views.criar_fanfic, name='criar_fanfic'),

    path('fanfic/<int:fanfic_id>/editar/', views.editar_fanfic, name='editar_fanfic'),
    path('fanfic/<int:fanfic_id>/capitulo/novo/', views.criar_capitulo, name='criar_capitulo'),

    path('sobre/', views.sobre, name='sobre'),
    path('contato/', views.contato, name='contato'),

    path('comentar/<int:id>/', views.comentar, name='comentar'),
    path('fanfic/<int:id>/like/', views.dar_like, name='dar_like'),

    path('autor/<str:username>/', views.perfil_autor, name='perfil_autor'),
    path('perfil/editar/', views.editar_perfil, name='editar_perfil'),

    path('perfil/', views.perfil, name='perfil'),

    path('fanfic/<int:fanfic_id>/publicar/', views.publicar_fanfic, name='publicar_fanfic'),
    path('fanfic/<int:fanfic_id>/excluir/', views.excluir_fanfic, name='excluir_fanfic'),

    path(
        'fanfic/<int:fanfic_id>/capitulo/<int:capitulo_id>/editar/',
        views.editar_capitulo,
        name='editar_capitulo'
    ),


    path('fanfic/<int:fanfic_id>/ler/', views.ler_agora, name='ler_agora'),
    path('fanfic/<int:fanfic_id>/capitulo/<int:ordem>/', views.ler_capitulo, name='ler_capitulo'),

    path(
    'fanfic/<int:fanfic_id>/lista/<str:tipo>/',
    views.adicionar_lista,
    name='adicionar_lista'
    ),

    path('fanfic/<int:fanfic_id>/painel/', views.painel_fanfic, name='painel_fanfic'),


]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
