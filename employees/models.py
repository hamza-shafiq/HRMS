from django.db import models


class BaseModel(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Department(BaseModel):
    department_name = models.CharField(max_length=50)
    description = models.CharField(max_length=250)

    def __str__(self):
        return f'{self.department_name}'


class Employee(BaseModel):
    GENDER_OPTIONS = [
        ('FEMALE', 'FEMALE'),
        ('MALE', 'MALE'),
        ('OTHER', 'OTHER')
    ]
    employee_id = models.CharField(max_length=50, primary_key=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone_number = models.TextField(max_length=20)
    email = models.EmailField()
    national_id_number = models.IntegerField(null=False, unique=True)
    emergency_contact_number = models.TextField(max_length=20)
    gender = models.CharField(choices=GENDER_OPTIONS, max_length=255)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    designation = models.CharField(max_length=50)
    salary = models.IntegerField()
    bank = models.CharField(max_length=50)
    account_number = models.TextField(max_length=50)
    profile_pic = models.ImageField()
    joining_date = models.DateTimeField()

    def __str__(self):
        return f"{self.employee_id} {self.first_name}"
