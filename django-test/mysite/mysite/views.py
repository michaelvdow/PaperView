from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.db import connection
from django.views.decorators.csrf import csrf_exempt
import json

# Create your views here.

def index(request):
    return HttpResponse("this is the MAIN PAGE")

def infodump(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT name FROM Example ORDER BY name")
        sql_response = cursor.fetchall()
    output = ', '.join([row[0] for row in sql_response])
    return HttpResponse(output)

@csrf_exempt
def echopostdata(request):
    return HttpResponse(request.body)

@csrf_exempt
def tothelimit(request):
    request_dict = json.loads(request.body)
    if request_dict['come on'] == 'fhqwgads':
        response_dict = {'everybody': 'to the limit!'}
    else:
        response_dict = {'everybody': 'SAD'}

    return JsonResponse(response_dict)
