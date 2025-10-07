from django.db import models

# Create your models here.


class Author(models.Model):
    name = models.CharField(max_length=100,null=True)
    slug = models.SlugField()
    about_author = models.CharField(max_length=100,null=True)
    author_profile = models.ImageField(upload_to="uploads/author")

    def __str__(self):
        return self.name



