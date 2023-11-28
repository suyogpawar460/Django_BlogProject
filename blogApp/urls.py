from django.urls import path
from . import views as blog_views

urlpatterns = [
    path('', blog_views.PostListView.as_view(), name='home'),
    path('about/', blog_views.aboutView, name='about'),
    path('services/', blog_views.servicesView, name='services'),
    path('contact/', blog_views.contactView, name='contact'),
    path('post_detail/<int:pk>/', blog_views.PostDetailView.as_view(), name='post_detail'),
    path('post_create/', blog_views.PostCreateView.as_view(), name='post_create'),
    path('post_update/<int:pk>/', blog_views.PostUpdateView.as_view(), name='post_update'),
    path('post_delete/<int:pk>/', blog_views.PostDeleteView.as_view(), name='post_delete'),
    path('user/<str:username>/', blog_views.UserPostListView.as_view(), name='user_posts'),
    path('latest_posts/', blog_views.latest_posts_view, name='latest_posts'),

]
