from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import requests
from django.views.decorators.http import require_GET
from .models import SensorData, Plant

last_message_water = None
last_message_fertilize = None

@csrf_exempt
def receive_data(request):
    if request.method == 'POST':
        try:
            # Parse the incoming JSON data
            data = json.loads(request.body.decode('utf-8'))
            print("data from m5stick: ", data)

            # Extract sensor data and plant_id from the incoming data
            water_level = data['water_level']
            nutrient_level = data['nutrient_level']
            plant_id = data['plant_id']

            sensor_data_table_name = SensorData._meta.db_table
            plant_table_name = Plant._meta.db_table
            print(f"Accessing SensorData database table: {sensor_data_table_name}")
            print(f"Accessing Plant database table: {plant_table_name}")
            
            # Retrieve the plant instance associated with plant_id
            plant = Plant.objects.get(pk=plant_id)
            
            # Create a new SensorData instance and save it to the database
            sensor_data = SensorData(
                water_level=water_level,
                nutrient_level=nutrient_level,
                plant=plant
            )
            sensor_data.save()
            
            return JsonResponse({"status": "success", "message": "Sensor data saved successfully"})
        except KeyError as e:
            return JsonResponse({"status": "error", "message": f"Missing field in request data: {str(e)}"}, status=400)
        except Plant.DoesNotExist:
            return JsonResponse({"status": "error", "message": "Plant not found"}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({"status": "error", "message": "Invalid JSON format"}, status=400)
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=500)
    else:
        return JsonResponse({"status": "error", "message": "Only POST requests are allowed"}, status=405)


@csrf_exempt
def water_plant(request):
    global last_message_water

    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            plant_id = data.get('plant_id')
            last_message_water = "Watering plant " + plant_id + "!"
            return JsonResponse({"message": last_message_water})
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
    elif request.method == 'GET':
        if last_message_water is not None:
            response = JsonResponse({"message": last_message_water})
            print("GET SUCCESS: ", last_message_water)
            last_message_water = None  # Clear the message after sending
            return response
        else:
            return JsonResponse({"error": "No recent watering action found."}, status=404)
    else:
        return JsonResponse({"error": "Only POST and GET methods are accepted."}, status=405)


@csrf_exempt
def fertilize_plant(request):
    global last_message_fertilize

    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            plant_id = data.get('plant_id')
            last_message_fertilize = "Fertilizing plant " + plant_id + "!"
            return JsonResponse({"message": last_message_fertilize})
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
    elif request.method == 'GET':
        if last_message_fertilize is not None:
            response = JsonResponse({"message": last_message_fertilize})
            print("GET SUCCESS: ", last_message_fertilize)
            last_message_fertilize = None  # Clear the message after sending
            return response
        else:
            return JsonResponse({"error": "No recent fertilizing action found."}, status=404)
    else:
        return JsonResponse({"error": "Only POST and GET methods are accepted."}, status=405)

@csrf_exempt
def water_plant_amt(request):
    global last_message_water

    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            plant_id = data.get('plant_id')
            amount_to_water = data.get('amount_to_water')
            last_message_water = "Watering plant " + str(plant_id) + " with " + amount_to_water + "ml!"
            return JsonResponse({"message": last_message_water})
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
    elif request.method == 'GET':
        if last_message_water is not None:
            response = JsonResponse({"message": last_message_water})
            print("GET SUCCESS: ", last_message_water)
            last_message_water = None  # Clear the message after sending
            return response
        else:
            return JsonResponse({"error": "No recent watering (amt) action found."}, status=404)
    else:
        return JsonResponse({"error": "Only POST and GET methods are accepted."}, status=405)