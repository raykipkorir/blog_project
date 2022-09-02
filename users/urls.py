from django.contrib.auth import views as auth_views
from django.urls import path, re_path, reverse_lazy

from . import views

app_name = "users"
urlpatterns = [
    path("register/", views.register, name="user_create"),
    path(
        "login/",
        views.UserLoginView.as_view(),
        name="login",
    ),
    path(
        "logout/",
        auth_views.LogoutView.as_view(template_name="users/logout.html"),
        name="logout",
    ),
    path("settings/", views.EditProfile, name="user_profile_update"),
    path("settings/profile/", views.EditProfile, name="user_profile_update"),
    path("settings/user/<int:pk>/", views.UserUpdateView.as_view(), name="user_update"),
    path("settings/user/delete/<int:pk>/", views.UserDeleteView.as_view(), name="user_delete"),
    path(
        "settings/user/password_change/",
        auth_views.PasswordChangeView.as_view(
            template_name="users/password_change.html",
            success_url=reverse_lazy("users:password_change_done"),
        ),
        name="password_change",
    ),
    path(
        "settings/user/password_change/done/",
        auth_views.PasswordChangeDoneView.as_view(
            template_name="users/password_change_done.html"
        ),
        name="password_change_done",
    ),
    path(
        "password-reset/",
        auth_views.PasswordResetView.as_view(
            template_name="users/password_reset.html",
            success_url=reverse_lazy("users:password_reset_done"),
            email_template_name="registration/password_reset_email.html",
        ),
        name="password_reset",
    ),
    path(
        "password-reset/done/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="users/password_reset_done.html"
        ),
        name="password_reset_done",
    ),
    path(
        "password-reset-confirm/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="users/password_reset_confirm.html",
            success_url=reverse_lazy("users:password_reset_complete"),
        ),
        name="password_reset_confirm",
    ),
    path(
        "password-reset-complete/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="users/password_reset_complete.html"
        ),
        name="password_reset_complete",
    ),
    re_path(r"^(?P<username>\w+)/$", views.profile, name="user_profile"),
]