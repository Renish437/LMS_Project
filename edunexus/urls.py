"""
URL configuration for edunexus project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path,include
from . import user_register

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('home.urls')),
    path('course/',include('course.urls')),
    path('edunexus/',include('app.urls')),
     path("accounts/register/", user_register.register, name="register"),
     path("accounts/login/", user_register.login, name="login"),
      path('logout/', user_register.logout_user, name='logout'),
    path('accounts/',include('django.contrib.auth.urls')),
    
]
if settings.DEBUG: 
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
