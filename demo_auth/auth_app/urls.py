from django.urls import re_path, path
from auth_app import views

urlpatterns = [
    path("", views.base_form, name="base-form"),
    path("land/", views.land_form, name="form-submit"),
    path("poll/", views.is_authed, name="poller"),
    path("interm/", views.inter_state, name="interm"),
]
