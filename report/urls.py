from django.urls import path

from . import mapacarga, apontamento

app_name='report'

urlpatterns = [
    path('mapa/imprime/<int:pk>/', mapacarga.imprimeMapa, name='imprime-mapa'),
    path('apontamento/imprime/<int:pk>/', apontamento.imprime, name='imprime-apontamento'),
]