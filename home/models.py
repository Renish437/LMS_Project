from django.db import models

# Create your models here.


class Slider(models.Model):
    title = models.CharField(max_length=255)
    sub_title = models.CharField(max_length=255)
    image = models.ImageField(upload_to="uploads/sliders/")

    def __str__(self):
        return self.title

    # def __unicode__(self):
    #     return 
