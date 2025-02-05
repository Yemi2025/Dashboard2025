
from django.urls import path
from . import views  

urlpatterns = [
    path('', views.index, name='index'),
    path('get_graph_data/', views.get_graph_data, name='get_graph_data'),
    path('reports/', views.reports_view, name='reports'),
    path("analytics/", views.analytics_view, name="analytics"),
]