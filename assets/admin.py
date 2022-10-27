from django.contrib import admin

import assets.models

# Register your models here.

admin.site.register(assets.models.Asset)
admin.site.register(assets.models.AssignedAsset)
