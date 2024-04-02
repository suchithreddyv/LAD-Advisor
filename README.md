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
- Developed custom API endpoints within the Django framework to trigger data retrieval from the Canvas LMS. Security & Authorization Protocols
- Implemented an authorization flow using keys and headers specified in Canvas LMS for secure data access.
### Data Retrieval & Storage
- Configured Django views to act as intermediaries for JSON data requests, utilizing authorization keys for data extraction from Canvas LMS.
- Incorporated a MySQL database into the architecture for persistent storage of historical data, facilitating longitudinal data analysis.
- Utilized Django models to query the MySQL database and present historical data on the dashboard Interface Design & Data Presentation
- Developed intuitive and responsive webpages using HTML, CSS, and JavaScript to display educational analytics in an engaging and understandable format.
### Key Canvas LMS API End-Points
- url:GET|/api/v1/courses/:course_id/assignments
- url:GET|/api/v1/courses/:course_id/enrollments
- url:GET|/api/v1/courses/:course_id/assignment_groups/:assignment_group_id
- url:GET|/api/v1/courses/:course_id/assignments/:assignment_id/submissions

## Architecture

![Blank diagram (2)](https://github.com/suchithreddyv/LAD-Advisor/assets/44540739/1451245f-1825-4fe1-a426-be39afcda6e2)

## Setup Instructions 


