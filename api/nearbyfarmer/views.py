from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
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
        plant_id = request.data.get('plant_id')
        data = {"message": "Watering plant " + plant_id + "!"}
        return JsonResponse(data)

@csrf_exempt
def fertilize_plant(request):
    if request.method == 'POST':
        plant_id = request.data.get('plant_id')
        data = {"message": "Fertilizing plant " + plant_id + "!"}
        return JsonResponse(data)
