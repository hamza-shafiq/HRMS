from rest_framework import serializers

from finance.models import Payroll


class PayRollSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payroll
        fields = ["id", "basic_salary", "bonus", "reimbursement", "travel_allowance", "tax_deduction", "config",
                  "month", "year", "released", "employee"]

    def to_representation(self, instance):
        ret = super(PayRollSerializer, self).to_representation(instance)
        ret['employee_name'] = str(instance.employee.get_full_name)
        ret['employee_status'] = str(instance.employee.employee_status)
        ret['employee_designation'] = str(instance.employee.designation)
        return ret
