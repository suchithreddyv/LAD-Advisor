from django_q.tasks import schedule
from django_q.models import Schedule
import django.utils.timezone as timezone
from datetime import timedelta

def ensure_unique_schedule(func_name, schedule_type, **kwargs):
    # Prepare a string representation of the kwargs to store in the Schedule
    kwargs_str = str(kwargs.get('kwargs', '{}'))
    
    # Check for existing scheduled task with the same function, schedule type, and parameters
    existing_task = Schedule.objects.filter(
        func=func_name,
        schedule_type=schedule_type,
        # Check if kwargs match. Note: This relies on consistent string representation.
        kwargs=kwargs_str
    )

    if not existing_task.exists():
        # If no existing task matches, schedule a new one
        schedule(func=func_name, schedule_type=schedule_type, **kwargs)
        print(f"Scheduled new task: {func_name}")
    else:
        print(f"Task already scheduled: {func_name}")

def start():
    task_path = 'testApp.views.update_all_students_grades'
    # Calculate the next Sunday from now
    next_sunday = timezone.now() + timedelta(days=((6 - timezone.now().weekday()) % 7))
    task_schedule_type = Schedule.WEEKLY
    task_kwargs = {
        'repeats': 0,  # Set to 0 for no repetition
        'next_run': next_sunday,  # Next Sunday
        'kwargs': '{}'
    }
    
    ensure_unique_schedule(task_path, task_schedule_type, **task_kwargs)

from datetime import datetime, time
import time
import logging
from apscheduler.schedulers.background import BackgroundScheduler
from django.conf import settings
from testApp.views import update_all_students_grades

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def start():
    logger.info("Starting the scheduler.")
    scheduler = BackgroundScheduler(timezone=settings.TIME_ZONE)

    # Adding a job to the scheduler
    scheduler.add_job(
        update_all_students_grades,
        'cron',
        day_of_week='sun',
        hour=23,
        minute=59,
        id='update_grades_weekly',
        next_run_time=datetime.now()  # Optionally start immediately
    )
    logger.info("Added job: update_all_students_grades, to run every 10 minutes.")

    # Starting the scheduler
    scheduler.start()
    logger.info("Scheduler started.")

    # This is required to keep the main thread alive.
    try:
        while True:
            time.sleep(2)
    except (KeyboardInterrupt, SystemExit):
        # Not strictly necessary if shutting down on Ctrl+C, but should be done if shutdown must be clean
        scheduler.shutdown()
        logger.info("Scheduler shut down.")
