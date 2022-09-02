from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)

from .forms import CreatePostForm, UpdatePostForm
from .models import Post

User = get_user_model()


class PostListView(ListView):
    model = Post
    template_name = "blog/home.html"
    context_object_name = "posts"
    paginate_by = 10

    def get_context_data(self, *args, **kwargs):
        try:
            return super().get_context_data(*args, **kwargs)
        except Http404:
            self.kwargs["page"] = 1
            return super().get_context_data(*args, **kwargs)


class PostDetailView(DetailView):
    model = Post
    template_name = "blog/post_detail.html"
    context_object_name = "post"


class CreatePostView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Post
    form_class = CreatePostForm
    template_name = "blog/post_create.html"
    success_message = "New post has been created!!"

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class PostUpdateView(
    LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, UpdateView
):
    model = Post
    form_class = UpdatePostForm
    template_name = "blog/post_update.html"
    success_message = "Post Updated Successfully"

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.user:
            return True
        return False


class PostDeleteView(
    LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, DeleteView
):
    model = Post
    template_name = "blog/post_confirm_delete.html"
    context_object_name = "post"
    success_url = reverse_lazy("blog:blog-home")

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.user:
            return True
        return False