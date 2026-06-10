from rest_framework import permissions

class IsCitizenOwnerOrAdminReadOnlyStatus(permissions.BasePermission):
    def has_permission(self, request, view):
        # Admin dilarang keras menembak POST (Create laporan) via API
        if request.method == 'POST' and request.user.is_superuser:
            return False
        return True

    def has_object_permission(self, request, view, obj):
        # 1. Jika pengguna adalah Admin (Superuser)
        if request.user.is_superuser:
            # Admin hanya boleh mengedit (PUT/PATCH), tidak boleh DELETE atau GET jika DRAFT
            if request.method == 'DELETE':
                return False
            return True

        # 2. Jika pengguna adalah Citizen (Warga)
        # Citizen hanya boleh mengutak-atik laporan milik dirinya sendiri
        return obj.reporter == request.user