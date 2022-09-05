import random

from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.core.mail import send_mail
from django.db import models
from .forms import EmailPostForm, SubscriberForm
from .models import Article, Subscriber
from django.conf import settings
from django.core.paginator import Paginator, EmptyPage,\
PageNotAnInteger
from django.views.generic import ListView, CreateView
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt

User = settings.AUTH_USER_MODEL

class ArticleListView(ListView):
    queryset = Article.published.all()
    context_object_name='posts'
    paginate_by = 4
    template_name = 'list.html'

class EmailCreateView(CreateView):
    model = Article
    template_name = 'article_new.html'
    fields = ('title', 'slug', 'author', 'body','status')


def article_detail(request, year, month, day, post):
    post = get_object_or_404(Article, slug=post,
    status='published',
    publish__year=year,
    publish__month=month,
    publish__day=day)

    return render(request,'detail.html', {'post': post})

def post_list(request):
    object_list = Article.published.all()
    paginator = Paginator(object_list, 3) # 3 posts in each page
    page = request.GET.get('page')
    try:
        post = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        post = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        post = paginator.page(paginator.num_pages)
    return render(request,
    'blog/post/list.html',
    {'page': page,
    'posts': post})


mail = settings.DEFAULT_FROM_EMAIL
def post_share(request, post_id):

    post = get_object_or_404(Article, id=post_id, status='published')
    sent = False
    if request.method == 'POST':

        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(
                post.get_absolute_url())
            subject = f"{cd['name']} recommends you read " \
                      f"{post.title}"
            message = f"Read {post.title} at {post_url}\n\n" \
                      f"{cd['name']}\'s comments: {cd['comments']}"
            send_mail(subject, message, mail,
                      cd['to'])
            sent = True
    else:
        form = EmailPostForm()
    return render(request, 'share.html',
                  {'post': post,'form': form,'sent': sent})

def random_digits():
    return "%0.12d" % random.randint(0, 999999999999)

@csrf_exempt
def new(request):
    if request.method == 'POST':
        sub = Subscriber(email=request.POST['email'], conf_num=random_digits())
        sub.save()

        return render(request, 'index.html', {'email': sub.email, 'action': 'added', 'form': SubscriberForm()})
    else:
        return render(request, 'index.html', {'form': SubscriberForm()})