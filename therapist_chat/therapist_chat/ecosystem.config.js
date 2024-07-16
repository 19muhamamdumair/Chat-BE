module.exports = {
    apps: [
      {
        name: "chat-app-daphne",
        script: "venv/bin/python",
        args: "daphne_config.py",
        interpreter: "none"
      },
      {
        name: "chat-app-gunicorn",
        script: "venv/bin/gunicorn",
        args: "therapist_chat.wsgi:application -b 0.0.0.0:8000"
      }
    ]
  };