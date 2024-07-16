import os
from daphne.cli import CommandLineInterface

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'therapist_chat.settings')

CommandLineInterface().run(
    argv=[
        "daphne",
        "therapist_chat.routing:application",
        "--bind", "0.0.0.0",
        "--port", "8001",  # Port for Daphne to serve ASGI
    ]
)