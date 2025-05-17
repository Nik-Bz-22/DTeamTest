from rest_framework import serializers
from .models import CV, Contact, Skill


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ["name", "level"]


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ["type", "value"]


class CVSerializer(serializers.ModelSerializer):
    contacts = ContactSerializer(many=True)
    skills = SkillSerializer(many=True)

    class Meta:
        model = CV
        fields = [
            "id",
            "firstname",
            "lastname",
            "projects",
            "bio",
            "contacts",
            "skills",
        ]
        read_only_fields = ["id"]

    def create(self, validated_data):
        contacts_data = validated_data.pop("contacts", [])
        skills_data = validated_data.pop("skills", [])
        cv = CV.objects.create(**validated_data)

        for contact_data in contacts_data:
            Contact.objects.create(cv=cv, **contact_data)

        for skill_data in skills_data:
            Skill.objects.create(cv=cv, **skill_data)

        return cv

    def update(self, instance, validated_data):
        contacts_data = validated_data.pop("contacts", [])
        skills_data = validated_data.pop("skills", [])

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Update contacts
        instance.contacts.all().delete()
        for contact_data in contacts_data:
            Contact.objects.create(cv=instance, **contact_data)

        # Update skills
        instance.skills.all().delete()
        for skill_data in skills_data:
            Skill.objects.create(cv=instance, **skill_data)

        return instance
