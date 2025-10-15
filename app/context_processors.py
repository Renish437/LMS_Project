from course.models import *
def course_categories(request):
    course_categories = Category.objects.filter(is_active=True)
    return dict(course_categories=course_categories)
def courses(request):
    courses = Course.objects.filter(status="Published")
    for course in courses:
        try:
            rating = float(course.rating) if course.rating else 0
            course.rating_percentage = (rating/5)*100
        except (ValueError,TypeError):
            course.rating_percentage =0
            
    return dict(courses=courses)


    