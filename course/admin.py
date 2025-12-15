from django.contrib import admin
from django.utils.text import slugify
from .models import *
from unfold.admin import ModelAdmin
from import_export.admin import ImportExportModelAdmin
from unfold.contrib.import_export.forms import ExportForm, ImportForm, SelectableFieldsExportForm
from unfold.contrib.filters.admin import RangeDateFilter, RangeDateTimeFilter
from unfold.admin import StackedInline, TabularInline
class CategoryAdmin(ModelAdmin,ImportExportModelAdmin):
    
    prepopulated_fields = {"slug": ("name",)}
    list_display = ('id', 'name', 'slug','parent_category', 'is_active')
    list_filter_submit =True 
    list_filter = (
        'is_active',

        )
    
    import_form_class = ImportForm
    export_form_class = ExportForm

    def save_model(self, request, obj, form, change):
        
        if not obj.slug or 'name' in form.changed_data:
            obj.slug = slugify(obj.name)
        super().save_model(request, obj, form, change)


class CourseRequirementTabularInline(StackedInline):
    model = CourseRequirement
class CourseGoalTabularInline(TabularInline):
    model = CourseGoal
    
class CourseVideoTabularInline(StackedInline):
    model = CourseVideo


    

class CourseAdmin(ModelAdmin,ImportExportModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    
    list_display = (
        'id',
        'title',
        'author',
        'price',
        'discounted_amount',
        'status',
        'level',
        'language',
        'rating',
        'created_at',
    )
    # change_list_template = "admin/course/course_list.html"
    list_filter_submit = True 
    list_filter = (
        'category',
        'status',
        'level',
        'language',
        'certificate',
        
        ("created_at", RangeDateTimeFilter),  
        ("updated_at", RangeDateTimeFilter),  
        )
    import_form_class = ImportForm
    export_form_class = ExportForm
    search_fields = ('title','slug','author__name')
    ordering = ('-created_at',)
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


class BaseUnfoldAdmin(ModelAdmin):
    list_per_page = 25
    search_fields = ("id",)

@admin.register(Level)
class LevelAdmin(BaseUnfoldAdmin):
    list_display = ('id','name')
    pass


@admin.register(CourseRequirement)
class CourseRequirementAdmin(BaseUnfoldAdmin):
    list_display = ('id','course','point')
    pass


@admin.register(CourseGoal)
class CourseGoalAdmin(BaseUnfoldAdmin):
    list_display = ('id','course','point')
    pass


@admin.register(CourseLesson)
class CourseLessonAdmin(BaseUnfoldAdmin):
    list_display = ('id','name','course')
    pass


@admin.register(CourseVideo)
class CourseVideoAdmin(BaseUnfoldAdmin):
    list_display = (
        'id',
        'title',
        'course',
        'lesson',
        'serial_number',
        'preview',
        'time_duration',
    )
    list_filter = ('preview',)
    pass


@admin.register(EnrolledCourse)
class EnrolledCourseAdmin(BaseUnfoldAdmin):
    list_display = (
        'id',
        'user',
        'course',
        'paid',
        'enroll_type',
        'enrolled_at',
    )
    list_filter = ('paid', 'enroll_type')

    pass


@admin.register(Language)
class LanguageAdmin(BaseUnfoldAdmin):
    list_display = ('id','language')
    pass



@admin.register(Payment)
class PaymentAdmin(BaseUnfoldAdmin):
    list_display = ('order_id','payment_id','user','course','status','date')
    list_filter = ('status',)
    pass


# admin.site.register(Level)
# admin.site.register(CourseRequirement)
# admin.site.register(CourseGoal)
# admin.site.register(CourseLesson)
# admin.site.register(CourseVideo)
# admin.site.register(EnrolledCourse)
# admin.site.register(Language)
# admin.site.register(Payment)
