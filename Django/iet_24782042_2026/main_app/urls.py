from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path('', ReportListView.as_view(), name='report_list'),
    path('add/', ReportCreateView.as_view(), name='add_report'),
    path('update/<int:pk>/', ReportUpdateView.as_view(), name='update_report'),
    path('delete/<int:pk>/', ReportDeleteView.as_view(), name='delete_report'),
    path('detail/<int:pk>/', ReportDetailView.as_view(), name='report_detail'),
    path('update-status/<int:pk>/', views.ReportUpdateStatusView.as_view(), name='update_status'),
]