from django.shortcuts import render

# Create your views here.

def contact(request):
    return render(request,'contact/contact.html')
def about(request):
    return render(request,'about/about-us.html')
    