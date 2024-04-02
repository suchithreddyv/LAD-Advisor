from django.http import HttpResponse,JsonResponse
from django.shortcuts import get_object_or_404, render
import requests,json,time,threading
from datetime import datetime, timedelta
from .models import *


# Global variable to store grades history
grades_history = []
# Create your views here.
def index(request):
    return render(request,'index.html')

def screen_1(request, course_id, course_name, student_name,user_id):
    return render(request, 'screen_1.html',{'students': student_name, 'course_id': course_id, 'course_name': course_name,'user_id':user_id})

def screen_2(request):
    return render(request, 'screen_2.html')

def screen_3(request):
    terms = ['Fall Semester 2023', 'Summer 2023', 'Spring Semester 2023', 'Spring Semester 2024']
    return render(request, 'screen_3.html', {'terms': terms})

def screen_4(request):
    term = request.GET.get('term', '')
    return render(request, 'screen_4.html', {'term': term})


def screen_5(request,term):
    api_url = "https://canvas.instructure.com/api/v1/"

    # Authentication headers (replace with your API token or OAuth)
    headers = {
        "Authorization": "Bearer 7~o1bbKk1sCwslpRjwUz2AjqlgDsFVUkvKvtKinsgx57pBhqkumaWQFomPAuKCsNpP"
    }

    # Extract subject and course_number from request parameters
    subject = request.GET.get('subject', '')
    course_number = request.GET.get('course_number', '')

    # Make the API call to retrieve courses
    response_courses = requests.get(f"{api_url}courses", headers=headers)

    if response_courses.status_code == 200:
        courses_data = response_courses.json()
        courses = []

        # Iterate through courses to retrieve instructor information
        for course in courses_data:
            course_id = course['id']
            # Make API call to retrieve enrollments for the course
            response_enrollments = requests.get(f"{api_url}courses/{course_id}/enrollments", headers=headers)
            if response_enrollments.status_code == 200:
                enrollments_data = response_enrollments.json()
                # Filter out teacher enrollments
                teacher_enrollments = [enrollment for enrollment in enrollments_data if enrollment['type'] == 'TeacherEnrollment']
                if teacher_enrollments:
                    instructor_name = teacher_enrollments[0]['user']['name']
                else:
                    instructor_name = "N/A"
            else:
                instructor_name = "N/A"

            # Filter courses based on subject or course number
            # Filter courses based on subject or course number
            if (not subject or subject.lower() in course['name'].lower()) and (not course_number or course_number.lower() in course['course_code'].lower()):
                # Construct course information dictionary
                course_info = {
                    'id': course_id,
                    'name': course['name'],
                    'course_code': course['course_code'],
                    'instructor': instructor_name
                }
                courses.append(course_info)

        return render(request, 'screen_5.html', {'courses': courses,'term': term})
    else:
        error_message = "API call failed with status code: " + str(response_courses.status_code)
        return render(request, 'screen_5.html', {'error_message': error_message})

def screen_6(request, course_id):
    api_url = "https://canvas.instructure.com/api/v1/"

    # Authentication headers (replace with your API token or OAuth)
    headers = {
        "Authorization": "Bearer 7~o1bbKk1sCwslpRjwUz2AjqlgDsFVUkvKvtKinsgx57pBhqkumaWQFomPAuKCsNpP"
    }

    # Get the course name from the query parameters
    course_name = request.GET.get('course_name', 'Student Details')

    # Make the API call to retrieve enrollments for the course
    response_enrollments = requests.get(f"{api_url}courses/{course_id}/enrollments", headers=headers)

    if response_enrollments.status_code == 200:
        enrollments_data = response_enrollments.json()
        students = []
        print(enrollments_data)
        # Filter out student enrollments
        for enrollment in enrollments_data:
            if enrollment['type'] == 'StudentEnrollment':
                student_info = {
                    'name': enrollment['user']['name'],
                    'user_id': enrollment['user']['id']
                }
                students.append(student_info)

        # Get the search query from the request
        search_query = request.GET.get('search_field', '')

        # Filter students based on the search query
        if search_query:
            students = [student for student in students if search_query.lower() in student['name'].lower() or search_query.lower() in student['csu_email'].lower()]

        return render(request, 'screen_6.html', {'students': students, 'course_id': course_id, 'course_name': course_name})
    else:
        return HttpResponse("Failed to fetch enrollments.", status=response_enrollments.status_code)

def screen_7(request, course_id, course_name, student_name,user_id):
    screen_data = retrieve_data(course_id, course_name, student_name,user_id)
    return render(request, 'screen_7.html', screen_data)

def screen_8(request, course_id, course_name, student_name,user_id):
    screen_data = retrieve_data(course_id, course_name, student_name, user_id)
    return render(request, 'screen_8.html', screen_data)

