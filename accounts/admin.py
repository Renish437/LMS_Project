from django.contrib import admin
from unfold.admin import ModelAdmin
# Register your models here.
from .models import *

from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin
from django.contrib.auth.models import User, Group
from django.contrib.admin import register

from unfold.forms import AdminPasswordChangeForm, UserChangeForm, UserCreationForm
from unfold.admin import ModelAdmin
from import_export.admin import ImportExportModelAdmin
from unfold.contrib.import_export.forms import ExportForm, ImportForm, SelectableFieldsExportForm
# 🔴 Unregister default admin
admin.site.unregister(User)
# admin.site.unregister(Group)
@admin.register(User)
class UserAdmin(BaseUserAdmin, ModelAdmin,ImportExportModelAdmin):
    # Forms loaded from `unfold.forms`
    form = UserChangeForm
    add_form = UserCreationForm
    change_password_form = AdminPasswordChangeForm
    

    
    list_display = ("username", "email", "is_staff", "is_active")
    list_filter = ("is_staff", "is_superuser", "is_active")
    search_fields = ("username", "email")
    ordering = ("username",)
    
    import_form_class = ImportForm
    export_form_class = ExportForm
    
    
class AuthorAdmin(ModelAdmin,ImportExportModelAdmin):
    list_display = ('id','name')
    # list_filter =('name')
    prepopulated_fields = {"slug":("name",)}
    import_form_class = ImportForm
    export_form_class = ExportForm

admin.site.register(Author, AuthorAdmin)



