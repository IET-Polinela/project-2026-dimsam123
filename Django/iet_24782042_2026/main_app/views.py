from django.shortcuts import get_object_or_404, redirect, render
from .models import Report
from .forms import ReportForm
from django.shortcuts import redirect

# Create your views here
def add_report(request):
    if request.method == "POST":
        form = ReportForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = ReportForm()
    return render(request, 'main_app/add_report.html', {'form': form})

def home(request):
    reports = Report.objects.all()
    return render(request, 'main_app/home.html', {'reports': reports})

def update_report(request, id):
    report = Report.objects.get(id=id)
    if request.method == "POST":
        form = ReportForm(request.POST, instance=report)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = ReportForm(instance=report)
    return render(request, 'main_app/update_report.html', {'form': form})

def delete_report(request, id):
    report = Report.objects.get(id=id)
    report.delete()
    return redirect('home')

def verify_report(request, id):
    report = get_object_or_404(Report, id=id)
    report.status = 'VERIFIED'
    report.save()
    return redirect('home')