from rest_framework import serializers

from finance.models import Payroll


class PayRollSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payroll
        fields = ["id", "basic_salary", "bonus", "reimbursement", "travel_allowance", "tax_deduction", "month", "year",
                  "released", "employee"]

    def to_representation(self, instance):
        ret = super(PayRollSerializer, self).to_representation(instance)
        ret['employee_name'] = str(str(instance.employee.first_name).capitalize() + " " +
                                   str(instance.employee.last_name).capitalize())
        return ret
