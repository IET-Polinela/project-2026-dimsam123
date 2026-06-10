from django import forms
from .models import Report

class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        # Ambil informasi user yang sedang mengakses form ini
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        # JIKA YANG BUKA HALAMAN ADALAH ADMIN
        if user and user.is_superuser:
            # Kunci mati semua field teks, sisakan HANYA field status yang bisa diubah!
            for field_name in self.fields:
                if field_name != 'status':
                    self.fields[field_name].disabled = True