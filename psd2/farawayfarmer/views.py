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
            p = Plant(name="test{}".format(i), 
                      floor="{}".format(i), 
                      public=True, 
                      auto_system=random.choice([True, False]), 
                      min_water_level=random.uniform(0, 100), 
                      amt_to_water=random.uniform(0, 100), 
                      user=User.objects.all()[0])
            p.save()
    return HttpResponse(template.render(context, request))

def plants(request):
    template = loader.get_template("plants.html")
    context = {
        "plants": Plant.objects.all(),
    }
    return HttpResponse(template.render(context, request))

def plant(request, plant_id):
    template = loader.get_template("plant.html")
    context = {
        "plant": Plant.objects.get(pk=plant_id),
    }
    return HttpResponse(template.render(context, request))