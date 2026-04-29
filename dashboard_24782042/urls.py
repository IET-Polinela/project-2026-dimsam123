from django.urls import path
from .views import dashboard_view, kategori_chart, last_reports
from .views import dashboard_view, last_reports, status_chart

urlpatterns = [
    path('', dashboard_view, name='dashboard'),
    path('api/status/', status_chart),
]

urlpatterns = [
    path('', dashboard_view, name='dashboard'),

    path('api/status/', status_chart),
    path('api/kategori/', kategori_chart),
    path('api/last/', last_reports),
]