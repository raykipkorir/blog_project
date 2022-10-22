from django.urls import path, re_path
from . import views

urlpatterns = [
    path("settings/", views.EditProfile, name="user_profile_update"),
    path("settings/profile/", views.EditProfile, name="user_profile_update"),
    path("settings/user/", views.account_update, name="user_update"),
    path("settings/user/delete/<int:pk>/", views.UserDeleteView.as_view(), name="user_delete"),
    re_path(r"^(?P<username>\w+)/$", views.profile, name="user_profile"),
]