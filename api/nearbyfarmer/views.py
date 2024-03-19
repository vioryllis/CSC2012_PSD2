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

@require_GET
def send_data(request):
    data = {"message": "WATER YOUR PLANT NOW"}
    return JsonResponse(data)
