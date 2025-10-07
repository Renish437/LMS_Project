from django.contrib import admin

# Register your models here.
from .models import *

class AuthorAdmin(admin.ModelAdmin):
    list_display = ('id','name')
    prepopulated_fields = {"slug":("name",)}

admin.site.register(Author, AuthorAdmin)



