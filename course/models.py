from django.db import models
from django.contrib.auth.models import User
# Create your models here.
from accounts.models import Author
from ckeditor.fields import RichTextField 
from ckeditor_uploader.fields import RichTextUploadingField
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
    

    
class Course(models.Model):
    STATUS = (
        ('Published','Published'),
        ('Draft','Draft')
    )
    title = models.CharField(max_length=500)
    slug = models.SlugField(null=True)
    author = models.ForeignKey(Author,on_delete=models.CASCADE,null=True)
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    description = RichTextUploadingField()
    price = models.IntegerField(null=True,default=0)
    discount = models.IntegerField(null=True,default=0)
    status = models.CharField(choices=STATUS,max_length=100,null=True)
    featured_image = models.ImageField(upload_to="uploads/courses/featured-images",null=True)
    featured_video = models.CharField(max_length=500,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 
    class Meta:
        db_table = 'course_courses'
        managed = True
        verbose_name = 'Course'
        verbose_name_plural = 'Courses'
    def __str__(self):
        return self.title
    


