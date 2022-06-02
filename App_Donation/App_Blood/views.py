from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.utils import timezone
from App_Blood.filters import Donerfilter
from App_Blood.forms import CommentForm, ContactusForm
from App_Blood.models import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from App_Accounts.models import *

# Create your views here.

def index(request):
    blogs=Blogpost.objects.all().order_by('-id')
    A_plus=Profile.objects.filter(bloodgroup='A+').count()
    B_plus=Profile.objects.filter(bloodgroup='B+').count()
    O_plus=Profile.objects.filter(bloodgroup='O+').count()
    O_minus=Profile.objects.filter(bloodgroup='O-').count()
    AB_plus=Profile.objects.filter(bloodgroup='AB+').count()
    AB_minus=Profile.objects.filter(bloodgroup='AB-').count()
    A_minus=Profile.objects.filter(bloodgroup='A-').count()
    B_minus=Profile.objects.filter(bloodgroup='B-').count()
    latest_doners = Profile.objects.filter(
        Q(type="blood doner") & Q(address__isnull=False) & Q(bloodgroup__isnull=False)
    ).order_by("-id")
    context={
        'blogs':blogs,
        'A_plus':A_plus,
        'A_minus':A_minus,
        'B_plus':B_plus,
        'AB_plus':AB_plus,
        'AB_minus':AB_minus,
        'B_minus':B_minus,
        'O_plus':O_plus,
        'O_minus':O_minus,
        'today': timezone.now(),
        'latest_doners':latest_doners,
    }
    return render(request, 'App_Blood/index.html',context)


def About(request):
    context={
        'today': timezone.now(),
    }
    return render(request, 'App_Blood/about-us.html',context)


def Contact(request):
    try:
        if request.method=="POST":
            form=ContactusForm(request.POST or None)
            if form.is_valid():
                form.save()
                messages.success(request,'Thanks for your message we will contact you soon',extra_tags="contact")
                return redirect(request.POST['next'])
        else:
            form=ContactusForm()

    except:
        return redirect('App_Blood:contact')

    context={
        'form':form,
        'today': timezone.now()
    }
    return render(request, 'App_Blood/contact.html',context)


def Gallery(request):
    context={
        'today': timezone.now(),
    }
    return render(request, 'App_Blood/gallery-2.html',context)


def Doner(request):
    all_doners=Profile.objects.filter(
        Q(type="blood doner") & Q(address__isnull=False) & Q(bloodgroup__isnull=False)
    )
    myfilter = Donerfilter(request.GET, queryset=all_doners)
    all_doners = myfilter.qs
    page = request.GET.get('page', 1)
    paginator = Paginator(all_doners, 12)
    try:
        all_doners = paginator.page(page)
    except PageNotAnInteger:
        all_doners = paginator.page(1)
    except EmptyPage:
        all_doners = paginator.page(paginator.num_pages)

    context={
        'all_doners':all_doners,
        'myfilter':myfilter,
        'today': timezone.now()
    }
    return render(request, 'App_Blood/donor.html',context)

def Donardetails(request,id):
    try:
        get_user=Profile.objects.get(id=id)
        if request.method=="POST":
            user_name=request.POST['name']
            user_email=request.POST['email']
            user_message=request.POST['message']

            msg=Bloodrequest.objects.create(
                name=user_name,email=user_email,message=user_message
            )
            msg.save()
            subject_ = "Blood Request"
            message = render_to_string('App_Blood/message.html', {
                'email': msg.email,
                'name': msg.name,
                'subject': subject_,
                'message': msg.message,
            })
            email = EmailMessage(
                subject_, message, to=[get_user.user.email, ]
            )
            email.send()
            messages.success(request,"Your message send successfully",extra_tags="blood_request")
            return redirect(request.POST['next'])
    except:
        return redirect('App_Blood:doner')

    context={
        'single_doner':get_user,
        'today': timezone.now()
    }
    return render(request,'App_Blood/doner_details.html',context)
def Blog(request):
    all_blog = Blogpost.objects.all()
    page = request.GET.get('page', 1)
    paginator = Paginator(all_blog, 6)
    try:
        all_blog = paginator.page(page)
    except PageNotAnInteger:
        all_blog = paginator.page(1)
    except EmptyPage:
        all_blog = paginator.page(paginator.num_pages)
    context = {
        'all_blog': all_blog,
        'today': timezone.now()
    }
    return render(request, 'App_Blood/blog.html', context)


@login_required(login_url="App_Accounts:login")
def Blogdetails(request, id):
    try:
        blog_post = Blogpost.objects.get(id=id)
        recent_blog = Blogpost.objects.exclude(id=blog_post.id).order_by('-post_on')[:8]
        comments = Comment.objects.filter(post=blog_post, reply=None).order_by('-id')
        if request.method == "POST":
            comment_form = CommentForm(request.POST or None)
            if comment_form.is_valid():
                content = comment_form.cleaned_data.get('content')
                reply_id = request.POST.get('comment_id')
                comment_qs = None
                if reply_id:
                    comment_qs = Comment.objects.get(id=reply_id)
                comment = Comment.objects.create(
                    post=blog_post, user=request.user, content=content,reply=comment_qs
                )
                comment.save()
        else:
            comment_form = CommentForm()
        is_liked = False
        if blog_post.like.filter(id=request.user.id).exists():
            is_liked = True
        context = {
            'blog_post': blog_post,
            'recent_blog': recent_blog,
            'comment_form': comment_form,
            'comments':comments,
            'is_liked':is_liked,
            'today': timezone.now()
        }
    except:
        return redirect('App_Blood:blog')
    if request.is_ajax():
        html = render_to_string('App_Blood/comment_section.html', context, request=request)
        return JsonResponse({'form': html})
    return render(request, 'App_Blood/blog_details.html', context)

def blog_like(request):
    blog_post = get_object_or_404(Blogpost, id=request.POST.get('blog_id'))
    is_liked = False
    if blog_post.like.filter(id=request.user.id).exists():
        blog_post.like.remove(request.user)
        is_liked = False
    else:
        blog_post.like.add(request.user)
        is_liked = True

    context = {
        'blog_post': blog_post,
        'is_liked': is_liked,
    }
    if request.is_ajax():
        html = render_to_string('App_Blood/reaction_section.html', context, request=request)
        return JsonResponse({'form': html})

def Privacy(request):
    return render(request, 'App_Blood/privacy.html')


def Brancheview(request):
    branch_list=Branch.objects.all()
    context={
        'branch_list':branch_list,
        'today': timezone.now()
    }

    return render(request,'App_Blood/branches.html',context)

def SingleBranch(request,id):
    try:
        branch=Branch.objects.get(id=id)
        slider_img=BranchSlider.objects.filter(branch_name=branch)
        context={
            'branch':branch,
            'slider_img':slider_img,
            'today': timezone.now(),
        }
    except:
        return redirect('App_Blood:branches')
    return render(request,'App_Blood/single_branch.html',context)