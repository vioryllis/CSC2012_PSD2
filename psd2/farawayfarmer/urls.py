from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("plants", views.plants, name="plants"),
    path("plants/<int:plant_id>", views.plant, name="plant"),
]