from rest_framework.routers import DefaultRouter
from main_app.views import ReportViewSet

router = DefaultRouter()
router.register(
    r'reports',
    ReportViewSet,
    basename='reports'
)
from django.urls import include, path
from . import views
from .views import (
    ReportListView,
    ReportCreateView,
    ReportUpdateView,
    ReportDeleteView,
    ReportUpdateStatusView,
    CustomLoginView,
    CustomLogoutView
)

urlpatterns = [
    # Auth Web HTML
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),

    # Utama Web HTML
    path('', ReportListView.as_view(), name='report_list'),
    path('add/', ReportCreateView.as_view(), name='add_report'),
    path('update/<int:pk>/', ReportUpdateView.as_view(), name='update_report'),
    path('delete/<int:pk>/', ReportDeleteView.as_view(), name='delete_report'),
    path('update-status/<int:pk>/', ReportUpdateStatusView.as_view(), name='update_status'),
    path('api/detail/<int:pk>/', views.report_detail_api, name='detail_api'),
    path('search/', views.search_reports, name='search'),
    path(
        'api/',
        include(router.urls)
    ),
]