from django.db import models
from main.constants import ContactsTypeEnum


class CV(models.Model):
    firstname = models.CharField(max_length=40, null=False, blank=False)
    lastname = models.CharField(max_length=40, null=False, blank=False)
    projects = models.TextField()
    bio = models.TextField()

    def __str__(self):
        return f"{self.firstname} {self.lastname}: {self.bio[:20]}..."


class Contact(models.Model):
    cv = models.ForeignKey(CV, on_delete=models.CASCADE, related_name="contacts")
    type = models.CharField(
        max_length=50, choices=[(tag, tag.value) for tag in ContactsTypeEnum]
    )
    value = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.type}: {self.value}"


class Skill(models.Model):
    cv = models.ForeignKey(CV, on_delete=models.CASCADE, related_name="skills")
    name = models.CharField(max_length=100)
    level = models.SmallIntegerField(choices=[(i, i) for i in range(1, 6)])

    def __str__(self):
        return f"{self.name}: {self.level}"
