import os
import sys
from datetime import datetime
from pathlib import Path
from random import choice

import django
from django.conf import settings

DJANGO_BASE_DIR = Path(__file__).parent.parent
NUMBER_OF_OBJECTS = 1000

sys.path.append(str(DJANGO_BASE_DIR))
os.environ['DJANGO_SETTINGS_MODULE'] = 'project.settings'
settings.USE_TZ = False

django.setup()

if __name__ == '__main__':
    import faker
    
    from contact.models import Category, Contact
    
    fake = faker.Faker('pt_BR')
    categories = ['Friends', 'Family', 'Coworkers', 'Enemies']
    
    django_categories: list[Category] = []
    
    for name in categories:
        django_categories.append(Category(name=name))
        
    for category in django_categories:
        category.save()
        
    django_contacts: list[Contact] = []
    
    for _ in range(NUMBER_OF_OBJECTS):
        profile = fake.profile()
        first_name, last_name = profile['name'].split(' ', 1)
        phone = fake.phone_number()
        email = profile['mail']
        created_date: datetime = fake.date()
        description = fake.text(max_nb_chars=100)
        category = choice(django_categories)
        django_contacts.append(
            Contact(
                first_name = first_name,
                last_name = last_name,
                phone = phone,
                email = email,
                created_date = created_date,
                description = description,
                category = category,
            )
        )
    
    if len(django_contacts) > 0:
        Contact.objects.bulk_create(django_contacts)
        