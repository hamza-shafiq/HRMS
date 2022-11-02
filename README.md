## HRMS API - ViteAce Solutions

This API contains the basic features of human resource management system.

### Modules:
* User Authorization & Authentication
* Employees Management
* Assets Management
* Employee Attendance
* Employee Leaves Management
* Recruitment
* Payroll

## Getting Started
### Dependencies
* Python IDE with Django framework.
* Postgres Database

### Installing

* Clone the repo by using link
```
git clone https://github.com/hamza-shafiq/HRMS.git
```
* Create & activate the virtual environment
```
- python -m venv hrms_venv
- source hrms_venv/bin/activate
```
* Install the required dependencies through pip
```
pip install -r requirements.txt
```
* Connect psql through terminal & create new database, db user & grant access on dataabse.

* Insert your database credentials in .env file
* Execute database migrations
```
python manage.py migrate
```
* For static files collection
```
python manage.py collectstatic
```
* Use the following command to crate superuser & follow the steps
```
python manage.py createsuperuser
```
* Finally, run django server through following command
```
python manage.py runserver
```

### Test coverage

To run the tests, check your test coverage, and generate an HTML coverage report:

    $ coverage run -m pytest
    $ coverage html
    $ open htmlcov/index.html