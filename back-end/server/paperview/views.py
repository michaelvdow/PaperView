from django.http import HttpResponse, JsonResponse
from django.db import connection
from django.views.decorators.csrf import csrf_exempt
import json

# Create your views here.

# Actual views
def search_for_author(request):
    name = request.GET['name']
    search_string = build_search_string(name)
    with connection.cursor() as cursor:
        cursor.execute("SELECT AuthorId, Name, Affiliation, CitedBy, "
                       "HIndex, I10Index FROM Author WHERE Name LIKE %s",
                       [search_string])
        rows = cursor.fetchall()

    author_list = []
    for row in rows:
        author_dict = {
            'AuthorId': row[0],
            'Name': row[1],
            'Affiliation': row[2],
            'CitedBy': row[3],
            'HIndex': row[4],
            'I10Index': row[5]
        }
        author_list.append(author_dict)

    response = { 'result': 'SUCCESS', 'Authors': author_list }
    return JsonResponse(response)

def search_for_article(request):
    name = request.GET['title']
    search_string = build_search_string(name)
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM Article WHERE Title LIKE %s LIMIT 20",
                       [search_string])
        rows = cursor.fetchall()

    author_list = []
    for row in rows:
        author_dict = {
            'ArticleId': row[0],
            'PrimaryAuthorId': row[1],
            'CitedBy': row[2],
            'Citations': row[3],
            'Title': row[4],
            'Year': row[5],
            'Url': row[6],
            'Publisher': row[7],
            'Journal': row[8]
        }
        author_list.append(author_dict)

    response = { 'result': 'SUCCESS', 'Articles': author_list }
    return JsonResponse(response)

@csrf_exempt
def specific_author(request, authorid):
    if request.method == "DELETE": 
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM Author WHERE authorid = %s",
                            [authorid])
            rows = cursor.fetchall()
        response = { 'result': 'SUCCESS'}
        return JsonResponse(response)
    return HttpResponse('stub')

@csrf_exempt
def specific_article(request, articleid):
    if request.method == "DELETE":
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM Article WHERE articleid = %s",
                            [articleid])
        response = { 'result': 'SUCCESS'}
        return JsonResponse(response)
    elif request.method == "POST":
        body = json.loads(request.body)
        print(body)
        with connection.cursor() as cursor:
            cursor.execute("UPDATE Article SET PrimaryAuthorId = %s, CitedBy = %s, Citations = %s, Title = %s, Year = %s, Url = %s, Publisher = %s, Journal = %s WHERE articleid = %s", 
            [body['PrimaryAuthorId'], body['CitedBy'], body['Citations'], body['Title'], body['Year'], body['Url'], body['Publisher'], body['Journal'], articleid])
        response = { 'result': 'SUCCESS'}
        return JsonResponse(response)

    return HttpResponse('stub')

def new_author(request):

    return HttpResponse('stub')

def new_article(request):
    return HttpResponse('stub')

def index(request):
    return HttpResponse("This will serve the react page.")


# Test views

def listnames(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT name FROM test ORDER BY name")
        sql_response = cursor.fetchall()
    output = ', '.join([row[0] for row in sql_response])
    return HttpResponse(output)

def searchForName(request):
    name = request.GET['name']
    #search_string = '%'.join(name.split(' '))
    #search_string = '%'.join(search_string.split('.'))
    #search_string = '%' + search_string + '%'
    search_string = build_search_string(name)
    with connection.cursor() as cursor:
        cursor.execute("SELECT name FROM test WHERE name LIKE %s",
                       [search_string])
        sql_response = cursor.fetchall()
    output = ', '.join([row[0] for row in sql_response])
    return HttpResponse(output)

@csrf_exempt
def addname(request):
    new_name = json.loads(request.body)['name']
    with connection.cursor() as cursor:
        cursor.execute("INSERT INTO test(name) VALUES (%s)", [new_name])
    return JsonResponse({'result':'SUCCESS'})

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

# Helper functions
def build_search_string(typed_input):
    search_string = '%'.join(typed_input.split(' '))
    search_string = '%'.join(search_string.split('.'))
    search_string = '%' + search_string + '%'
    return search_string
