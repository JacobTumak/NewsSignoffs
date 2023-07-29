from django.urls import path
from article.views import new_article_view, article_detail_view,\
    all_articles_view, my_articles_view, all_liked_articles_view,\
    like_article_view, save_article_view

urlpatterns = [
    path('new_article/', new_article_view, name='new_article'),
    path('article_detail/<int:article_id>/', article_detail_view, name='article_detail'),
    path('all_articles/', all_articles_view, name='all_articles'),
    path('liked_articles/', all_liked_articles_view, name='liked_articles'),
    path('my_articles/', my_articles_view, name='my_articles'),
    path('like_article/<int:article_id>/', like_article_view, name='like_article'),
    path('save_article/<int:article_id>/', save_article_view, name='save_article'),
]