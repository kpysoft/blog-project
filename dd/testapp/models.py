from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from taggit.managers import TaggableManager

# Create your models here.

class post(models.Model):
    STATUS_CHOICES=(('draft','Draft'),('published','Published'))
    title=models.CharField(max_length=300)
    slug=models.SlugField(max_length=254)
    author=models.ForeignKey(User,related_name='blog_posts',on_delete=models.CASCADE)
    body=models.TextField()
    publish=models.DateTimeField(default=timezone.now)
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)
    status=models.CharField(max_length=10,choices=STATUS_CHOICES,default='draft')
    tags=TaggableManager()

    class Meta:
        ordering=['-publish']

    def __str__(self):
        return self.title

    #def get_absolute_url(self):
        #return reverse('details',args=[self.id,self.slug])

class Comment(models.Model):
    post=models.ForeignKey(post,on_delete=models.CASCADE,related_name='comments')
    name=models.CharField(max_length=30)
    body=models.TextField()
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)
    active=models.BooleanField(default=True)


    class Meta:

        ordering=['-created']

    def __str__(self):

        return "commented by {} on {}".format(self.name,self.post)
