from course.models import *
def course_categories(request):
    course_categories = Category.objects.filter(is_active=True)
    return dict(course_categories=course_categories)
    