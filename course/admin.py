from django.contrib import admin
from django.utils.text import slugify
from .models import *


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = ('id', 'name', 'slug', 'is_active')

    def save_model(self, request, obj, form, change):
        # Auto-update slug if name changed or slug is blank
        if not obj.slug or 'name' in form.changed_data:
            obj.slug = slugify(obj.name)
        super().save_model(request, obj, form, change)


class CourseRequirementTabularInline(admin.TabularInline):
    model = CourseRequirement
class CourseGoalTabularInline(admin.TabularInline):
    model = CourseGoal
    
class CourseVideoTabularInline(admin.TabularInline):
    model = CourseVideo


    

class CourseAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    list_display = ('id', 'title', 'slug', 'status')
    inlines = (CourseGoalTabularInline,CourseRequirementTabularInline,CourseVideoTabularInline)

    def save_model(self, request, obj, form, change):
        # Auto-update slug if title changed or slug is blank
        if not obj.slug or 'title' in form.changed_data:
            new_slug = slugify(obj.title)
            unique_slug = new_slug
            num = 1
            # Ensure slug is unique
            while Course.objects.filter(slug=unique_slug).exclude(pk=obj.pk).exists():
                unique_slug = f"{new_slug}-{num}"
                num += 1
            obj.slug = unique_slug

        super().save_model(request, obj, form, change)


admin.site.register(Category, CategoryAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(Level)
admin.site.register(CourseRequirement)
admin.site.register(CourseGoal)
admin.site.register(CourseLesson)
admin.site.register(CourseVideo)
admin.site.register(Language)
