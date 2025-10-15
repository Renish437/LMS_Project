from django.contrib import admin
from . import views
from django.urls import path,include
app_name = 'course'
urlpatterns = [
# Main list page – static filters + initial courses
    path('course-list/', views.course_list, name='course-list'),
    
    # AJAX filter endpoint (used by JS)
    path('filter-data/', views.filter_data, name='filter-data'),
    
    # Detail view – make it distinct (e.g., require 'course/' prefix or put it first if slugs are unique)
    path('courses/<slug:slug>/', views.course_detail, name='course-detail'),
]