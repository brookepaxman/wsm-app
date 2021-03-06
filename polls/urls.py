from django.urls import path, include
from rest_framework import routers
from django.conf import settings
from django.conf.urls.static import static

from . import views

router = routers.DefaultRouter()
router.register(r'api/stats', views.StatView, basename='StatView')
router.register(r'api/analysis', views.AnalysisSetView, basename='AnalysisSetView')
router.register(r'api/month', views.MonthAnalysisViewSet, basename='MonthAnalysisViewSet')


app_name = 'polls'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('', include(router.urls)),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('analysis/', views.MultiView.as_view(), name='analysis'),
    path('graphs/', views.ChartView.as_view(), name='graphs'),
    path('analysis/<int:session_id>/', views.UserInputView.as_view(),name='user_input'),
    path('realtime', views.RealtimeView.as_view(), name='realtime'),
    path('calc/<int:session_id>/', views.AnalysisView.as_view(), name='calculate'),
    path('generate/', views.GenerateView.as_view(), name='generate')
    #path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    #path('<int:user_id>/vote/', views.vote, name='vote'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
