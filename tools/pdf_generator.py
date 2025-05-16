from django.template.loader import get_template
from weasyprint import HTML


def generate_pdf(template_path, context):
    template = get_template(template_path)
    html = template.render(context)
    pdf_file = HTML(string=html).write_pdf()
    return pdf_file
