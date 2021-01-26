from django.contrib import admin
from .models import CropModel,CustomOrder
# Register your models here.
class CropAdmin(admin.ModelAdmin):
    ordering = ['-time',]
    list_display = ('image__name',)

admin.site.register(CropModel)
class CustomOrdersAdmin(admin.ModelAdmin):
    list_display = ('id', 'amount', "created_at")

admin.site.register(CustomOrder, CustomOrdersAdmin)
