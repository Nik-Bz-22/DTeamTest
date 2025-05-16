# main/views.py
from django.views.generic import ListView, DetailView
from .models import CV


class CVListView(ListView):
    model = CV
    template_name = "templates/main/cv_list.html"
    context_object_name = "cvs"


class CVDetailView(DetailView):
    model = CV
    template_name = "main/cv_detail.html"
    context_object_name = "cv"
