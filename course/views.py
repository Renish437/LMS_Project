# course/views.py
import logging
from time import time
from django.shortcuts import render, get_object_or_404,redirect
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.db.models import Q,Count
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import *
from django.utils.safestring import mark_safe
from django.db.models import Sum
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from django.conf import settings
import stripe 
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
    # Explicit related_name='course' on FK
    instructors = Author.objects.annotate(course_count=Count('course_author'))
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
        
    is_enroll=False
    if request.user.is_authenticated:
        is_enroll = EnrolledCourse.objects.filter(user=request.user,course=course).exists()
        
    
    course.description = mark_safe(course.description)
    
    time_duration = CourseVideo.objects.filter(course__slug=slug).aggregate(sum=Sum('time_duration'))
    context = {
        "course": course,
         "time_duration":time_duration,
         "is_enroll":is_enroll
   
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


@login_required
def checkout(request, slug):
    course = get_object_or_404(Course, slug=slug)
    action = request.GET.get('action')
   
    discounted_amount = course.price - (course.price * course.discount / 100)
    domain = settings.APP_URL
    stripe.api_key = settings.STRIPE_SECRET
    
    if course.price == 0:
        EnrolledCourse.objects.get_or_create(
            user=request.user,  
            course=course,
        )
        course.save()
        messages.success(request, "Enrolled course successfully!")
        return redirect('home')
    
    elif action == "create_payment":
        if request.method == "POST":
            first_name      = request.POST.get('first_name', '').strip()
            last_name       = request.POST.get('last_name', '').strip()
            country         = request.POST.get('country', '').strip()
            address_1       = request.POST.get('address_1', '').strip()
            address_2       = request.POST.get('address_2', '').strip()
            city            = request.POST.get('city', '').strip()
            state           = request.POST.get('state', '').strip()
            postcode        = request.POST.get('postcode', '').strip()
            phone           = request.POST.get('phone', '').strip()
            email           = request.POST.get('email', '').strip()
            order_comments  = request.POST.get('order_comments', '').strip()
            payment_method  = request.POST.get('payment_method', 'stripe')
            # receipt =f"Edunexus-{int(time())}"
            order_id = f"EDUNEXUS-ORDER-{int(time())}"

            payment = Payment.objects.create(
            order_id=order_id,
            payment_id=None, 
            user=request.user,
            course=course,
            status=False  
            )

            # Save order reference in session
            request.session['course_id'] = course.id
            request.session['payment_method'] = payment_method
            request.session['order_id'] = order_id
            checkout_session = stripe.checkout.Session.create(
                line_items=[
                    {
                       'price_data':{
                           'currency':'usd',
                           'product_data':{
                               'name':course.title,
                               'description':course.short_description[:100],
                               
                           },
                           'unit_amount': int(discounted_amount * 100)
                       },
                         'quantity': 1,
                       
                    }
                ],
                mode="payment",
                customer_email=email,
                success_url=domain + '/course/success/',
                cancel_url=domain + '/course/cancel/',
            )
            return redirect(checkout_session.url, code=303)
            
        
        
    
    context = {
            'course': course,
            'user':request.user
            }
    return render(request, 'course/checkout.html',context)

@login_required
def success(request):
    course_id = request.session.get('course_id')
    order_id = request.session.get('order_id')
    enroll_type = request.session.get('payment_method', 'Stripe')

    if not course_id or not order_id:
        messages.error(request, "Course information not found!")
        return redirect('home')

    course = get_object_or_404(Course, id=course_id)
    user = request.user

    #  Retrieve the payment record created in checkout
    try:
        payment = Payment.objects.get(order_id=order_id, user=user, course=course)
        payment.status = True

      
        stripe_session_id = request.GET.get('session_id')
        if stripe_session_id:
            stripe_session = stripe.checkout.Session.retrieve(stripe_session_id)
            payment.payment_id = stripe_session.payment_intent  # or stripe_session.id
        else:
            payment.payment_id = f"EDUNEXUS-PAY-{int(time())}"  # fallback

        payment.save()
    except Payment.DoesNotExist:
        messages.error(request, "Payment record not found!")
        return redirect('home')

    enrolled_course, created = EnrolledCourse.objects.get_or_create(
        user=user,
        course=course,
        defaults={'paid': True, 'enroll_type': enroll_type}
    )
    payment.enrolled_course = enrolled_course
    payment.save()

    # Cleanup
    for key in ['course_id', 'payment_method', 'order_id']:
        request.session.pop(key, None)

    if created:
        messages.success(request, f"You have successfully enrolled in {course.title}!")
    else:
        messages.info(request, f"You were already enrolled in {course.title}.")

    return render(request, "course/pages/success.html", {"course": course})



@login_required
def cancel(request):
    course_id = request.session.get('course_id')
    enroll_type = request.session.get('payment_method', 'Stripe')

    if not course_id:
        messages.error(request, "No course found for this cancelled transaction.")
        return redirect('home')

    course = get_object_or_404(Course, id=course_id)
    user = request.user

    request.session.pop('course_id', None)
    request.session.pop('payment_method', None)

    messages.warning(request, f"Your payment for {course.title} was cancelled. Please try again.")

    return render(request, "course/pages/cancel.html", {"course": course})



def my_courses(request):
    enrolled_courses = EnrolledCourse.objects.filter(user=request.user)
    courses = [enrolled.course for enrolled in enrolled_courses]
    context={
      'enrolled_courses' :courses 
    }
    return render(request,'course/my-courses.html',context)





        