# Generated by Django 4.1.1 on 2024-03-28 18:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Course",
            fields=[
                ("course_id", models.IntegerField(primary_key=True, serialize=False)),
                ("course_name", models.CharField(max_length=255)),
            ],
            options={"db_table": "Course",},
        ),
        migrations.CreateModel(
            name="Student",
            fields=[
                (
                    "student_id",
                    models.IntegerField(
                        db_column="student_id", primary_key=True, serialize=False
                    ),
                ),
                (
                    "student_name",
                    models.CharField(db_column="StudentName", max_length=100),
                ),
            ],
            options={"db_table": "Students",},
        ),
        migrations.CreateModel(
            name="WeeklyGrade",
            fields=[
                ("GradeID", models.AutoField(primary_key=True, serialize=False)),
                ("WeekNumber", models.CharField(max_length=100)),
                ("PercentileGrade", models.CharField(max_length=255)),
                ("AlphabetGrade", models.CharField(max_length=50)),
                ("categorized_assignment_grades", models.JSONField(default=dict)),
                (
                    "course",
                    models.ForeignKey(
                        db_column="course_id",
                        on_delete=django.db.models.deletion.CASCADE,
                        to="testApp.course",
                    ),
                ),
                (
                    "student",
                    models.ForeignKey(
                        db_column="student_id",
                        on_delete=django.db.models.deletion.CASCADE,
                        to="testApp.student",
                    ),
                ),
            ],
            options={"db_table": "WeeklyGrades",},
        ),
    ]
