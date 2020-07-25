from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:entry>", views.entry, name="entry"),
    path("search_result/", views.search, name="search"),
    path("new_wiki/", views.new_wiki, name="new_wiki"),
    path("wiki/<str:entry>/edit", views.edit_entry, name="edit_entry"),
    path("random/", views.random, name="random")
]
