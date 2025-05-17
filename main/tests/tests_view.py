from django.test import TestCase
from django.urls import reverse
from main.models import CV, Contact, Skill


class CVViewsTestCase(TestCase):
    def setUp(self):
        # Create the CV instance
        self.cv = CV.objects.create(
            firstname="John",
            lastname="Doe",
            projects="Portfolio",
            bio="Experienced developer",
        )

        # Create related Contact and Skill instances
        Contact.objects.create(cv=self.cv, type="email", value="john.doe@example.com")
        Skill.objects.create(cv=self.cv, name="Python", level=5)

    def test_cv_list_view(self):
        response = self.client.get(reverse("cv_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "John Doe")

    def test_cv_detail_view(self):
        response = self.client.get(reverse("cv_detail", args=[self.cv.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Portfolio")
        self.assertContains(response, "john.doe@example.com")
