from django.urls import path
from . import views

app_name = 'mailing'
urlpatterns = [
# post views
path('', views.ArticleListView.as_view(), name='mailing'),
path('<int:year>/<int:month>/<int:day>/<slug:post>/',
views.article_detail,
name='article_detail'),
path('article_new/', views.PostCreateView.as_view(), name='article_new'),
path('<int:post_id>/share/',views.post_share, name='post_share'),
    ]
