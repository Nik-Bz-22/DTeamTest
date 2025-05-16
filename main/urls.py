from django.urls import path
from .views import CVListView, CVDetailView, download_cv_pdf

urlpatterns = [
    path("", CVListView.as_view(), name="cv_list"),
    path("cv/<int:pk>/", CVDetailView.as_view(), name="cv_detail"),
    path("cv/<int:pk>/download/", download_cv_pdf, name="download_cv_pdf"),
]
