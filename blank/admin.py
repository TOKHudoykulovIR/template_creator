from django.contrib import admin
from .models import Blank, BlankMeta, Furniture


# Register your models here.

@admin.register(Blank)
class BlankAdmin(admin.ModelAdmin):
    list_display = ['id']


@admin.register(BlankMeta)
class ActionAdmin(admin.ModelAdmin):
    list_filter = ['id']


@admin.register(Furniture)
class FURNITUREAdmin(admin.ModelAdmin):
    list_filter = ['id']
