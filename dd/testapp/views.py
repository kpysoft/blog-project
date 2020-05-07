from django.shortcuts import render,get_object_or_404
from .models import post
from taggit.models import Tag
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
from testapp.forms import emailform
from django.core.mail import send_mail
#from django.models import count



# Create your views here.
from django.db.models import Count

def post_view(request,t_name=None):

    post_data=post.objects.all()

    latest=post_data.order_by('-created')[:2]#to get latest post

#to get most number of post
    most_commented=post_data.annotate(c_c=Count('comments')).order_by('-c_c')

    #total=post_data.count()

    tag=None

    if t_name:
        tag=get_object_or_404(Tag,name=t_name)
        #give you list of tag object  which name is pass in argument
        post_data=post_data.filter(tags__in=[tag])


    paginator=Paginator(post_data,2)
    page_number=request.GET.get('page')
    try:
        post_data=paginator.page(page_number)
    except PageNotAnInteger:
        post_data=paginator.page(1)
    except EmptyPage:
        post_data=paginator.page(paginator.num_pages)


    return render(request,'testapp/home.html',{'post_data':post_data,'tag':tag,'latest':latest,'most':most_commented})

from .forms import CommentForm

def details_view(request,id,slug):

    p_post=get_object_or_404(post,id=id,slug=slug)


    comments=p_post.comments.filter(active=True)
    csubmit=False

    if request.method=='POST':
        form=CommentForm(request.POST)
        if form.is_valid():
            newcomment=form.save(commit=False)
            newcomment.post=p_post
            newcomment.save()
            csubmit=True
            #return HttpResponseRedirect('/')
    if request.method=='GET':
        form=CommentForm()
    return render(request,'testapp/detail.html',{'csubmit':csubmit,'p_post':p_post,'form':form,'comments':comments})



def email_send_view(request,id):

    p_post=get_object_or_404(post,id=id)
    flag=False
    if request.method=='POST':
        form=emailform(request.POST)
        if form.is_valid():
            cd=form.cleaned_data

            subject='{} is recommended to read{} '.format(cd['name'],p_post.title)
            message='you are awseom\n\n you can read comment{}'.format(cd['comment'])
            send_mail(subject,message,'durgasoft@gmail.com',[cd['to']])
            flag=True
    else:

        form=emailform()
    return render(request,'testapp/email.html',{'post':p_post,'form':form})
