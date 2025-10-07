from django.db import models

# Create your models here.
from course.models import *

class Slider(models.Model):
    title = models.CharField(max_length=255)
    sub_title = models.CharField(max_length=255)
    slider_course = models.ForeignKey(Course,on_delete=models.SET_NULL,null=True,related_name="course_slider")
    image = models.ImageField(upload_to="uploads/sliders/")

    def __str__(self):
        return self.title

    # def __unicode__(self):
    #     return 
