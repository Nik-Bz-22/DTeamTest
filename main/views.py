from django.forms import model_to_dict
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, DetailView
from django.shortcuts import get_object_or_404, render, redirect
from .models import CV
from tools.pdf_generator import generate_pdf
from tools.email_validator import is_valid_email
from main.constants import SKILLS_LIMIT, BIO_CHAR_LIMIT
from rest_framework.viewsets import ModelViewSet
from .serializers import CVSerializer
from main.tasks.send_cv_email_pdf import send_cv_pdf_email


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


def settings_view(request):
    return render(request, "main/settings.html")


@csrf_exempt
def send_cv_email(request, pk):
    if request.method == "POST":
        email = request.POST.get("email")
        if not is_valid_email(email):
            return HttpResponse(content="Invalid email address.", status=400)

        cv = CV.objects.get(pk=pk)
        context = {"cv": model_to_dict(cv)}
        send_cv_pdf_email.delay("main/cv_pdf.html", context, email)
        return redirect("cv_detail", pk=pk)
    return HttpResponse(content="Invalid request method.", status=400)
