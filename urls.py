from django.contrib import admin
from django.urls import path
from fanfics import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),  # RAIZ do site
    path('explorar/', views.explorar, name='explorar'),
    path('fanfic/<int:id>/', views.fanfic_detail, name='fanfic_detail'),
    path('login/', views.login_page, name='login'),
    path('register/', views.register_page, name='register'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('criar/', views.criar_fanfic, name='criar'),
    path('sobre/', views.sobre, name='sobre'),
    path('contato/', views.contato, name='contato'),
]
