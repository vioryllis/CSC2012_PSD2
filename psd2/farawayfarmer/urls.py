from django.urls import path

from . import views

urlpatterns = [
    # path("", views.index, name="index"),
    path("", views.dashboard, name="dashboard"),
    path("register", views.register, name="register"),
    path("login", views.login_view, name="login"),
    path('logout/', views.logout_view, name='logout'),
    path('add-plant/', views.add_plant, name='add_plant'),
    path('plants/update-name/<int:plant_id>/', views.update_plant_name, name='update_plant_name'),
    path('plants/update-public/<int:plant_id>/', views.update_plant_public, name='update_plant_public'),
    path('delete_plant/<int:plant_id>/', views.delete_plant, name='delete_plant'),
    path("plants", views.plants, name="plants"),
    path("plants/<int:plant_id>", views.plant, name="plant"),
    path('dashboard/', views.dashboard, name='dashboard'),

    # for testings
    path("plants/call_water_plant/", views.call_water_plant, name="call_water_plant"),
    path("plants/call_fertilize_plant/", views.call_fertilize_plant, name="call_fertilize_plant"),
    path("plants/update_plant_settings/", views.update_plant_settings, name="update_plant_settings"),
]