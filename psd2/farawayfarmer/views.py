from django.http import HttpResponse
from django.template import loader

from .models import Plant
import random

def index(request):
    template = loader.get_template("index.html")
    context = {}
    if not Plant.objects.all():
        for i in range(10):
            p = Plant(name="test{}".format(i), last_watered="2021-01-01", water_level=random.randint(0, 100), floor_level=random.randint(0, 5))
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