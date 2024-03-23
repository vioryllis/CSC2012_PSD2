from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
import requests
from django.http import JsonResponse
from .models import User, Plant, SensorData
import random
import json
from django.views.decorators.csrf import csrf_exempt

def register(request):
    if request.method == 'POST':
        # Retrieve form data
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        floor = request.POST.get('floor')
        
        # Check if user already exists
        if User.objects.filter(email=email).exists():
            error_message = "Email already registered."
            return render(request, 'register.html', {'error_message': error_message})
        
        # Use the custom user manager to create a new user
        try:
            user = User.objects.create_user(email=email, name=name, password=password, floor=floor)
        except ValueError as e:
            error_message = str(e)
            return render(request, 'register.html', {'error_message': error_message})
        
        return redirect('login')
        
    else:
        # If it's a GET request, just display the registration form
        return render(request, 'register.html')
    
def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('plants')
        else:
            error_message = "Invalid email or password."
            return render(request, 'login.html', {'error_message': error_message})
    else:
        return render(request, 'login.html')
    
def logout_view(request):
    logout(request)
    return redirect('login')

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


@csrf_exempt
def call_water_plant(request):
    url = "http://localhost:8000/api/water_plant/"
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            plantId = data.get('plant.plant_id')
            data = {"plant_id": plantId}
            response = requests.post(url, json=data)
            print("Success plant ", plantId)
            if response.status_code == 200:
                print("POST SUCCESS FROM PSD2: ", response)
                return JsonResponse(response.json())
            else:
                return JsonResponse({"error": "Failed to call water_plant in on api side"}, status=response.status_code)
        except json.JSONDecodeError as e:
            return JsonResponse({"error": "Invalid JSON data"}, status=400)
    else:
        print("post not working")
        return JsonResponse({"error": "Invalid request method"}, status=405)

    # data = {"plant_id": "1"}
    
    # # Make the POST request
    # response = requests.post(url, json=data)
    
    # if response.status_code == 200:
    #     print("POST SUCCESS FROM PSD2: ", response)
    #     return JsonResponse(response.json())
    # else:
    #     return JsonResponse({"error": "Failed to call water_plant in on api side"}, status=response.status_code)

def call_fertilize_plant(request):
    url = "http://localhost:8000/api/fertilize_plant/"

    data = {"plant_id": "1"}
    
    # Make the POST request
    response = requests.post(url, json=data)
    
    if response.status_code == 200:
        print("POST SUCCESS FROM PSD2: ", response)
        return JsonResponse(response.json())
    else:
        return JsonResponse({"error": "Failed to call fertilize_plant in on api side"}, status=response.status_code)
    
@csrf_exempt
def update_plant_settings(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            plant_id = data['plant_id']
            min_water_level = data['min_water_level']
            amt_to_water = data['amt_to_water']

            # Find the plant and update its settings
            plant, created = Plant.objects.update_or_create(
                plant_id=plant_id,
                defaults={
                    'min_water_level': min_water_level,
                    'amt_to_water': amt_to_water
                }
            )

            # Check and water the plant if necessary
            check_and_water_plant(plant)

            return JsonResponse({"status": "success", "message": "Plant settings updated and checked successfully"})
        except Plant.DoesNotExist:
            return JsonResponse({"status": "error", "message": "Plant not found"}, status=404)
        except KeyError as e:
            return JsonResponse({"status": "error", "message": f"Missing key in request data: {str(e)}"}, status=400)
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=500)
    else:
        return JsonResponse({"status": "error", "message": "Only POST requests are allowed"}, status=405)

def check_and_water_plant(plant):
    current_water_level = get_current_water_level_for_plant(plant.plant_id)
    if current_water_level < plant.min_water_level:
        response = water_plant(plant)
        print(f"Action taken for plant {plant.plant_id}: {response}")
    else:
        print(f"No action needed for plant {plant.plant_id}")

def water_plant(plant):
    data_to_send_over = {
        "plant_id": plant.plant_id,
        "amount_to_water": str(plant.amt_to_water)
    }
    url = "http://localhost:8000/api/water_plant_amt/"
    try:
        response = requests.post(url, json=data_to_send_over)
        return {"status_code": response.status_code, "message": "Request sent"}
    except Exception as e:
        return {"status_code": 500, "message": str(e)}

def get_current_water_level_for_plant(plant_id):
    # Get the plant by ID
    plant = get_object_or_404(Plant, pk=plant_id)

    # Query the SensorData entry with the largest sensor_data_id for the given plant
    latest_sensor_data = SensorData.objects.filter(plant=plant).order_by('-sensor_data_id').first()

    if latest_sensor_data:
        return latest_sensor_data.water_level
    else:
        return None