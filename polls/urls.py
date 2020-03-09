from django.urls import path

from . import views

app_name = 'polls'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('dummy/', views.DummyView.as_view(), name='dummy'),
    #path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    #path('<int:user_id>/vote/', views.vote, name='vote'),
]
