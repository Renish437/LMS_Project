from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
# Create your models here.


class Author(models.Model):
    name = models.CharField(max_length=100,null=True)
    slug = models.SlugField()
    author_role = models.CharField(max_length=100,null=True)
    author_rating = models.FloatField(null=True)
    author_reviews = models.IntegerField(null=True)
    author_students = models.IntegerField(null=True)
    about_author = RichTextUploadingField(null=True)
    author_profile = models.ImageField(upload_to="uploads/author")

    def __str__(self):
        return self.name



