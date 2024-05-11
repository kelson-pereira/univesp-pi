"""
Configurações de URL para projeto univesp_pi.

A lista `urlpatterns` roteia URLs para visualizações. Para mais informações consulte:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Exemplos:
Função views
    1. Adicione a importação:  from my_app import views
    2. Adicione a URL em urlpatterns:  path('', views.home, name='home')
Views baseada em uma classe:
    1. Adicione a importação:  from other_app.views import Home
    2. Adicione a URL em urlpatterns:  path('', Home.as_view(), name='home')
Incluindo outra configuração de URL:
    1. Importe a função include(): from django.urls import include, path
    2. Adicione a URL em urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
from combate_mosquito import views

urlpatterns = [
    path('', views.principal, name='principal'),
    path('registros/', views.registros, name='registros'),
    path('registrar/', views.registrar, name='registrar'),
    path('apagar/', views.apagar, name='apagar'),
    path('politica/', views.politica, name='politica'),
    path('mapa/', views.mapa, name='mapa'),
]
