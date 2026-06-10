from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from .models import Report
from .forms import ReportForm
from django.views import View
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied

# REST Framework Imports
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied as DRFPermissionDenied
from django.db.models import Q
from .permissions import IsCitizenOwnerOrAdminReadOnlyStatus
from .serializers import ReportSerializer
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from .models import Report


User = get_user_model()

# =====================================================================
# 1. MIXINS & AUTHENTICATION (WEB HTML)
# =====================================================================

# Mixin khusus Web HTML: Memastikan hanya Admin (Superuser) yang bisa masuk
class AdminRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or not getattr(request.user, 'is_superuser', False):
            messages.error(request, "Akses Ditolak: Khusus Admin")
            return redirect('report_list')
        return super().dispatch(request, *args, **kwargs)


class CustomLoginView(LoginView):
    template_name = 'login.html'

    def form_valid(self, form):
        messages.success(self.request, "Login berhasil")
        return super().form_valid(form)


class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('login')

    def dispatch(self, request, *args, **kwargs):
        messages.success(request, "Logout berhasil")
        return super().dispatch(request, *args, **kwargs)


# =====================================================================
# 2. VIEW UTAMA (WEB HTML) - DISESUAIKAN DENGAN ATURAN PAPAN TULIS
# =====================================================================

# LIST (Semua user yang login boleh melihat, filter disamakan dengan API)
class ReportListView(ListView):
    model = Report
    template_name = 'main_app/home.html'
    context_object_name = 'reports'

    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated:
            return Report.objects.none()
        if user.is_superuser:
            return Report.objects.exclude(status='DRAFT')
        return Report.objects.filter(Q(reporter=user) | ~Q(status='DRAFT'))


# DETAIL
class ReportDetailView(DetailView):
    model = Report
    template_name = 'main_app/detail.html'


# CREATE (HANYA UNTUK CITIZEN - ADMIN DIBLOKIR)
class ReportCreateView(CreateView):
    model = Report
    form_class = ReportForm
    template_name = 'main_app/add_report.html'
    success_url = reverse_lazy('report_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def dispatch(self, request, *args, **kwargs):
        # Jika Admin (Superuser) mencoba membuat laporan di web, TOLAK!
        if request.user.is_authenticated and request.user.is_superuser:
            messages.error(request, "Admin tidak diperbolehkan membuat laporan.")
            return redirect('report_list')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.reporter = self.request.user
        messages.success(self.request, "Laporan berhasil dibuat")
        return super().form_valid(form)


# UPDATE (ADMIN BISA AKSES, CITIZEN CUMA BISA EDIT LAPORANNYA SENDIRI)
class ReportUpdateView(UpdateView):
    model = Report
    form_class = ReportForm
    template_name = 'main_app/update_report.html'
    success_url = reverse_lazy('report_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
            
        obj = self.get_object()
        
        # JIKA YANG MASUK BUKAN ADMIN, MAKA DIA HARUS SI PEMILIK LAPORAN
        if not request.user.is_superuser and obj.reporter != request.user:
            messages.error(request, "Akses Ditolak: Anda hanya boleh mengedit laporan milik sendiri.")
            return redirect('report_list')
            
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        messages.success(self.request, "Laporan berhasil diperbarui")
        return super().form_valid(form)


# DELETE (ADMIN TIDAK BOLEH - CITIZEN HANYA BOLEH HAPUS LAPORAN SENDIRI)
class ReportDeleteView(DeleteView):
    model = Report
    template_name = 'main_app/delete_confirm.html'
    success_url = reverse_lazy('report_list')

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if request.user.is_superuser:
            messages.error(request, "Admin tidak diperbolehkan menghapus laporan.")
            return redirect('report_list')
        if obj.reporter != request.user:
            messages.error(request, "Anda hanya boleh menghapus laporan milik sendiri.")
            return redirect('report_list')
        return super().dispatch(request, *args, **kwargs)


# WORKFLOW STATUS (ADMIN ONLY)
class ReportUpdateStatusView(AdminRequiredMixin, View):
    def post(self, request, pk):
        report = get_object_or_404(Report, pk=pk)
        new_status = request.POST.get('status')

        if new_status in ['VERIFIED', 'IN_PROGRESS', 'RESOLVED', 'DONE']:
            report.status = new_status
            report.save()
            messages.success(request, "Status berhasil diperbarui")
        return redirect('report_list')


class ReportPagination(PageNumberPagination):

    page_size = 10
    page_size_query_param = 'page_size'

    def get_paginated_response(self, data):

        return Response({
            'count': self.page.paginator.count,
            'current_page': self.page.number,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'results': data
        })


class ReportViewSet(viewsets.ModelViewSet):
    serializer_class = ReportSerializer
    pagination_class = ReportPagination
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        queryset = Report.objects.all().order_by('-updated_at')
        tab = self.request.query_params.get('tab')

        user = self.request.user

        # MY REPORTS
        if tab == 'my_reports':
            if user.is_authenticated:
                return queryset.filter(reporter=user)
            return queryset.none()

        # FEED
        if tab == 'feed':
            feed_queryset = queryset.exclude(status='DRAFT')

            if user.is_authenticated:
                return feed_queryset.exclude(reporter=user)

            return feed_queryset

        # DEFAULT (fallback aman)
        return queryset

    def perform_create(self, serializer):
        if self.request.user.is_authenticated:
            serializer.save(reporter=self.request.user)
        else:
            serializer.save(reporter=None)

# =====================================================================
# 4. KODE LAMA FUNGSIONAL (AGAR URLS.PY TIDAK EROR)
# =====================================================================

def detail_report(request, id):
    d = Report.objects.get(id=id)
    return JsonResponse({
        'title': d.title,
        'status': d.status,
        'description': d.description
    })

def search_reports(request):
    query = request.GET.get('q', '')
    reports = Report.objects.filter(title__icontains=query)
    data = {
        'results': [
            {'id': r.id, 'title': r.title}
            for r in reports
        ]
    }
    return JsonResponse(data)

def report_detail_api(request, pk):
    report = Report.objects.get(pk=pk)
    data = {
        "title": report.title,
        "description": report.description,
        "location": report.location,
        "status": report.status
    }
    return JsonResponse(data)


