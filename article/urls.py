from django.urls import include, path
from article import views

urlpatterns = [
    path('', views.redirect_to_home, name='redirect_to_home'),
    path('accounts/', include("django.contrib.auth.urls")),
    path('accounts/profile/', views.custom_profile_redirect, name='custom_profile_redirect'),
    path('accounts/profile/logout/', views.custom_logout, name='logout'),
    path('signup/', views.signup_view, name='signup'),
    path('new-article/', views.new_article_view, name='new_article'),
    path('article-detail/<int:article_id>/', views.article_detail_view, name='article_detail'),
    path('all-articles/', views.all_articles_view, name='all_articles'),
    path('liked-articles/', views.all_liked_articles_view, name='liked_articles'),
    path('my-articles/', views.my_articles_view, name='my_articles'),
    path('like-article/<int:article_id>/', views.like_article_view, name='like_article'),
    path('delete-article/<int:article_id>/', views.delete_article_view, name='delete_article'),
    path('edit-article/<int:article_id>/', views.edit_article_view, name='edit_article'),
    # path('save-article/<int:article_id>/', save_article_view, name='save_article'),
]