def screen_9(request, course_id, course_name, student_name, user_id):

    # update_student_grades(course_id, student_name, course_name,user_id)
    # update_all_students_grades()
    # Retrieve the weekly grades and category percentages
    grades = WeeklyGrade.objects.filter(
        student__student_id=user_id,
        course__course_id=course_id
    ).order_by('WeekNumber')
    
    # Convert the grades to a list of dictionaries
    hist_grade_data = [
        {
            'week': grade.WeekNumber,
            'grade': grade.PercentileGrade,
            'categorical_percentage':grade.categorized_assignment_grades
        }
        for grade in grades
    ]
    
    # Convert the grade data to JSON
    hist_grade_data_json = json.dumps(hist_grade_data)
    
    # Retrieve the categorical grade scores
    categorical_grades = WeeklyGrade.objects.filter(
        student__student_id=user_id,
        course__course_id=course_id
    ).order_by('WeekNumber').values_list('WeekNumber', 'categorized_assignment_grades')
    
    # Convert the categorical grade scores to a list of dictionaries
    categorical_grade_data = [
        {
            'week': week,
            'category_scores': json.loads(score)
        }
        for week, score in categorical_grades
    ]
    
    # Convert the categorical grade data to JSON
    categorical_grade_data_json = json.dumps(categorical_grade_data)
    
    screen_data = retrieve_data(course_id, course_name, student_name, user_id)
    # Pass the data to the template context
    screen_data['hist_grade_data_json'] = hist_grade_data_json
    screen_data['categorical_grade_data_json']= categorical_grade_data_json
    print(hist_grade_data_json)
    # Render the screen 9 template with the provided context
    return render(request, 'screen_9.html', screen_data)


def retrieve_data(course_id, course_name, student_name, user_id):
    api_url = "https://canvas.instructure.com/api/v1/"
    headers = {
        "Authorization": "Bearer 7~o1bbKk1sCwslpRjwUz2AjqlgDsFVUkvKvtKinsgx57pBhqkumaWQFomPAuKCsNpP"
    }

    # Initialize an empty dictionary to store categorized assignment grades
    categorized_assignment_grades = {}

    # Retrieve assignment groups
    response_assignment_groups = requests.get(f"{api_url}courses/{course_id}/assignment_groups", headers=headers)
    if response_assignment_groups.status_code == 200:
        assignment_groups_data = response_assignment_groups.json()

        # Iterate through assignment groups to initialize categories
        for group in assignment_groups_data:
            group_name = group['name']
            categorized_assignment_grades[group_name] = {
                'assignments': [],  # Store assignments here
                'total_points_possible': 0
            }

        # Fetch all assignments with pagination
        all_assignments = retrieve_all_assignments(course_id, headers)
        assignment_statistics = []

        # Iterate through assignments to collect grades and categorize them
        for assignment in all_assignments:
            assignment_id = assignment['id']
            assignment_name = assignment.get('name', 'Unknown Assignment')
            points_possible = assignment.get('points_possible', 0)

            
            statistics = fetch_and_calculate_statistics(course_id, assignment_id)
            if statistics is not None:
                assignment_statistics.append({
                    'assignment_name': assignment_name,
                    'statistics': statistics
                })

            # Retrieve grades for the specific assignment and user
            response_assignment_grades = requests.get(f"{api_url}courses/{course_id}/assignments/{assignment_id}/submissions/{user_id}", headers=headers)
            if response_assignment_grades.status_code == 200:
                assignment_grades = response_assignment_grades.json()
                student_assignment_grade = assignment_grades.get('score', 'Not Graded')

                # Find the group of the assignment
                group_id = assignment.get('assignment_group_id', None)
                group_name = next((group['name'] for group in assignment_groups_data if group['id'] == group_id), 'Uncategorized')

                # Append assignment grade to the corresponding category
                categorized_assignment_grades[group_name]['assignments'].append({
                    'name': assignment_name,
                    'grade': student_assignment_grade,
                    'points_possible': points_possible,
                    'score_statistics': statistics
                })

                categorized_assignment_grades[group_name]['total_points_possible'] += points_possible

    else:
        # Handle error response for assignment groups
        categorized_assignment_grades = {}

    category_percentages = {}
    for category, data in categorized_assignment_grades.items():
        total_points_possible = data['total_points_possible']
        total_score = sum(assignment['grade'] for assignment in data['assignments'] if assignment['grade'] is not None)
        if total_points_possible != 0:
            category_percentages[category] = (total_score / total_points_possible) * 100
        else:
            category_percentages[category] = 0

    for category, data in categorized_assignment_grades.items():
        for assignment in data['assignments']:
            assignment_name = assignment['name']
            for stat in assignment_statistics:
                if stat['assignment_name'] == assignment_name:
                    assignment['score_statistics'] = stat['statistics']
    

    # Retrieve the enrollment for the specified student in the course
    response_enrollment = requests.get(f"{api_url}courses/{course_id}/enrollments", headers=headers)
    if response_enrollment.status_code == 200:
        enrollments_data = response_enrollment.json()
        student_enrollment = None
        for enrollment in enrollments_data:
            if enrollment['user']['name'] == student_name:
                student_enrollment = enrollment
                break
        
        if student_enrollment:
            # Extract the grade information
            grade_info = {
                'current_grade': student_enrollment.get('grades', {}).get('current_grade', ''),
                'current_score': student_enrollment.get('grades', {}).get('current_score', ''),
            }
        else:
            grade_info = None
    else:
        grade_info = None

    assignment_groups_weightages, individual_risk_factors, overall_risk_factor,weighted_scores = risk_factors(course_id, headers, category_percentages)

    weighted_scores_json = json.dumps(categorized_assignment_grades)
    assignment_groups_weightages_json = json.dumps(assignment_groups_weightages)
    total_weighted_scores_json = json.dumps(weighted_scores)

    # Render the template with the provided context
    context = {
        'course_name': course_name,
        'student_name': student_name,
        'categorized_assignment_grades': categorized_assignment_grades,
        'category_percentages': category_percentages,
        'grade_info': grade_info,
        'individual_risk_factors' : individual_risk_factors,
        'overall_risk_factor' : overall_risk_factor,
        'weighted_scores' : weighted_scores,
        'assignment_groups_weightages' : assignment_groups_weightages,



        'weighted_scores_json': weighted_scores_json,
        'total_weighted_scores_json' : total_weighted_scores_json,
        'assignment_groups_weightages_json' : assignment_groups_weightages_json

    }
    return context

