from rest_framework import serializers
from .models import Report

class ReportSerializer(serializers.ModelSerializer):
    is_owner = serializers.SerializerMethodField()
    reporter_name = serializers.SerializerMethodField()

    class Meta:
        model = Report
        fields = [
            'id',
            'title',
            'description',
            'status',
            'reporter_name',
            'is_owner',
            'updated_at'
        ]

    def get_is_owner(self, obj):
        request = self.context.get('request')

        if request and request.user.is_authenticated:
            return obj.reporter == request.user

        return False

    def get_reporter_name(self, obj):
        request = self.context.get('request')
        tab = request.query_params.get('tab') if request else None

        if tab == 'feed':
            return "Warga Anonim"

        return obj.reporter.username if obj.reporter else "Warga Anonim"