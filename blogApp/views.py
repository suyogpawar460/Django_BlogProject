from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import redirect_to_login
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView

from .models import Post


# Create your views here.
class PostListView(ListView):
    model = Post
    context_object_name = 'posts'
    template_name = 'blogApp/home.html'
    ordering = ['-date_posted']


class PostDetailView(DetailView):
    model = Post
    context_object_name = 'post'
    template_name = 'blogApp/post_detail.html'


# def homeView(request):
#     posts = Post.objects.all()
#     context = {
#         "posts": posts
#     }
#     return render(request, 'blogApp/home.html', context)


class PostCreateView(CreateView):
    model = Post
    fields = ['title', 'content']
    context_object_name = 'form'
    template_name = 'blogApp/post_create.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']
    context_object_name = 'form'
    template_name = 'blogApp/post_update.html'
    success_url = '/'
    login_url = 'login'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

    def handle_no_permission(self):
        if self.raise_exception:
            raise PermissionDenied(self.get_permission_denied_message())

        return redirect_to_login(self.request.get_full_path(),
                                 self.get_login_url(),
                                 self.get_redirect_field_name())


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    context_object_name = 'post'
    template_name = 'blogApp/post_delete.html'
    success_url = '/'
    login_url = 'login'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

    def handle_no_permission(self):
        if self.raise_exception:
            raise PermissionDenied(self.get_permission_denied_message())

        return redirect_to_login(self.request.get_full_path(),
                                 self.get_login_url(),
                                 self.get_redirect_field_name())


class UserPostListView(ListView):
    model = Post
    context_object_name = 'user_posts'
    template_name = 'blogApp/user_posts.html'

    def get_queryset(self):
        user = get_object_or_404(
            User, username=self.kwargs.get('username')
        )
        return Post.objects.filter(author=user)


def latest_posts_view(request):
    latest_posts = Post.objects.all().order_by('-date_posted')[:2]
    context = {
        'latest_posts': latest_posts
    }
    return render(request, 'blogApp/latest_posts.html', context)


def aboutView(request):
    return render(request, 'blogApp/about.html')


def servicesView(request):
    return render(request, 'blogApp/services.html')


def contactView(request):
    return render(request, 'blogApp/contact.html')
