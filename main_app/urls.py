from django.urls import path
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

    # 🔥 API Detail yang dipakai oleh Javascript/AJAX di Web HTML kamu
    path('api/detail/<int:pk>/', views.report_detail_api, name='detail_api'),

    # 🔍 Search Feature yang dipakai di Web HTML kamu
    path('search/', views.search_reports, name='search'),
]