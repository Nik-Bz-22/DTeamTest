from django.http import HttpResponse
from django.views.generic import ListView, DetailView
from django.shortcuts import get_object_or_404
from .models import CV
from tools.pdf_generator import generate_pdf
from main.constants import SKILLS_LIMIT, BIO_CHAR_LIMIT
from rest_framework.viewsets import ModelViewSet
from .serializers import CVSerializer


class CVListView(ListView):
    model = CV
    template_name = "templates/main/cv_list.html"
    context_object_name = "cvs"

    # limit the skills to the first three and shorten bio
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        for cv in context["cvs"]:
            cv.skills_preview = cv.skills.all()[:SKILLS_LIMIT]
            cv.skills_count = cv.skills.count()
            cv.skills_count_remaining = cv.skills_count - SKILLS_LIMIT
            cv.bio_preview = (
                cv.bio[:BIO_CHAR_LIMIT] + "..."
                if len(cv.bio) > BIO_CHAR_LIMIT
                else cv.bio
            )
        return context


class CVDetailView(DetailView):
    model = CV
    template_name = "main/cv_detail.html"
    context_object_name = "cv"


def download_cv_pdf(request, pk):
    cv = get_object_or_404(CV, pk=pk)
    context = {"cv": cv}
    pdf_file = generate_pdf("main/cv_pdf.html", context)
    response = HttpResponse(pdf_file, content_type="application/pdf")
    response["Content-Disposition"] = (
        f'attachment; filename="{cv.firstname}_{cv.lastname}_CV.pdf"'
    )
    return response


class CVViewSet(ModelViewSet):
    queryset = CV.objects.all()
    serializer_class = CVSerializer
