from django.contrib import admin

import recruitments.models

# Register your models here.
admin.site.register(recruitments.models.Recruits)
admin.site.register(recruitments.models.Referrals)
admin.site.register(recruitments.models.RecruitsHistory)
