# main/tests.py
from django.test import TestCase
from django.urls import reverse
from .models import CV, Contact


class CVViewsTestCase(TestCase):
    def setUp(self):
        self.cv = CV.objects.create(
            firstname="John",
            lastname="Doe",
            skills="Python, Django",
            projects="Portfolio",
            bio="Experienced developer",
        )
        Contact.objects.create(cv=self.cv, type="EMAIL", value="john.doe@example.com")

    def test_cv_list_view(self):
        response = self.client.get(reverse("cv_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "John Doe")

    def test_cv_detail_view(self):
        response = self.client.get(reverse("cv_detail", args=[self.cv.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Python, Django")
        self.assertContains(response, "john.doe@example.com")
