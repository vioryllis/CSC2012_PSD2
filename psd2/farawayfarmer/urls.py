from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login, name="login"),
    path("plants", views.plants, name="plants"),
    path("plants/<int:plant_id>", views.plant, name="plant"),

    # for testings
    path("plants/call_water_plant/", views.call_water_plant, name="call_water_plant"),
    path("plants/call_fertilize_plant/", views.call_fertilize_plant, name="call_fertilize_plant"),
]