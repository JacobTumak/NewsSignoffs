from django.urls import include, path
from article import views, generic_views

urlpatterns = [
    path('', generic_views.redirect_to_home, name='redirect_to_home'),
    path('accounts/', include("django.contrib.auth.urls")),
    path('accounts/profile/', generic_views.custom_profile_redirect, name='custom_profile_redirect'),
    path('accounts/profile/logout/', generic_views.custom_logout, name='logout'),

    path('signup/', views.signup_view, name='signup'),
    path('signup/terms-of-service/', views.terms_of_service_view, name='terms_of_service'),
    path('signup/newsletter/', views.newsletter_view, name='newsletter'),
    path('signup/newsletter/revoke/<int:signet_id>/', views.revoke_newsletter_view, name='revoke_newsletter'),

    path('users/<username>/', views.user_profile_view, name='user_profile'),

    path('new-article/', views.new_article_view, name='new_article'),
    path('delete-article/<int:article_id>/', generic_views.delete_article_view, name='delete_article'),
    path('edit-article/<int:article_id>/', views.edit_article_view, name='edit_article'),
    path('like-article/<int:article_id>/', views.like_article_view, name='like_article'),
    path('article-detail/<int:article_id>/', views.article_detail_view, name='article_detail'),
    path('article-detail/revoke/<int:signet_id>/', views.revoke_comment_view, name='revoke_comment'),
    path('article-detail/publish/<int:article_id>/', views.publish_article_view, name='publish_article'),

    path('all-articles/', generic_views.all_articles_view, name='all_articles'),
    path('liked-articles/', generic_views.all_liked_articles_view, name='liked_articles'),
    path('my-articles/', generic_views.my_articles_view, name='my_articles'),
]
