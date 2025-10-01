from django.contrib import admin
from . import views
from django.urls import path,include

urlpatterns = [
 path('course-list/',views.course_list,name="course-list")
]