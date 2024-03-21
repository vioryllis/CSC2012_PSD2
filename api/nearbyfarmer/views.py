from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import requests
from django.views.decorators.http import require_GET

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
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            print("LALALAL", data)
            plant_id = data.get('plant_id')
            return JsonResponse({"message": "Watering plant " + plant_id + "!"})
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
    else:
        return JsonResponse({"error": "Only POST method is accepted."}, status=405)


@csrf_exempt
def fertilize_plant(request):
    if request.method == 'POST':
        plant_id = request.data.get('plant_id')
        data = {"message": "Fertilizing plant " + plant_id + "!"}
        return JsonResponse(data)

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