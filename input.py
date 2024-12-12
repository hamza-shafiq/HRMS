import random
from faker import Faker
from datetime import date, timedelta
from django.contrib.auth import get_user_model
from employees.models import Employee, Department

# Initialize Faker instance
fake = Faker()

def create_fake_employees(count=20):


    # Ensure there are enough departments in the database
    departments = Department.objects.all()
    if not departments.exists():
        print("No departments found. Please create departments first.")
        return

    for _ in range(count):
        try:
            # Generate unique username and email
            username = fake.unique.user_name()
            email = fake.unique.email()
            first_name = fake.first_name()
            last_name = fake.last_name()
            phone_number = fake.phone_number()
            national_id_number = fake.unique.ssn()
            emergency_contact_number = fake.phone_number()
            gender = random.choice(['FEMALE', 'MALE', 'OTHER'])
            department = random.choice(departments)
            designation = fake.job()
            bank = fake.company()
            account_number = fake.unique.bban()
            joining_date = fake.date_between(start_date="-5y", end_date="today")
            employee_status = random.choice(['WORKING'])
            remaining_leaves = random.randint(0, 18)
            total_leaves = 18
            extra_leaves = random.randint(0, 5)
            is_team_lead = random.choice([True, False])

            # Create the employee
            employee = Employee.objects.create(
                username=username,
                email=email,
                first_name=first_name,
                last_name=last_name,
                phone_number=phone_number,
                national_id_number=national_id_number,
                emergency_contact_number=emergency_contact_number,
                gender=gender,
                department=department,
                designation=designation,
                bank=bank,
                account_number=account_number,
                joining_date=joining_date,
                employee_status=employee_status,
                remaining_leaves=remaining_leaves,
                total_leaves=total_leaves,
                extra_leaves=extra_leaves,
                is_team_lead=is_team_lead
            )

            # Optionally assign a random team lead (other than self)
            if not is_team_lead and Employee.objects.count() > 1:
                team_lead = random.choice(Employee.objects.exclude(id=employee.id))
                employee.team_lead = team_lead
                employee.save()

        except Exception as e:
            print(f"Error creating employee: {e}")

    print(f"{count} fake employees have been added.")

# Run the script
create_fake_employees()
