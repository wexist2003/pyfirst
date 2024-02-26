from django.contrib import admin
from django.urls import path

from .apps import AppInstagramConfig
from . import views

# app_name = AppInstagramConfig.name
app_name = "app_instagram"

urlpatterns = [
    path("", views.main, name = "root"),
]
