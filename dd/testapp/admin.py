from django.contrib import admin
from .models import post,Comment

# Register your models here.

class postadmin(admin.ModelAdmin):

    list_display=['title','slug','author','body','publish','created','updated','status']
    #list_editable=['slug','author','body','publish','status']
    list_filter=['title','author','publish','created','updated','status']
    search_fields=['title','body']
    prepopulated_fields={'slug':['title']}
    raw_id_fields=['author']
    ordering=['created']
    date_hierarchy="publish"

class CommentAdmin(admin.ModelAdmin):

    lsit_display=['name','body','post','created','updated','active']




admin.site.register(post,postadmin)
admin.site.register(Comment,CommentAdmin)
