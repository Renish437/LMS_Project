from django.shortcuts import render
from .models import *
from course.models import *
# Create your views here.

def home(request):
    sliders = Slider.objects.all()
    for slider in sliders:
        try:
            rating = float(slider.slider_course.rating) if slider.slider_course.rating else 0
            slider.slider_course.rating_percentage = (rating / 5) * 100
        except (ValueError, TypeError):
            slider.slider_course.rating_percentage = 0
    context={
        'sliders':sliders,
   
    }
    return render(request,'home/home.html',context)
    