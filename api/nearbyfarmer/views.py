from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import requests
from django.views.decorators.http import require_GET

last_message_water = None
last_message_fertilize = None

@csrf_exempt
def receive_data(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        print("data from m5stick: ", data)
        
        return JsonResponse({"status": "success", "data": data})
    else:
        return JsonResponse({"status": "error", "message": "Only POST requests are allowed"})


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
            amount_to_water = data.get('amt_to_water')
            last_message_water = "Watering plant " + plant_id + " with " + amount_to_water + "ml!"
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

@csrf_exempt
def toggle_auto_system(request):
    if request.method == "POST":
        # TODO: 
        on_or_off = request.data.get('on_or_off')
        
        if on_or_off:
            # Data to send to M5Stick
            data_to_m5stick = {"message": "Request to turn on auto watering system"}
            
            # URL of the M5Stick endpoint
            m5stick_url = "http://m5stick_ip_address/api/receive_data"
            
            # Send data to M5Stick
            response_to_m5stick = requests.post(m5stick_url, json=data_to_m5stick)
            
            if response_to_m5stick.status_code == 200:
                return JsonResponse({"status": "success", "message": "Data sent to M5Stick successfully"})
            else:
                return JsonResponse({"status": "error", "message": "Failed to send data to M5Stick"}, status=500)
        else:
             # Data to send to M5Stick
            data_to_m5stick = {"message": "Request to turn off auto watering system"}
            
            # URL of the M5Stick endpoint
            m5stick_url = "http://m5stick_ip_address/api/receive_data"
            
            # Send data to M5Stick
            response_to_m5stick = requests.post(m5stick_url, json=data_to_m5stick)
            
            if response_to_m5stick.status_code == 200:
                return JsonResponse({"status": "success", "message": "Data sent to M5Stick successfully"})
            else:
                return JsonResponse({"status": "error", "message": "Failed to send data to M5Stick"}, status=500)