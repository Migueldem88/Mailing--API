import random
from django.conf import settings

from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.core.mail import send_mail, EmailMessage
from .forms import EmailPostForm, SubscriberForm, EmailSendForm
from .models import Article, Subscriber, Email

from django.core.paginator import Paginator, EmptyPage,\
PageNotAnInteger
from django.views.generic import ListView, DetailView, CreateView
from django.shortcuts import redirect,render
from django.views.decorators.csrf import csrf_exempt
from django.views import View

from django.views.generic.edit import UpdateView, DeleteView

User = settings.AUTH_USER_MODEL

class ArticleListView(ListView):
    queryset = Article.published.all()
    context_object_name='posts'
    paginate_by = 4
    template_name = 'list.html'


class PostCreateView(CreateView):
    model = Article
    template_name = 'article/article_new.html'
    fields = ('title', 'slug', 'author', 'body','status')



def article_detail(request, year, month, day, post):
    post = get_object_or_404(Article, slug=post,
    status='published',
    publish__year=year,
    publish__month=month,
    publish__day=day)

    return render(request,'article/detail.html', {'post': post})

class ArticleUpdateView(UpdateView):
    model = Article
    fields = ('title', 'body',)
    template_name = 'article/article_edit.html'
class ArticleDeleteView(DeleteView):
    model = Article
    template_name = 'article/article_delete.html'
    success_url = reverse_lazy('mailing')

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

# class EmailCreateView(CreateView):
#     model = Email
#     template_name = 'sendmail.html'
#     fields = ('to','subject', 'content',)

class EmailAttachementView(View):
    form_class = EmailSendForm
    template_name = 'sendmail.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'email_form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)

        if form.is_valid():

            subject = form.cleaned_data['subject']
            body = form.cleaned_data['content']

            email = form.cleaned_data['to']
            attach = request.FILES['attach']
            mail = EmailMessage(subject, body, settings.DEFAULT_FROM_EMAIL, email,)
            mail.send()

            try:
                mail = EmailMessage(subject, body, [email])
                mail.attach(attach.name, attach.read(), attach.content_type)
                mail.send()
                return render(request, self.template_name,
                              {'email_form': form, 'error_message': 'Sent email to %s' % email})
            except:
                return render(request, self.template_name,
                              {'email_form': form, 'error_message': 'Either the attachment is too big or corrupt'})

        return render(request, self.template_name,
                      {'email_form': form, 'error_message': 'Unable to send email. Please try again later'})

