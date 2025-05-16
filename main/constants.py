from enum import Enum


class ContactsTypeEnum(Enum):
    EMAIL = "email"
    PHONE = "phone"
    LINKEDIN = "linkedin"
    GITHUB = "github"
    WEBSITE = "website"


SKILLS_LIMIT = 3
BIO_CHAR_LIMIT = 100
