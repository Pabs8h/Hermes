from django.urls import  path
from . import views

urlpatterns= [
    #path('prueba/',views.prueba,name='buscar'),
    path('creacion/',views.creaciontexto,name='creacion'),
    path('analizar/',views.analizar,name='analisis'),
    path('documentos/', views.documentosActuales, name='documentos'),
    path('documentos/<str:pk>', views.documentoActual, name='documento'),
]