# seed_data.py

import os
import django
from django.utils import timezone
from faker import Faker

# Set up Django environment
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "therapist_chat.settings")
# django.setup()

# Now you can import your models and start using Django ORM
from chat.models import Conversation, Message, UserProfile
from django.contrib.auth.models import User

# Initialize Faker generator
fake = Faker()

# Define functions to create sample data
def create_users(num_therapists, num_parents):
    therapists = []
    parents = []
    
    for _ in range(num_therapists):
        therapist_username = fake.user_name()
        therapist = User.objects.create_user(username=therapist_username, password='password', email=f'{therapist_username}@example.com')
        UserProfile.objects.create(user=therapist, role='therapist')
        therapists.append(therapist)
    
    for _ in range(num_parents):
        parent_username = fake.user_name()
        parent = User.objects.create_user(username=parent_username, password='password', email=f'{parent_username}@example.com')
        UserProfile.objects.create(user=parent, role='parent')
        parents.append(parent)
    
    return therapists, parents

def create_conversations(therapist, parent):
    conversation1 = Conversation.objects.create(therapist=therapist, parent=parent, status=1)
    conversation2 = Conversation.objects.create(therapist=therapist, parent=parent, status=4)
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
    num_therapists = 4
    num_parents = 4
    
    therapists, parents = create_users(num_therapists, num_parents)
    
    for therapist in therapists:
        for parent in parents:
            conversation1, conversation2 = create_conversations(therapist, parent)
            create_messages(conversation1)
            create_messages(conversation2)

    print("Sample data generated successfully.")

if __name__ == "__main__":
    main()
