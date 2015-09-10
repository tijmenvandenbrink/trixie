from django.shortcuts import render


def reports_list(request):
    return render(request, 'reports.html', {"active": "reports"})

