from django.contrib import admin
from .models import CustomUser, ListDetails

admin.site.register(CustomUser)
@admin.register(ListDetails)
class AdministDetails(admin.ModelAdmin):
    list_display = ["id", "desc", "is_finished"]
