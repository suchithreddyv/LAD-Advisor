from django.db import models

# Create your models here.
class Student(models.Model):
    student_id = models.IntegerField(primary_key=True, db_column='student_id')
    student_name = models.CharField(max_length=100, db_column='StudentName')

    # Meta class to specify the existing table name
    class Meta:
        db_table = 'Students'  # Specifies the name of the table in your MySQL database

    def __str__(self):
        return f"ID: {self.student_id}, Name: {self.student_name}"
    
class Course(models.Model):
    course_id = models.IntegerField(primary_key=True)
    course_name = models.CharField(max_length=255)

    class Meta:
        db_table = 'Course'

    def __str__(self):
        return f"{self.course_name} ({self.course_id})"
    
class WeeklyGrade(models.Model):
    GradeID = models.AutoField(primary_key=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE,db_column='student_id')
    course = models.ForeignKey(Course, on_delete=models.CASCADE,db_column='course_id')
    WeekNumber = models.CharField(max_length=100)
    PercentileGrade = models.CharField(max_length=255)
    AlphabetGrade = models.CharField(max_length=50)
    categorized_assignment_grades = models.JSONField(default=dict)

    class Meta:
        db_table = 'WeeklyGrades'

