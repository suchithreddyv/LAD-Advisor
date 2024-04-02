from django.apps import AppConfig

class TestappConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "testApp"

    def ready(self):
        from . import scheduler  # Assuming you create a scheduler.py for your scheduling logic
        scheduler.start()  # Call the start function to schedule your tasks
