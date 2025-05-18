from rest_framework.test import APITestCase
from rest_framework import status
from main.models import CV, Contact, Skill
from tools.ai_translate import ai_translate


class CVAPITestCase(APITestCase):
    def setUp(self):
        self.cv_data = {
            "firstname": "John",
            "lastname": "Doe",
            "projects": "Portfolio",
            "bio": "Experienced developer",
        }
        self.cv = CV.objects.create(**self.cv_data)

        self.contact_data = {"type": "EMAIL", "value": "john.doe@example.com"}
        self.skill_data = {"name": "Python", "level": 5}

        Contact.objects.create(cv=self.cv, **self.contact_data)
        Skill.objects.create(cv=self.cv, **self.skill_data)

        self.cv_url = f"/cvs/{self.cv.id}/"
        self.cv_list_url = "/cvs/"

    def test_create_cv(self):
        data = {
            "firstname": "Jane",
            "lastname": "Smith",
            "projects": "New Project",
            "bio": "Skilled developer",
            "contacts": [{"type": "email", "value": "jane.s.mith@example.com"}],
            "skills": [{"name": "Django", "level": 4}],
        }
        response = self.client.post(self.cv_list_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(CV.objects.count(), 2)
        self.assertEqual(Contact.objects.count(), 2)
        self.assertEqual(Skill.objects.count(), 2)

    def test_retrieve_cv(self):
        response = self.client.get(self.cv_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["firstname"], self.cv.firstname)
        self.assertEqual(len(response.data["contacts"]), 1)
        self.assertEqual(len(response.data["skills"]), 1)

    def test_update_cv(self):
        updated_data = {
            "firstname": "John",
            "contacts": [{"type": "email", "value": "updated.email@example.com"}],
            "skills": [
                {"name": "Python", "level": 4},
                {"name": "JavaScript", "level": 3},
            ],
        }
        response = self.client.patch(self.cv_url, updated_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.cv.refresh_from_db()
        self.assertEqual(self.cv.firstname, "John")
        self.assertEqual(Contact.objects.filter(cv=self.cv).count(), 1)
        self.assertTrue(
            Contact.objects.filter(value="updated.email@example.com").exists()
        )
        self.assertEqual(Skill.objects.filter(cv=self.cv).count(), 2)
        self.assertTrue(Skill.objects.filter(name="JavaScript").exists())

    def test_delete_cv(self):
        response = self.client.delete(self.cv_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(CV.objects.filter(id=self.cv.id).exists())
        self.assertEqual(Contact.objects.filter(cv=self.cv).count(), 0)
        self.assertEqual(Skill.objects.filter(cv=self.cv).count(), 0)


class ToolsTestCase(APITestCase):
    def test_ai_translate(self):
        json_data = {
            "id": 1,
            "firstname": "John",
            "lastname": "Doe",
            "projects": "Portfolio Site, API Service",
            "bio": "Senior backend developer with 5+ years of experience.",
            "skills": [{"name": "Python", "level": 5}, {"name": "Django", "level": 4}],
            "contacts": [
                {"type": "EMAIL", "value": "john.doe@example.com"},
                {"type": "LINKEDIN", "value": "https://linkedin.com/in/johndoe"},
            ],
        }

        target_language = "Spanish"
        translated_data = ai_translate(json_data, target_language)
        self.assertIsInstance(translated_data, dict)
        self.assertIn("firstname", translated_data)
        self.assertIn("lastname", translated_data)
        self.assertIn("projects", translated_data)
        self.assertIn("bio", translated_data)
        self.assertIn("skills", translated_data)
        self.assertIn("contacts", translated_data)
