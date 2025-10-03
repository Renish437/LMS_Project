from django.urls import path 
from . import views
from django.contrib.auth import views as auth_views
urlpatterns = [
    path("register/", views.register, name="register"),
    path("login/", views.login, name="login"),
    path('logout/', views.logout_user, name='logout'),
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='password_reset.html'), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'), name='password_reset_done'),
    
    path('profile/update/', views.profile_update, name='profile_update'),
]
