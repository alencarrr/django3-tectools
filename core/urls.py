from django.urls import path

from .views import views, views_mapa, views_apt


app_name='core'

# Captura os erros 404 e 500 para tratar em view customizada
handler404 = 'core.views.views.handler404'
handler500 = 'core.views.views.handler500'

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.meulogin, name='login'),
    path('logout/', views.meulogout, name='logout'),
    path('novasenha/', views.trocasenha, name='trocasenha'),
    path('apontamento/list/', views_apt.ApontamentoListView.as_view(), name='lista-apontamento'),
    path('apontamento/view/<int:pk>/', views_apt.ApontamentoDatailView.as_view(), name='view-apontamento'),
    path('apontamento/add/', views_apt.ApontamentoCriarView.as_view(), name='add-apontamento'),
    path('apontamento/edit/<int:pk>/', views_apt.ApontamentoAlterarView.as_view(), name='edit-apontamento'),
    path('apontamento/del/<int:pk>/', views_apt.ApontamentoExcluirView.as_view(), name='del-apontamento'),            
    path('mapa/list/', views_mapa.MapaListView.as_view(), name='lista-mapa'),
    path('mapa/view/<int:pk>/', views_mapa.MapaDatailView.as_view(), name='view-mapa'),
    path('mapa/add/', views_mapa.MapaCreate.as_view(), name='add-mapa'),
    path('mapa/edit/<int:pk>/', views_mapa.MapaUpdate.as_view(), name='edit-mapa'),
    path('mapa/del/<int:pk>/', views_mapa.MapaDelete.as_view(), name='del-mapa'),
    path('mapa/campos/list/<int:idmapa>/', views_mapa.CampoListView.as_view(), name='lista-campos'),
    path('mapa/campos/view/<int:idmapa>/<int:pk>/', views_mapa.CampoDatailView.as_view(), name='view-campo'),
    path('mapa/campos/add/<int:idmapa>/', views_mapa.CampoCreate.as_view(), name='add-campo'),
    path('mapa/campos/edit/<int:idmapa>/<int:pk>/', views_mapa.CampoUpdate.as_view(), name='edit-campo'),
    path('mapa/campos/del/<int:idmapa>/<int:pk>/', views_mapa.CampoDelete.as_view(), name='del-campo'),    
]