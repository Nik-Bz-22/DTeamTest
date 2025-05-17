from django.urls import path
from .views import (
    CVListView,
    CVDetailView,
    download_cv_pdf,
    CVViewSet,
    settings_view,
    send_cv_email,
)
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r"cvs", CVViewSet, basename="cv")

urlpatterns = [
    path("", CVListView.as_view(), name="cv_list"),
    path("cv/<int:pk>/", CVDetailView.as_view(), name="cv_detail"),
    path("cv/<int:pk>/download/", download_cv_pdf, name="download_cv_pdf"),
    path("settings/", settings_view, name="settings"),
    path("send_cv_email/<int:pk>/", send_cv_email, name="send_cv_email"),
] + router.urls
