from django.shortcuts import render
from django.http import HttpResponse
from django.db import connection

# Create your views here.

def index(request):
    return HttpResponse("Hello, Dad! Hello, Mom! ch-ch-ch-ch-ch-ch-ch-ch-CHERRY BOMB!")

def infodump(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT name FROM Example ORDER BY name")
        sql_response = cursor.fetchall()
    output = ', '.join([row[0] for row in sql_response])
    return HttpResponse(output)
