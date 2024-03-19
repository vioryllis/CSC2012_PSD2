from django.http import HttpResponse
from django.template import loader

from .models import User, Plant
import random

def index(request):
    template = loader.get_template("dashboard.html")
    context = {}
    if not User.objects.all():
        u = User(name="user", email="user@mail.com", password="password", floor="floor")
        u.save()
    
    if not Plant.objects.all():
        for i in range(10):
            p = Plant(name="Plant {}".format(i), 
                      floor="{}".format(random.choice(["1", "2", "3", "4", "5"])), 
                      public=True, 
                      auto_system=random.choice([True, False]), 
                      min_water_level=random.uniform(0, 100), 
                      amt_to_water=random.uniform(0, 100), 
                      user=User.objects.all()[0])
            p.save()
    return HttpResponse(template.render(context, request))

def plants(request):
    template = loader.get_template("plants.html")
    plants = {}
    # sort plants by floor
    for plant in Plant.objects.all():
        if plant.floor not in plants:
            plants[plant.floor] = []
        plants[plant.floor].append(plant)
    
    # Sort the plants by floor
    context = {
        "plants": dict(sorted(plants.items(), key=lambda x: x[0])),
    }
    return HttpResponse(template.render(context, request))

def plant(request, plant_id):
    template = loader.get_template("plant.html")
    context = {
        "plant": Plant.objects.get(pk=plant_id),
    }
    return HttpResponse(template.render(context, request))