def fetch_and_calculate_statistics(course_id, assignment_id):
    api_url = "https://canvas.instructure.com/api/v1/" 
    headers = {
        "Authorization": "Bearer 7~o1bbKk1sCwslpRjwUz2AjqlgDsFVUkvKvtKinsgx57pBhqkumaWQFomPAuKCsNpP"
    }
    # Fetch grades for the assignment from the gradebook
    response = requests.get(f"{api_url}/courses/{course_id}/assignments/{assignment_id}/submissions", headers=headers)
    data = response.json()

    # Extract grades data
    grades = [submission.get('score') for submission in data if 'score' in submission and submission.get('score') is not None]

    if not grades:
        return None  # No grades available
    
    # Calculate statistics
    mean_score = sum(grades) / len(grades)
    max_score = max(grades)
    min_score = min(grades)

    return {
        'mean_score': mean_score,
        'max_score': max_score,
        'min_score': min_score,
        'total_submissions': len(grades)
    }
        
def retrieve_all_assignments(course_id, headers):
    api_url = "https://canvas.instructure.com/api/v1/"
    all_assignments = []
    page = 1
    
    while True:
        response = requests.get(f"{api_url}courses/{course_id}/assignments?page={page}", headers=headers)
        if response.status_code == 200:
            assignments_data = response.json()
            all_assignments.extend(assignments_data)
            # Check if there are more pages
            if 'next' in response.links:
                page += 1
            else:
                break
        else:
            print("Failed to retrieve assignments:", response.status_code)
            break
            
    return all_assignments

def risk_factors(course_id, headers, category_percentages):
    api_url = "https://canvas.instructure.com/api/v1/"
    assignment_groups_with_weightages = {}
    risk_factors = {}

    # Fetch assignment group weightages
    response_assignment_groups = requests.get(f"{api_url}courses/{course_id}/assignment_groups", headers=headers)
    if response_assignment_groups.status_code == 200:
        assignment_groups_data = response_assignment_groups.json()
        for group in assignment_groups_data:
            group_name = group['name']
            weight = group.get('group_weight', 0)
            assignment_groups_with_weightages[group_name] = {'weight': weight}

            # Calculate risk factor for each assignment group
            percentage = category_percentages.get(group_name, 0)
            risk_factor = max((100 - percentage) / 100, 0) * weight
            risk_factors[group_name] = risk_factor

    # Calculate overall risk factor
    overall_risk_factor = sum(risk_factors.values())

    # Calculate normalized weighted scores
    weighted_scores = {}
    total_weighted_score = 0
    for category, percentage in category_percentages.items():
        weightage = assignment_groups_with_weightages.get(category, {}).get('weight', 0)
        weighted_score = (percentage * weightage)/100
        weighted_scores[category] = weighted_score
        total_weighted_score += weighted_score

    return assignment_groups_with_weightages, risk_factors, overall_risk_factor, weighted_scores

