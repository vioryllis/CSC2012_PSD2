from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.db.models import Avg
import requests
from django.http import JsonResponse
from .models import User, Plant, SensorData
import random
import json
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.core.serializers.json import DjangoJSONEncoder
from django.utils.safestring import mark_safe

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
    
@login_required 
def logout_view(request):
    logout(request)
    return redirect('login')

# @login_required 
# def index(request):
#     template = loader.get_template("dashboard.html")
#     context = {}
#     if not User.objects.all():
#         u = User(name="user", email="user@mail.com", password="password", floor="floor")
#         u.save()
    
#     if not Plant.objects.all():
#         for i in range(10):
#             p = Plant(name="Plant {}".format(i), 
#                       floor="{}".format(random.choice(["1", "2", "3", "4", "5"])), 
#                       public=True, 
#                       auto_system=random.choice([True, False]), 
#                       min_water_level=random.uniform(0, 100), 
#                       amt_to_water=random.uniform(0, 100), 
#                       user=User.objects.all()[0])
#             p.save()
#     return HttpResponse(template.render(context, request))

@login_required 
@csrf_exempt
def add_plant(request):
    if request.method == 'POST':
        # Get form data
        name = request.POST.get('plantName')
        is_public = request.POST.get('isPublic')
        user_id = request.user.user_id 
        floor = request.user.floor
        default_value = 50
        
        # Save plant to database
        plant = Plant.objects.create(
            name=name,
            floor=floor,
            public=is_public,
            min_water_level=default_value,
            amt_to_water=default_value,
            user_id=user_id,
        )
        
        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request method'})

@login_required
@csrf_exempt
def update_plant_name(request, plant_id):
    data = json.loads(request.body)
    try:
        plant = Plant.objects.get(pk=plant_id, user=request.user)
        plant.name = data.get('name')
        plant.save()
        return JsonResponse({"success": "Plant name updated successfully."})
    except Plant.DoesNotExist:
        return JsonResponse({"error": "Plant not found."}, status=404)

@login_required
@csrf_exempt
def update_plant_public(request, plant_id):
    data = json.loads(request.body)
    try:
        plant = Plant.objects.get(pk=plant_id, user=request.user)
        plant.public = data.get('public', False)
        plant.save()
        return JsonResponse({"success": "Plant public status updated successfully."})
    except Plant.DoesNotExist:
        return JsonResponse({"error": "Plant not found."}, status=404)

@login_required
def delete_plant(request, plant_id):
    try:
        plant = Plant.objects.get(pk=plant_id, user=request.user)
        plant.delete()
        return redirect('plants')  
    except Plant.DoesNotExist:
        return HttpResponse('Plant not found', status=404)

@login_required 
def plants(request):
    user_plants_only = 'true' == request.GET.get('user_plants', 'false').lower()
    
    if user_plants_only:
        plant_query = Plant.objects.filter(user=request.user)
    else:
        plant_query = Plant.objects.filter(public=True)
    
    plants = {}
    for plant in plant_query:
        if plant.floor not in plants:
            plants[plant.floor] = []
        plants[plant.floor].append(plant)
    
    context = {
        "plants": dict(sorted(plants.items(), key=lambda x: x[0])),
        "user_plants_only": user_plants_only,  # Pass this to the template to keep track of the current filter state
        "active_filter": "mine" if user_plants_only else "all",
    }
    return render(request, "plants.html", context)

@login_required 
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
            print("Success water plant ", plantId)
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

@csrf_exempt
def call_fertilize_plant(request):
    url = "http://localhost:8000/api/fertilize_plant/"
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            plantId = data.get('plant.plant_id')
            data = {"plant_id": plantId}
            response = requests.post(url, json=data)
            print("Success fertilize plant ", plantId)
            if response.status_code == 200:
                print("POST SUCCESS FROM PSD2: ", response)
                return JsonResponse(response.json())
            else:
                return JsonResponse({"error": "Failed to call fertilize_plant in on api side"}, status=response.status_code)
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
    #     return JsonResponse({"error": "Failed to call fertilize_plant in on api side"}, status=response.status_code)
    
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
    
@login_required 
def dashboard(request):
    # Filter plants by the current user
    user_plants = Plant.objects.filter(user=request.user)
    total_user_plants = user_plants.count()

    # Get average sensor data for the user's plants
    sensor_data_qs = SensorData.objects.filter(plant__in=user_plants).values('plant__name').annotate(
        avg_water_level=Avg('water_level'),
        avg_nutrient_level=Avg('nutrient_level')
    )

    # Prepare the data for the bar chart
    plant_names = [entry['plant__name'] for entry in sensor_data_qs]
    avg_water_levels = [entry['avg_water_level'] for entry in sensor_data_qs]
    avg_nutrient_levels = [entry['avg_nutrient_level'] for entry in sensor_data_qs]

    # Serialize the data to JSON strings
    plant_names_json = mark_safe(json.dumps(plant_names, cls=DjangoJSONEncoder))
    avg_water_levels_json = mark_safe(json.dumps(avg_water_levels, cls=DjangoJSONEncoder))
    avg_nutrient_levels_json = mark_safe(json.dumps(avg_nutrient_levels, cls=DjangoJSONEncoder))

    context = {
        'total_user_plants': total_user_plants,
        'user': request.user,
        'plant_names': plant_names_json,
        'avg_water_levels': avg_water_levels_json,
        'avg_nutrient_levels': avg_nutrient_levels_json,
    }
    print(context)
    return render(request, 'dashboard.html', context)