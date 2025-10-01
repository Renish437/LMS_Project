from django.shortcuts import render
from django.urls import path
from . import views
urlpatterns = [
    path('contact-us/',views.contact,name="contact"),
    path('about-us/',views.about,name="about"),
]
