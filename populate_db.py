import os
import django
from faker import Faker
import random

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'event_management.settings')
django.setup()

from events.models import Category, Event, Participant

def populate_db():
    # Clear existing data
    Participant.objects.all().delete()
    Event.objects.all().delete()
    Category.objects.all().delete()

    fake = Faker()

    # Fixed categories
    category_names = [
        ("Educational", "Events related to education and learning."),
        ("Cultural", "Events celebrating culture and traditions."),
        ("Business", "Corporate and business-related events."),
        ("Social", "Social gatherings and community events."),
        ("Sports", "Sports and athletic events."),
    ]

    categories = []
    for name, desc in category_names:
        cat = Category.objects.create(name=name, description=desc)
        categories.append(cat)
    print(f"Created {len(categories)} fixed categories.")

    # Create Events
    events = []
    for _ in range(20):
        event = Event.objects.create(
            name=fake.catch_phrase(),
            description=fake.text(),
            date=fake.date_between(start_date='-10d', end_date='+10d'),
            time=fake.time(),
            location=fake.city(),
            category=random.choice(categories)
        )
        events.append(event)
    print(f"Created {len(events)} events.")

    # Create Participants and assign random events
    total_participants = 30
    for _ in range(total_participants):
        participant = Participant.objects.create(
            name=fake.name(),
            email=fake.unique.email()
        )
        participant.events.set(random.sample(events, random.randint(1, 3)))

    print(f"Created {total_participants} participants.")
    print("Database populated successfully!")

if __name__ == '__main__':
    populate_db()
