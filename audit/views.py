from django.shortcuts import render
from .models import RequestLog


def recent_requests_view(request):
    logs = RequestLog.objects.order_by("-timestamp")[:10]
    return render(request, "audit/recent_requests.html", {"logs": logs})
