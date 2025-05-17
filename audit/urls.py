from django.urls import path

from .views import recent_requests_view

urlpatterns = [
    path("logs/", recent_requests_view, name="recent_requests"),
]
