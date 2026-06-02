from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from .models import Report
from .forms import ReportForm
from django.views import View
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.views.generic import CreateView
from django.contrib.auth import get_user_model
from django.contrib.auth.views import LoginView, LogoutView



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


User = get_user_model()
class AdminRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_admin:
            messages.error(request, "Akses Ditolak")
            return redirect('report_list')
        return super().dispatch(request, *args, **kwargs)


# LIST (semua boleh akses)
class ReportListView(ListView):
    model = Report
    template_name = 'main_app/home.html'
    context_object_name = 'reports'


# DETAIL (semua boleh akses)
class ReportDetailView(DetailView):
    model = Report
    template_name = 'main_app/detail.html'


# CREATE (ADMIN ONLY)
class ReportCreateView(CreateView):
    model = Report
    form_class = ReportForm
    template_name = 'main_app/add_report.html'
    success_url = reverse_lazy('report_list')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or not getattr(request.user, 'is_admin', False):
            messages.error(request, "Akses Ditolak")
            return redirect('report_list')
        return super().dispatch(request, *args, **kwargs)


# UPDATE (ADMIN ONLY)
class ReportUpdateView(AdminRequiredMixin, UpdateView):
    model = Report
    form_class = ReportForm
    template_name = 'main_app/update_report.html'
    success_url = reverse_lazy('report_list')

    def form_valid(self, form):
        messages.success(self.request, "Laporan berhasil diperbarui")
        return super().form_valid(form)


# DELETE (ADMIN ONLY)
class ReportDeleteView(AdminRequiredMixin, DeleteView):
    model = Report
    template_name = 'main_app/delete_confirm.html'
    success_url = reverse_lazy('report_list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Laporan berhasil dihapus")
        return super().delete(request, *args, **kwargs)


# WORKFLOW STATUS (ADMIN ONLY)
class ReportUpdateStatusView(View):
    def post(self, request, pk):
        if not request.user.is_authenticated or not request.user.is_admin:
            messages.error(request, "Akses Ditolak")
            return redirect('report_list')

        report = get_object_or_404(Report, pk=pk)
        new_status = request.POST.get('status')

        if new_status in ['VERIFIED', 'IN_PROGRESS', 'RESOLVED']:
            report.status = new_status
            report.save()
            messages.success(request, "Status berhasil diperbarui")

        return redirect('report_list')
    