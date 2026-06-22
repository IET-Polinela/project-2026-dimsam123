from rest_framework import viewsets, permissions
from .models import Report
from .serializers import ReportSerializer

class ReportViewSet(viewsets.ModelViewSet):
    # Mengizinkan siapa saja untuk mengakses (sesuai instruksi lab)
    permission_classes = [permissions.AllowAny]
    queryset = Report.objects.all()
    serializer_class = ReportSerializer


class ReportViewSet(viewsets.ModelViewSet):
    serializer_class = ReportSerializer

    def get_queryset(self):
        if self.request.user.is_authenticated and self.request.user.is_staff:
            return Report.objects.exclude(status='DRAFT')
        # Jika bukan admin, tampilkan semua (atau sesuaikan logika lainnya)
        return Report.objects.all()