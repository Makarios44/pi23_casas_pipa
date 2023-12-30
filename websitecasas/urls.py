"""
URL configuration for websitecasas project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from  core import views
from django.contrib import admin
from django.urls import path
from core.views import *
from core.views import formcad, editar_casas, remover_casa
from django.contrib.auth.views import  LogoutView
from core.views import views_perfil
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name="home"),
    path('login/', login_view, name='login'),
    path('perfil/', views_perfil, name='perfil'),
    path('booking/', booking, name ="booking"),
    path('formcad/', formcad, name="formcad"),
    path('editar_casas/<int:id>', editar_casas, name="editar_casas"),
    path('casa_remover/<int:id>',remover_casa, name = "remover_casa"),
    path('cadastro/', views.cadastro, name="cadastro" ),

    path("logout/", LogoutView.as_view(), name="logout"),
 

]

#urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
