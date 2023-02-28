from rest_framework import serializers
from finance.models import Payroll
from user.tasks import generate_and_send_employee_credentials


class PayRollSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payroll
        fields = ["id", "basic_salary", "bonus", "reimbursement", "travel_allowance", "tax_deduction", "month", "year",
                  "released", "employee"]

    def to_representation(self, instance):
        ret = super(PayRollSerializer, self).to_representation(instance)
        ret['employee_name'] = str(instance.employee.get_full_name)
        return ret

    def create(self, validated_data):
        user_email = validated_data['employee'].email
        email_body = 'Hi ' + validated_data['employee'].username + '!\n' + \
                     ' Your payroll has been generated for the month of ' + validated_data['month']\
                     + ' ' + validated_data['year'] + '\n' + \
                     'You can now view it at your dashboard.'
        data = {'email_body': email_body, 'to_email': user_email,
                'email_subject': 'Payroll Generated'}
        generate_and_send_employee_credentials(data)

        response = Payroll.objects.create(**validated_data)

        return response

    def update(self, instance, validated_data):
        user_email = validated_data['employee'].email
        if validated_data['released'] == instance.released:
            email_body = 'Hi ' + validated_data['employee'].username + '!\n' + \
                         ' Your payroll has been updated for the month of ' + validated_data['month'] \
                         + ' ' + validated_data['year'] + '\n' + \
                         'You can now view it at your dashboard.'
            data = {'email_body': email_body, 'to_email': user_email,
                    'email_subject': 'Payroll Updated'}
        else:
            email_body = 'Hi ' + validated_data['employee'].username + '!\n' + \
                         ' Your payroll has been released for the month of ' + validated_data['month'] \
                         + ' ' + validated_data['year'] + '\n' + \
                         'You can now view it at your dashboard.'
            data = {'email_body': email_body, 'to_email': user_email,
                    'email_subject': 'Payroll Released'}

        generate_and_send_employee_credentials(data)
        super().update(instance, validated_data)
        return instance
