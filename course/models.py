from django.db import models

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200)
    icon = models.TextField(null=True)
    is_active = models.BooleanField(default=True)
    
    
    class Meta:
        db_table = 'course_categories'
        managed = True
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
    
    def __str__(self):
        return self.name