def fetch_all_courses(api_url, headers):
    courses = []
    page = 1
    while True:
        # Adjusting the URL to use the provided endpoint for courses
        response = requests.get(f"{api_url}courses?page={page}", headers=headers)
        if response.status_code == 200:
            fetched_courses = response.json()
            if not fetched_courses:
                break  # Exit the loop if no more courses are returned
            courses.extend(fetched_courses)
            page += 1
        else:
            print(f"Failed to fetch courses. Status Code: {response.status_code}")
            break
    return courses

def fetch_course_students(course_id, api_url, headers):
    students = []

    # Request the first page of enrollments data from the Canvas API
    response_enrollments = requests.get(f"{api_url}courses/{course_id}/enrollments?type[]=StudentEnrollment", headers=headers)

    if response_enrollments.status_code == 200:
        enrollments_data = response_enrollments.json()

        # Iterate through each enrollment record, filtering for students
        for enrollment in enrollments_data:
            if enrollment['type'] == 'StudentEnrollment':
                student_info = {
                    'name': enrollment['user']['name'],
                    'user_id': enrollment['user']['id']
                }
                students.append(student_info)
    else:
        print(f"Failed to fetch students for course {course_id}. Status Code: {response_enrollments.status_code}")
    return students

def update_all_students_grades():
    api_url = "https://canvas.instructure.com/api/v1/"
    headers = {
        "Authorization": "Bearer 7~o1bbKk1sCwslpRjwUz2AjqlgDsFVUkvKvtKinsgx57pBhqkumaWQFomPAuKCsNpP"
    }
    courses = fetch_all_courses(api_url, headers)  # You need to implement this based on your API
    for course in courses:
        course_id = course['id']
        course_name = course['name']
        print(course_name)
        students = fetch_course_students(course_id, api_url, headers)  # Implement this function to fetch students
        for student in students:
            student_name = student['name']
            user_id = student['user_id']
            print(student_name)
            # Now, you use your existing logic to update grades, adjusted to this loop
            update_student_grades(course_id, student_name, course_name, user_id)
            print("Done !")

def update_student_grades(course_id, student_name, course_name,user_id):
    # Assuming `api_url` and `headers` are defined elsewhere and are correct
    api_url = "https://canvas.instructure.com/api/v1/"

    # Authentication headers (replace with your API token or OAuth)
    headers = {
        "Authorization": "Bearer 7~o1bbKk1sCwslpRjwUz2AjqlgDsFVUkvKvtKinsgx57pBhqkumaWQFomPAuKCsNpP"
    }

    # Fetch the current week number since the start date
    
    week_number = 6

    context = retrieve_data(course_id, course_name, student_name, user_id)
    categorized_assignment_grades = context.get('categorized_assignment_grades', {})
    

    response_enrollment = requests.get(f"{api_url}courses/{course_id}/enrollments", headers=headers)
    if response_enrollment.status_code == 200:
        enrollments_data = response_enrollment.json()
        for enrollment in enrollments_data:
            if enrollment['user']['name'] == student_name:
                grade_info = {
                    'current_grade': enrollment.get('grades', {}).get('current_grade', ''),
                    'current_score': enrollment.get('grades', {}).get('current_score', ''),
                }
                category_percentages = {}
                for category, data in categorized_assignment_grades.items():
                    total_points_possible = data['total_points_possible']
                    total_score = sum(assignment['grade'] for assignment in data['assignments'] if assignment['grade'] is not None)
                    if total_points_possible != 0:
                        category_percentages[category] = (total_score / total_points_possible) * 100
                    else:
                        category_percentages[category] = 0

                category_percentages_json = json.dumps(category_percentages)
                # Update or create student information
                student, created = Student.objects.update_or_create(
                    student_id=user_id,
                    defaults={'student_name': student_name}
                )

                course, _ = Course.objects.get_or_create(
                    course_id=course_id,
                    defaults={'course_name': course_name}  # Assuming course_name is passed or retrieved
                )

                # Create a new weekly grade record
                WeeklyGrade.objects.update_or_create(
                    student=student,
                    course=course,
                    WeekNumber='Week - ' + str(week_number),
                    PercentileGrade=grade_info['current_score'],
                    AlphabetGrade=grade_info['current_grade'],
                    categorized_assignment_grades = category_percentages_json
                )

                return JsonResponse({"success": True, "message": "Grade information updated successfully."})
                
        return JsonResponse({"success": False, "message": "Student enrollment not found."})
    else:
        return JsonResponse({"success": False, "message": "Failed to fetch enrollment information."})

# def list_view(request):

#     student = Student(student_id='8120830', student_name='Rakshith Kumar')
#     student.save()

#     items = Student.objects.all()
#     for item in items:
#         print(f"ID: {item.student_id}, Name: {item.student_name}")
#     # return render(request, 'myapp/template_list.html', {'items': items})

