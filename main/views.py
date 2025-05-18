from django.forms import model_to_dict
from django.http import HttpResponse
from django.views.generic import ListView, DetailView, View
from django.shortcuts import get_object_or_404, render, redirect
from .models import CV
from tools.pdf_generator import generate_pdf
from tools.email_validator import is_valid_email
from main.constants import SKILLS_LIMIT, BIO_CHAR_LIMIT
from rest_framework.viewsets import ModelViewSet
from .serializers import CVSerializer
from main.tasks.send_cv_email_pdf import send_cv_pdf_email
from tools.ai_translate import ai_translate
import logging

logger = logging.getLogger(__name__)


# Helper function to fetch CV with related fields
def get_cv_with_related(pk):
    return get_object_or_404(CV.objects.prefetch_related("skills", "contacts"), pk=pk)


class CVListView(ListView):
    model = CV
    template_name = "templates/main/cv_list.html"
    context_object_name = "cvs"

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["contacts"] = self.object.contacts.all()
        context["skills"] = self.object.skills.all()
        return context


def download_cv_pdf(request, pk):
    cv = get_cv_with_related(pk)
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


def settings_view(request):
    return render(request, "main/settings.html")


class SendCVEmailView(View):
    def post(self, request, pk):
        email = request.POST.get("email")
        if not is_valid_email(email):
            return HttpResponse(content="Invalid email address.", status=400)

        cv = get_cv_with_related(pk)
        cv_dict = model_to_dict(cv)
        cv_dict["skills"] = list(cv.skills.values("name", "level"))
        cv_dict["contacts"] = list(cv.contacts.values("type", "value"))
        context = {"cv": cv_dict}
        send_cv_pdf_email.delay("main/cv_pdf.html", context, email)
        return redirect("cv_detail", pk=pk)


class TranslateCVView(View):
    def get(self, request, pk):
        cv = get_cv_with_related(pk)
        language = request.GET.get("language")
        if not language:
            return HttpResponse(content="Language not specified.", status=400)

        cv_dict = model_to_dict(cv)
        cv_dict["skills"] = list(cv.skills.values("name", "level"))
        cv_dict["contacts"] = list(cv.contacts.values("type", "value"))

        try:
            translated_cv = ai_translate(cv_dict, language)
            if not translated_cv:
                raise ValueError("Translation failed.")
        except Exception as e:
            logger.error(f"Translation error: {e}")
            return HttpResponse(content="Translation failed.", status=500)

        context = {"cv": translated_cv}
        return render(request, "main/cv_detail.html", context)
