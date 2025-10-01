from django.shortcuts import render
from .models import *
# Create your views here.

def home(request):
    sliders = Slider.objects.all()
    context={
        'sliders':sliders
    }
    return render(request,'home/home.html',context)
    