"""
URL configuration for awm_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path, include
from awm_app.views import manifest, offline, service_worker,get_user_locations, update_location, get_pubs_in_location, get_current_user, update_group, get_vote_values, delete_group
from django.views.generic.base import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),
    re_path(r"^serviceworker\.js$", service_worker, name="serviceworker"),
    re_path(r"^manifest\.json$", manifest, name="manifest"),
    path("offline/", offline, name="offline"),
    path("", TemplateView.as_view(template_name="new_index.html"), name="index"),
    path('get_user_locations/', get_user_locations, name='get_user_locations'),
    path('update_location/', update_location, name='update_location'),
    path('get_pubs_in_location/', get_pubs_in_location, name='get_pubs_in_location'),
    path('get_current_user/', get_current_user, name='get_current_user'),
    path('update_group/', update_group, name='update_group'),
    path('get_vote_values/', get_vote_values, name='get_vote_values'),
    path('delete_group/', delete_group, name='delete_group'),
]
