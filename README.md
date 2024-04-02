# LAD-Advisor

## Introduction
- Learning Analytics Dashboard (LAD) for Advisors offers data insights to aid decision-making on student progress and success.
- Uses Analytics & Visualization to improve the quality of advising through interpretable data.
- Essential Features of this Advisor focused LAD include :
    - Comprehensive Cumulative Analytics to deliver a full spectrum view of student academic trajectories.
    - Early Intervention for Risk Identification and Performance Feedback Analysis.
    - Historical Grade Trend & Categorical Impact Analysis.

## Methodology

### System Architecture & API Integration
- Established the core structure using the Django framework, ensuring robustness and scalability for the Learning Analytics Dashboard.
- Developed custom API endpoints within the Django framework to trigger data retrieval from the Canvas LMS.
### Security & Authorization Protocols
- Implemented an authorization flow using keys and headers specified in Canvas LMS for secure data access.
### Data Retrieval & Storage
- Configured Django views to act as intermediaries for JSON data requests, utilizing authorization keys for data extraction from Canvas LMS.
- Incorporated a MySQL database into the architecture for persistent storage of historical data, facilitating longitudinal data analysis.
- Utilized Django models to query the MySQL database and present historical data on the dashboard.
### Interface Design & Data Presentation
- Developed intuitive and responsive webpages using HTML, CSS, and JavaScript to display educational analytics in an engaging and understandable format.
### Key Canvas LMS API End-Points
- url:GET|/api/v1/courses/:course_id/assignments
- url:GET|/api/v1/courses/:course_id/enrollments
- url:GET|/api/v1/courses/:course_id/assignment_groups/:assignment_group_id
- url:GET|/api/v1/courses/:course_id/assignments/:assignment_id/submissions

## Architecture

![Blank diagram (2)](https://github.com/suchithreddyv/LAD-Advisor/assets/44540739/1451245f-1825-4fe1-a426-be39afcda6e2)

## Setup Instructions 

#### Prerequisites:
- **Django:** Make sure to have Django installed. If not, install it using pip: pip install Django==4.1.1.
- **Canvas LMS Account:** We'll need access to a Canvas Instructure LMS instance where we can configure and use the Dashboard. So, we need to create an instructor account.
- **Database Server:** We will also require Database to store Histrorical Data. We are using MySQL Server here. 

#### 1.Clone the repository
git clone https://project.git
cd project
#### 2.Set up a virtual environment (Optional but recommended)
python -m venv venv
**On Windows**
venv\Scripts\activate
**On Unix or MacOS**
source venv/bin/activate

#### 3. Canvas LMS Configuration
In your Canvas Instructure account, navigate to App Settings of the course and add an external tool/app definition for your LTI application. This step will involve providing essential information such as the launch URL (usually a localhost URL with a port number and the endpoint which we give in the urls.py: https://127.0.0.1:8080/lti/), as well as configuring security settings by putting the consumer and secret keys. Retrieve the consumer_key and secret_key generated by Canvas, which you'll need to use in the Django project to verify incoming requests.

#### 4.Configure settings.py

- Configure the Django project settings, particularly the MIDDLEWARE settings in the settings.py file where we must disable the csrf to get the application working.
- Additionally, update the INSTALLED_APPS list to include AppName and sslserver.
- Implement LTI authentication by verifying the incoming LTI launch request's parameters, such as Consumer Key and Secret Key.
- Configure the Keys as below in the settings.py:

PYLTI_CONFIG = {
'consumers': {'<random number string>': { 'secret': '<random number string>' }}}

#### 5. Authorization Header Setup.

To create a API Header Authorization Token , In your Canvas Instructure Account Go to Account Settings --> Approved Integrations --> New Access Token

Copy that access token , Set it's expiry date and put that token in the views.py

#### 6.Set up the database (Adjust instructions based on your database choice - Here I've used MySQL)

This project uses MySQL as its database backend. Follow these steps to configure your MySQL database with Django.

**Prerequisites**
- MySQL Server installed on your machine.
- MySQL Client for connecting to the server (usually included with the server installation).
- Install MySQL Python dependencies
- Django requires mysqlclient to interface with MySQL databases. 

Install it using pip: pip install mysqlclient

Then create database and other basic settings in MySQL.

**Configure Django to Use MySQL**
- Modify settings.py
- Open your Django project's settings.py file.
- Find the DATABASES setting and update it to match your MySQL database configuration:

  DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'yourdbname',
        'USER': 'yourusername',
        'PASSWORD': 'yourpassword',
        'HOST': 'localhost',  # Or an IP Address that your DB is hosted on
        'PORT': '3306',
    }
}

**Apply migrations**
To create the necessary database tables, run:

python manage.py makemigrations

python manage.py migrate

#### 7.Run the development server
python manage.py runserver

Here we are using SSL Server 

Use the following commands to install and run the SSL server:
- **Installation** - sudo pip install django-sslserver
- **Execution** - python ./manage.py runsslserver localhost:portNumber

Note:  Navigate to http://127.0.0.1:8000/ to see the project running locally.

