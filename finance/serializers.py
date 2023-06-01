from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.template.loader import render_to_string
from employees.models import Employee
from finance.models import Payroll
from user.tasks import send_email



class PayRollSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payroll
        fields = ["id", "basic_salary", "bonus", "reimbursement", "travel_allowance", "tax_deduction", "month", "year",
                  "released", "employee"]

    def create(self, validated_data):
        employee = validated_data.get('employee')
        if employee:
            email_body = 'Hi ' + employee.username + '!\n' + \
                         ' Your payroll has been generated for the month of ' + validated_data['month']\
                         + ' ' + validated_data['year'] + '\n' + \
                         'You can now view it at your dashboard.'
            data = {'email_body': email_body, 'to_email': employee.email,
                    'email_subject': 'Payroll Generated'}
            # generate_and_send_employee_credentials(data)
            send_email.delay(data)
            validated_data['employee'] = employee
            return super().create(validated_data)
        else:
            raise ValidationError('This asset is already assigned to someone')

    def to_representation(self, instance):
        ret = super(PayRollSerializer, self).to_representation(instance)
        ret['employee_name'] = str(instance.employee.get_full_name)
        return ret


    def update(self, instance, validated_data):
        user_email = validated_data['employee'].email
        context = {
            'employee': validated_data['employee'],
            'month': validated_data['month'],
            'year': validated_data['year'],
            'released': validated_data['released'],
            'basic_salary': validated_data['basic_salary']
        }

        if validated_data['released'] == instance.released:
            email_subject = 'Payroll Released'

        else:
            email_subject = 'Payroll Created'
        template_file_path = "emails/salary_slip.html"

        email_body = render_to_string(template_file_path, context)
        #
        data = {
            'email_body': email_body,
            'to_email': user_email,
            'email_subject': email_subject
        }
        send_email(data)
        super().update(instance, validated_data)
        return instance
