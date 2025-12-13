from django.contrib import admin
from .models import *
from unfold.admin import ModelAdmin
# Register your models here.


class BaseUnfoldAdmin(ModelAdmin):
    list_per_page = 25
    search_fields = ("id",)

@admin.register(Slider)
class SliderAdmin(BaseUnfoldAdmin):
    pass
# admin.site.register(Slider)