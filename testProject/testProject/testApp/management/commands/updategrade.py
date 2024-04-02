from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from testApp.models import Student, Course
from testApp.views import update_student_grades  # Adjust the import path as necessary

class Command(BaseCommand):
    help = 'Updates student grades every 3 minutes from the start date'

    def handle(self, *args, **options):
        start_date = timezone.datetime(2024, 2, 1)  # Adjust start date as needed
        now = timezone.now()

        if now >= start_date:
            # Example: iterate over all students and courses to update grades
            # Adjust the logic to fit your specific requirements
            for student in Student.objects.all():
                for course in Course.objects.all():
                    # Here, you'd call update_student_grades for each student-course pair
                    # Make sure to adjust update_student_grades to work without specific args
                    update_student_grades(course.course_id, student.student_name, course.course_name,student.student_id)
            
            self.stdout.write(self.style.SUCCESS('Successfully updated student grades'))

