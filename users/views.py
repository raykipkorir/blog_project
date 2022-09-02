from django.contrib import messages
from django.contrib.auth import authenticate, get_user_model, login
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.mail import EmailMessage
from django.shortcuts import redirect, render
from django.urls import reverse_lazy, reverse
from django.views.generic import DeleteView, UpdateView
from django.template.loader import render_to_string

from blog_project import settings
from blog.models import Post
from .models import Profile
from .forms import ProfileUpdateForm, UserRegisterForm, UserUpdateForm

User = get_user_model()

def register(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            form = UserRegisterForm(request.POST)
            if form.is_valid():
                form.save()
                content = render_to_string("users/email_confirmation_template.html", {"form":form}, request)
                email = EmailMessage(
                subject="Thank you",
                body=content,
                from_email=settings.EMAIL_HOST_USER,
                to=[form.instance.email],
                )
                email.send(fail_silently=False)
                user = authenticate(
                    username=form.cleaned_data["username"],
                    password=form.cleaned_data["password1"],
                )
                if user is not None:
                    login(request, user)
                    messages.success(request, "Account created successfully!!")
                    return redirect("blog:blog-home")
        else:
            form = UserRegisterForm()
        return render(request, "users/user_create.html", {"form": form})
    else:
        return redirect(reverse("blog:blog-home"))

class UserLoginView(LoginView):
    template_name = "users/login.html"
    redirect_authenticated_user = True

    def form_valid(self, form):
        messages.success(self.request, message="Logged in successfully!!!")
        return super().form_valid(form)

@login_required()
def profile(request, username):
    user_profile = Profile.objects.get(user__username=username)
    posts = Post.objects.filter(user=user_profile.user)
    context = {"user_profile":user_profile, "posts":posts}
    return render(request, "users/user_profile.html", context)


@login_required()
def EditProfile(request):
    profile = Profile.objects.get(user=request.user)
    if request.method == "POST":
        form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile Updated successfully!!")
            return redirect("users:user_profile_update")
    else:
        form = ProfileUpdateForm(instance=profile)
    context = {"form": form}
    return render(request, "users/user_profile_update.html", context)

class UserUpdateView(LoginRequiredMixin,UserPassesTestMixin,SuccessMessageMixin,UpdateView):
    model = User
    template_name = "users/user_update.html"
    form_class = UserUpdateForm
    success_message = "Account updated successfully"

    def test_func(self):
        user = self.get_object()
        if self.request.user == user:
            return True
        else:
            return False


class UserDeleteView(LoginRequiredMixin,UserPassesTestMixin,SuccessMessageMixin,DeleteView):
    model = User
    template_name = "users/user_delete.html"
    success_url = reverse_lazy("users:login")
    success_message = "We are sad to see you leave :("

    def test_func(self):
        user = self.get_object()
        if self.request.user == user:
            return True
        else:
            return False
