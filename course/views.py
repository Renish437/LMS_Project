# course/views.py
import logging
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.db.models import Q
from .models import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

logger = logging.getLogger(__name__)

def course_list(request):
    initial_qs = Course.objects.select_related('author', 'level') \
                                .prefetch_related('category') \
                                .order_by('-id')
    categories = Category.objects.filter(is_active=True)
    levels = Level.objects.all()
    return render(request, 'course/course-list.html', {
        'courses_initial': initial_qs,
        'categories': categories,
        'levels': levels,
    })

def filter_data(request):
    """
    AJAX endpoint for all sidebar filters:
    - category[] (parent/sub combined via M2M)
    - level[]
    - instructor[]
    - price[] (radio: priceall, pricefree, pricepaid)
    - rating_min (from rating checkboxes: highest selected "X & up")
    - search (title contains)
    Returns {'data': html, 'count': int}
    """
    try:
        queryset = Course.objects.select_related('author', 'level') \
                                 .prefetch_related('category') \
                                 .order_by('-id')

        # Gather all filter params
        category_ids = request.GET.getlist('category[]')
        level_ids    = request.GET.getlist('level[]')
        instructor_ids = request.GET.getlist('instructor[]')
        price_opts   = request.GET.getlist('price[]')
        rating_min   = request.GET.get('rating_min')
        search_term  = request.GET.get('search', '').strip()

        # --- Category (M2M: parent/sub share same field) ---
        if category_ids:
            category_ids = [int(i) for i in category_ids if i.isdigit()]
            if category_ids:
                queryset = queryset.filter(category__id__in=category_ids)

        # --- Level (FK) ---
        if level_ids:
            level_ids = [int(i) for i in level_ids if i.isdigit()]
            if level_ids:
                queryset = queryset.filter(level__id__in=level_ids)

        # --- Instructor (FK to Author) ---
        if instructor_ids:
            instructor_ids = [int(i) for i in instructor_ids if i.isdigit()]
            if instructor_ids:
                queryset = queryset.filter(author__id__in=instructor_ids)

        # --- Price (radio options) ---
        if price_opts:
            # Ignore 'priceall' – it means no price filter
            if 'pricefree' in price_opts:
                queryset = queryset.filter(price=0)
            elif 'pricepaid' in price_opts:
                queryset = queryset.filter(price__gte=1)
            # If multiple or 'priceall', no filter applied

        # --- Rating (min threshold, e.g., 4.5 & up) ---
        if rating_min:
            try:
                min_val = float(rating_min)
                if 0 <= min_val <= 5:
                    queryset = queryset.filter(rating__gte=min_val)
            except ValueError:
                logger.warning("Invalid rating_min: %s", rating_min)

        # --- Search (title) ---
        if search_term:
            queryset = queryset.filter(title__icontains=search_term)

        # --- Deduplicate (critical for M2M category joins) ---
        queryset = queryset.distinct()
        
        sort_param = request.GET.get('sort')
        if sort_param == 'newest':
            queryset = queryset.order_by('-created_at')  # Assume 'created_at' field; use '-id' if none
        elif sort_param == 'price_low':
            queryset = queryset.order_by('price')
        elif sort_param == 'price_high':
            queryset = queryset.order_by('-price')
        
        # --- Pagination ---
        paginator = Paginator(queryset, 9)  # 9 courses per page (match your grid: 3 cols x 3 rows)
        page_param = request.GET.get('page', 1)
        try:
            courses_page = paginator.page(page_param)
        except PageNotAnInteger:
            courses_page = paginator.page(1)
        except EmptyPage:
            courses_page = paginator.page(paginator.num_pages)

        # --- Render results ---
        html = render_to_string('course/ajax/courses.html', {'courses': queryset}, request=request)
        count = queryset.count()

        return JsonResponse({'data': html, 'count': count})

    except Exception as exc:
        logger.error("filter_data error: %s | params: %s", exc, request.GET)
        empty_html = render_to_string('course/ajax/courses.html', {'courses': Course.objects.none()}, request=request)
        return JsonResponse({'data': empty_html, 'count': 0}, status=500)

def course_detail(request, slug):
    course = get_object_or_404(Course, slug=slug)
    return render(request, 'course/course-detail.html', {'course': course})