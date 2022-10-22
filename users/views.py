from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import DeleteView, UpdateView
from allauth.account.views import EmailView
from allauth.account.forms import AddEmailForm
from blog.models import Post
from .models import Profile
from .forms import ProfileUpdateForm, UserUpdateForm

User = get_user_model()

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
            return redirect("user_profile_update")
    else:
        form = ProfileUpdateForm(instance=profile)
    context = {"form": form}
    return render(request, "users/user_profile_update.html", context)

# class UserUpdateView(LoginRequiredMixin,UserPassesTestMixin,SuccessMessageMixin,UpdateView):
#     model = User
#     http_method_names = ["POST"]
#     template_name = "users/user_update.html"
#     form_class = UserUpdateForm
#     success_message = "Account updated successfully"

#     def test_func(self):
#         user = self.get_object()
#         if self.request.user == user:
#             return True
#         else:
#             return False
# user_update = UserUpdateView.as_view()

class UserEmailView(EmailView):
    success_url = reverse_lazy("user_update")
    template_name = "users/user_update.html"

    def form_invalid(self, form):
        messages.error(self.request, "Email not available")
        return redirect("user_update")
email_view = UserEmailView.as_view()

@login_required()
def account_update(request):
    user = User.objects.get(pk=request.user.id)
    if request.method == "POST" and "user_update" in request.POST:
        form = UserUpdateForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Account updated successfully")
            return redirect(reverse_lazy("user_update"))
    elif ("action_add" in request.POST or "action_send" in request.POST or "action_primary" in request.POST or "action_remove" in request.POST) and request.method == "POST":
        return email_view(request)
    else:
        user_form = UserUpdateForm(instance=user)
        add_email_form = AddEmailForm()
        context= {"user_form":user_form, "add_email_form":add_email_form}
        return render(request, "users/user_update.html", context)

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
