from django.contrib import admin

# Register your models here.
from .models import *

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug":("name",)}
    list_display = ('id','name','slug','is_active')

admin.site.register(Category, CategoryAdmin)
class CourseAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug":("title",)}
    list_display = ('id','title','slug','status')

admin.site.register(Course, CourseAdmin)
admin.site.register(Level)
