from django.urls import path
from . import views

app_name = 'tarefas'

urlpatterns = [
    path(
        'v1/',
        views.tarefa_list_create_fbv,
        name='lista-fbv',
    ),
    path(
        'v1/<int:pk>/',
        views.tarefa_detail_fbv,
        name='detalhe-fbv',
    ),

    path(
        'v2/',
        views.TarefaListCreateAPIView.as_view(),
        name='lista-cbv',
    ),
    path(
        'v2/<int:pk>/',
        views.TarefaDetailAPIView.as_view(),
        name='detalhe-cbv',
    ),

    path(
        'v3/',
        views.TarefaListCreate.as_view(),
        name='lista-generic',
    ),
    path(
        'v3/<int:pk>/',
        views.TarefaDetail.as_view(),
        name='detalhe-generic',
    ),
]