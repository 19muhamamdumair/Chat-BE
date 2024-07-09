# seed_data.py

import os
import django
from django.utils import timezone
from faker import Faker
from therapist_chat.settings import *  # Adjust this import based on your actual settings module

# Set up Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "therapist_chat.settings")
django.setup()

# Now you can import your models and start using Django ORM
from chat.models import Conversation, Message
from django.contrib.auth.models import User

# Initialize Faker generator
fake = Faker()

# Define functions to create sample data
def create_users():
    therapist_username = fake.user_name()  # Generates a unique username
    parent_username = fake.user_name()  # Generates another unique username
    
    therapist = User.objects.create_user(username=therapist_username, password='password', email='therapist@example.com')
    parent = User.objects.create_user(username=parent_username, password='password', email='parent@example.com')
    
    return therapist, parent

def create_conversations(therapist, parent):
    conversation1 = Conversation.objects.create(therapist=therapist, parent=parent, status='active')
    conversation2 = Conversation.objects.create(therapist=therapist, parent=parent, status='closed')
    return conversation1, conversation2

def create_messages(conversation):
    sender = conversation.therapist  # For example, messages are sent by therapist
    for _ in range(5):
        Message.objects.create(
            conversation=conversation,
            sender=sender,
            content=fake.text(),
            file=None,  # Replace with actual file if needed
        )

def main():
    therapist, parent = create_users()
    conversation1, conversation2 = create_conversations(therapist, parent)
    create_messages(conversation1)
    create_messages(conversation2)

    print("Sample data generated successfully.")

if __name__ == "__main__":
    main()
