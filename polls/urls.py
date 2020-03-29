from django.urls import path, include
from rest_framework import routers
from django.conf import settings
from django.conf.urls.static import static

from . import views

router = routers.DefaultRouter()
router.register(r'stat-api', views.StatView, basename='StatView')

app_name = 'polls'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('', include(router.urls)),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('line-chart/', views.ChartView.as_view(), name='line-chart'),
    path('analysis/', views.MultiView.as_view(), name='analysis'),
    path('analysis/<int:session_id>/', views.UserInputView.as_view(),name='user_input'),
    path('analysis/calculate/<int:session_id>/', views.AnalysisView.as_view(), name='calculate')
    #path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    #path('<int:user_id>/vote/', views.vote, name='vote'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
