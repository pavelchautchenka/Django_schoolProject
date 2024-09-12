School Website Project

Project Description

This is a web application designed for a school website. It contains important admission information and provides individual accounts for students, parents, and teachers.

Key Features:
General Information: The site provides essential information about the school and the admission process.
Personal Accounts:
Student Account: Students can view their schedule, check grades, and access exam timetables.
Parent Account: Parents can monitor their child's grades, receive messages from teachers, and view schedules and exam timetables.
Teacher Account: Teachers can assign grades, create schedules, and send messages to parents.
Technologies Used

Backend: Django (Python Web Framework)
Database: PostgreSQL
Task Queue: Redis and Celery
Frontend: HTML, CSS
Containerization: Docker
Orchestration: Kubernetes
Web Server: Nginx



Installation Instructions

Clone the repository:
git clone https://github.com/pavelchautchenka/Django_schoolProject

Navigate to the project directory:

cd school-website-project

Install dependencies:

pip install -r requirements.txt

Set up the PostgreSQL database:

Create a new PostgreSQL database.
Update the DATABASES configuration in settings.py with your database credentials.

Run migrations:

python manage.py migrate

Run Redis and Celery (if using Docker, include Docker Compose setup):

redis-server
celery -A school_project worker -l info

Run the development server:

python manage.py runserver
Docker Instructions

Build and start the Docker containers:

docker-compose up --build
To stop the containers:

docker-compose down
Future Improvements

Implement notifications for parents and students via email.
Expand administrative functionalities.
Add real-time updates for schedules and grades.
