from django.db import models
from django.contrib.auth.models import User
# Create your models here.
from accounts.models import Author
from ckeditor.fields import RichTextField 
from ckeditor_uploader.fields import RichTextUploadingField
from django.core.validators import MinValueValidator, MaxValueValidator
from django.urls import reverse
class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200)
    icon = models.TextField(null=True)
    parent_category = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='sub_categories')
    is_active = models.BooleanField(default=True)
    
    
    class Meta:
        db_table = 'course_categories'
        managed = True
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
    
    def __str__(self):
        return self.name

class Level(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name 
class Language(models.Model):
    language = models.CharField(max_length=100)
    
    def __str__(self):
        return self.language

    
class Course(models.Model):
    STATUS = (
        ('Published', 'Published'),
        ('Draft', 'Draft'),
    )
    LEVELS = (
        ("Beginner","Beginner"),
        ("Intermediate","Intermediate"),
        ("Advanced","Advanced"),
    )

    title = models.CharField(max_length=500)
    slug = models.SlugField(null=True, blank=True,max_length=100)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, null=True,related_name="course_author")
    category = models.ManyToManyField('Category',related_name="course_category")
    short_description = models.TextField(max_length=255,null=True)
    description = RichTextUploadingField()
    price = models.IntegerField(null=True, default=0)
    discounted_amount = models.IntegerField(null=True, default=0)
    discount = models.IntegerField(null=True, default=0)
    status = models.CharField(choices=STATUS, max_length=100, null=True)
    level = models.ForeignKey(Level,on_delete=models.CASCADE,null=True,related_name="course_level")
    featured_image = models.ImageField(upload_to="uploads/courses/featured-images", null=True, blank=True)
    featured_video = models.CharField(max_length=500, null=True, blank=True)
    review_count = models.IntegerField(null=True, blank=True)
    lesson_count = models.IntegerField(null=True, blank=True)
    
   
    rating = models.DecimalField(
        max_digits=2,             
        decimal_places=1,          
        null=True,
        blank=True,
        validators=[
            MinValueValidator(1.0),
            MaxValueValidator(5.0)
        ]
    )
    language = models.ForeignKey(Language,on_delete=models.CASCADE,null=True)
    deadline = models.DateField(null=True)
    certificate =models.BooleanField(default=True) 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        db_table = 'course_courses'
        managed = True
        verbose_name = 'Course'
        verbose_name_plural = 'Courses'
    def __str__(self):
        return self.title
    def get_url(self):
        return reverse('course:course-detail', kwargs={'slug': self.slug})
    def get_checkout_url(self):
        return reverse('course:checkout',kwargs={'slug': self.slug})
    def get_watch_url(self):
       return reverse('course:watch-course', kwargs={'slug': self.slug}) + f'?lecture={self.id}'

      
    

class CourseGoal(models.Model):
    course = models.ForeignKey(Course,on_delete=models.CASCADE,related_name="course_goals")
    point = models.CharField(max_length=500)

    def __str__(self):
        return self.point
    
class CourseRequirement(models.Model):
    course = models.ForeignKey(Course,on_delete=models.CASCADE,related_name="course_requirements")
    point = models.CharField(max_length=500)
    

    def __str__(self):
        return self.point


class CourseLesson(models.Model):
    name = models.CharField(max_length=200)
    course = models.ForeignKey(Course,on_delete=models.CASCADE,related_name="course_lessons")
    
    

    def __str__(self):
        return self.name + "-"+self.course.title

class CourseVideo(models.Model):
    serial_number = models.IntegerField(null=True)
    title = models.CharField(max_length=100)
    course = models.ForeignKey(Course,on_delete=models.CASCADE,related_name="course_videos")
    lesson = models.ForeignKey(CourseLesson,on_delete=models.CASCADE,related_name="lesson_videos")
    thumbnail = models.ImageField(upload_to="uploads/courses/youtube-thumbnails", null=True, blank=True)
    youtube_id = models.CharField(max_length=200)
    time_duration = models.FloatField(null=True)
    preview = models.BooleanField(default=False)
    

    def __str__(self):
        return self.title
    def get_watch_url(self):
       return reverse('course:watch-course', kwargs={'slug': self.lesson.course.slug}) + f'?lecture={self.id}'
    
class EnrolledCourse(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    course = models.ForeignKey(Course,on_delete=models.CASCADE,related_name="enrolled_course")
    paid = models.BooleanField(default=0)
    enroll_type = models.CharField(max_length=100,null=True,default="Free") # Stripe, RazorPay,Paypal,Free
    enrolled_at = models.DateTimeField(auto_now_add=True)
    
    # def __str__(self):
    #     return self.user.username+ " - "+ self.course.title
    
    
class Payment(models.Model):
    order_id = models.CharField(max_length=100,null=True,blank=True)
    payment_id = models.CharField(max_length=100,null=True,blank=True)
    enrolled_course = models.ForeignKey(EnrolledCourse,on_delete=models.CASCADE,null=True,blank=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    course = models.ForeignKey(Course,on_delete=models.CASCADE,null=True)
    date = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=False)
    

    
    
    








