# course/views.py
import logging
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.db.models import Q,Count
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import *
from django.utils.safestring import mark_safe
# course/views.py



logger = logging.getLogger(__name__)

def course_list(request,slug=None):
    initial_qs = Course.objects.select_related('author', 'level') \
                                .prefetch_related('category') \
                                .order_by('-id')
    selected_category = request.GET.get('category')

    # ✅ Filter by category slug (if in URL)
    # if slug:
    #     selected_category = get_object_or_404(Category, slug=slug)
    #     # Include subcategories as well
    #     subcategories = selected_category.sub_categories.all()
    #     initial_qs = initial_qs.filter(category__in=[selected_category] + list(subcategories)).distinct()
    
    paginator = Paginator(initial_qs, 9)
    page_number = request.GET.get('page')
    courses_initial_page = paginator.get_page(page_number)
    for course in courses_initial_page:
        try:
            rating = float(course.rating) if course.rating else 0
            course.rating_percentage = (rating/5)*100
        except (ValueError,TypeError):
            course.rating_percentage =0

    # Fixed annotations: Use correct reverse related names from models/error
    course_categories = Category.objects.filter(is_active=True).annotate(course_count=Count('course_category'))  # M2M reverse
    levels = Level.objects.annotate(course_count=Count('course_level'))  # FK reverse
    instructors = Author.objects.annotate(course_count=Count('course'))  # Explicit related_name='course' on FK

    free_count = Course.objects.filter(price=0).count()
    paid_count = Course.objects.filter(price__gte=1).count()

    return render(request, 'course/course-list.html', {
        'courses_initial_page': courses_initial_page,
        'paginator': paginator,
        'course_categories': course_categories,
        'levels': levels,
        'instructors': instructors,
        'free_count': free_count,
        'paid_count': paid_count,
        
        'selected_category': selected_category,
    })

def filter_data(request):
    try:
        queryset = Course.objects.select_related('author', 'level') \
                                 .prefetch_related('category')

        # Filters
        category_ids = request.GET.getlist('category[]')
        level_ids = request.GET.getlist('level[]')
        instructor_ids = request.GET.getlist('instructor[]')
        price_opt = request.GET.get('price[]')  # Single value
        rating_min = request.GET.get('rating_min')
        search_term = request.GET.get('search', '').strip()

        if category_ids:
            category_ids = [int(i) for i in category_ids if i.isdigit()]
            if category_ids:
                queryset = queryset.filter(category__id__in=category_ids)

        if level_ids:
            level_ids = [int(i) for i in level_ids if i.isdigit()]
            if level_ids:
                queryset = queryset.filter(level__id__in=level_ids)

        if instructor_ids:
            instructor_ids = [int(i) for i in instructor_ids if i.isdigit()]
            if instructor_ids:
                queryset = queryset.filter(author__id__in=instructor_ids)

        if price_opt:
            if price_opt == 'pricefree':
                queryset = queryset.filter(price=0)
            elif price_opt == 'pricepaid':
                queryset = queryset.filter(price__gte=1)

        if rating_min:
            try:
                min_val = float(rating_min)
                if 0 <= min_val <= 5:
                    queryset = queryset.filter(rating__gte=min_val)
            except ValueError:
                logger.warning("Invalid rating_min: %s", rating_min)

        if search_term:
            queryset = queryset.filter(
                Q(title__icontains=search_term) | Q(author__name__icontains=search_term)
            )

        queryset = queryset.distinct()

        # Sorting
        sort_param = request.GET.get('sort')
        if sort_param == 'newest':
            queryset = queryset.order_by('-created_at')
        elif sort_param == 'price_low':
            queryset = queryset.order_by('price')
        elif sort_param == 'price_high':
            queryset = queryset.order_by('-price')
        else:
            queryset = queryset.order_by('-id')

        # Pagination
        paginator = Paginator(queryset, 9)
        page_number = request.GET.get('page', 1)
        try:
            courses_page = paginator.page(page_number)
        except PageNotAnInteger:
            courses_page = paginator.page(1)
        except EmptyPage:
            courses_page = paginator.page(paginator.num_pages)

        # Render
        courses_html = render_to_string('course/ajax/courses_grid.html', {'courses': courses_page.object_list if courses_page else []}, request=request)
        pagination_html = render_to_string('course/ajax/pagination.html', {
            'courses_page': courses_page,
            'paginator': paginator,
        }, request=request)

        return JsonResponse({
            'courses_html': courses_html,
            'pagination_html': pagination_html,
            'count': paginator.count
        })

    except Exception as exc:
        logger.error("filter_data error: %s | params: %s", exc, request.GET)
        empty_html = render_to_string('course/ajax/courses_grid.html', {'courses': []}, request=request)
        empty_pag = render_to_string('course/ajax/pagination.html', {'courses_page': None, 'paginator': None}, request=request)
        return JsonResponse({
            'courses_html': empty_html,
            'pagination_html': empty_pag,
            'count': 0
        }, status=500)

def course_detail(request, slug):
    course = get_object_or_404(Course, slug=slug)

    try:
        rating = float(course.rating) if course.rating else 0
        course.rating_percentage = (rating/5)*100
    except (ValueError,TypeError):
        course.rating_percentage =0
    
    
    
    course.description = mark_safe(course.description)
    
    
    context = {
        "course": course,
   
    }
    return render(request, 'course/course-detail.html', context)



def search_course(request):
    keyword = request.GET.get('keyword', '')  # get the keyword safely
    print(keyword)  # for debugging, optional

    # You can later add filtering logic like:
    courses = Course.objects.filter(Q(title__icontains=keyword)|Q(category__name__icontains=keyword)).distinct()
    context ={
        'courses':courses,
        'keyword': keyword
    }

    return render(request, 'course/search-course.html',context)