from django.http import JsonResponse
from main_app.models import Report
from django.db.models import Count
from django.shortcuts import render
from django.http import JsonResponse
from main_app.models import Report  # sesuaikan kalau nama model beda

def status_chart(request):
    data = Report.objects.values('status').order_by('-id').distinct('status')

    result = {}
    for item in data:
        status = item['status']
        result[status] = result.get(status, 0) + 1

    return JsonResponse(result)

def dashboard_view(request):
    return render(request, 'dashboard/index.html')

# 📊 status chart
def status_chart(request):
    data = Report.objects.values('status').annotate(total=Count('id'))
    return JsonResponse(list(data), safe=False)

# 📊 kategori chart
def kategori_chart(request):
    data = Report.objects.values('category').annotate(total=Count('id'))
    return JsonResponse(list(data), safe=False)

# 📋 last reports
def last_reports(request):
    reported = Report.objects.filter(status='REPORTED').order_by('-id')[:5]
    resolved = Report.objects.filter(status='RESOLVED').order_by('-id')[:5]

    data = {
        "reported": list(reported.values()),
        "resolved": list(resolved.values())
    }
    return JsonResponse(data)