from django.http import HttpResponse, JsonResponse
from django.db import connection
from django.views.decorators.csrf import csrf_exempt
import json
from . import graph_driver

graph_conn = graph_driver.Neo4jConnector()

# was going to use these but didn't, might be useful so I'm leaving them here
AUTHOR_ATTRIBUTES = ['Name', 'Affiliation', 'CitedBy', 'HIndex', 'I10Index']
ARTICLE_ATTRIBUTES = ['ArticleId', 'PrimaryAuthorId', 'CitedBy', 'Citations',
                      'Title', 'Year', 'Url', 'Publisher', 'Journal']

# Create your views here.

# Actual views
@csrf_exempt
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

@csrf_exempt
def search_for_article(request):
    name = request.GET['title']
    search_string = buildArticleSearch(name)
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM Article WHERE MATCH(Title) AGAINST(%s IN NATURAL LANGUAGE MODE) LIMIT 100",
                       [name])
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
def search_for_interest(request):
    interest = request.GET['interest']
    search_string = build_search_string(interest)
    with connection.cursor() as cursor:
        cursor.execute(	"SELECT AuthorId, Name, MAX(Interest) AS Interest "
                        "FROM Author NATURAL JOIN InterestedIn "
                        "WHERE Interest LIKE %s "
                        "GROUP BY AuthorId "
                        "ORDER BY Name",
                        [search_string])
        rows = cursor.fetchall()

    interest_list = []
    for row in rows:
        #TODO: make a proper dict as above
        interest_list.append(row[0])

    response = { 'result': 'SUCCESS', 'Authors': interest_list }
    return JsonResponse(response)

@csrf_exempt
def specific_author(request, authorid):
    if request.method == "DELETE":   # delete author
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM Author WHERE authorid = %s",
                            [authorid])
        response = { 'result': 'SUCCESS'}
        return JsonResponse(response)
    elif request.method == "POST":   # update author
        body = json.loads(request.body)
        with connection.cursor() as cursor:
            cursor.execute("UPDATE Author SET Name=%s, "
                           "Affiliation=%s, CitedBy=%s, HIndex=%s, I10Index=%s "
                           "WHERE authorid = %s",
                           [body['Name'], body['Affiliation'], body['CitedBy'],
                            body['HIndex'], body['I10Index'], authorid])
        graph_conn.update_author_name(authorid, body['Name'])
        response = { 'result': 'SUCCESS'}
        return JsonResponse(response)
# TODO: write method for GET (i.e. specific author page)
    elif request.method == "GET":   # view author
        res = { 'result': 'SUCCESS'}
        with connection.cursor() as cursor:
            cursor.execute("SELECT AuthorId, Name, Affiliation, CitedBy, "
                           "HIndex, I10Index FROM Author "
                           "WHERE AuthorId = %s", [authorid])
            basic_info = cursor.fetchone()
            res['AuthorId'], res['Name'], res['Affiliation'], res['CitedBy'], \
                res['HIndex'], res['I10Index'] = basic_info

            cursor.execute("SELECT Interest FROM InterestedIn "
                           "WHERE AuthorId = %s", [authorid])
            interest_raw = cursor.fetchall()
            res['Interests'] = []
            for interest_tuple in interest_raw:
                res['Interests'].append(interest_tuple[0])

        res['Articles'] = graph_conn.get_articles_written_by(authorid)

        # TODO: get graph data to display

        return JsonResponse(res)
    return HttpResponse('stub')

@csrf_exempt
def specific_article(request, articleid):
    if request.method == "DELETE":  # Delete article
        print(request.method)
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM Article WHERE ArticleId = %s",
                            [articleid])
        print("Executed")
        response = { 'result': 'SUCCESS'}
        return JsonResponse(response)
    elif request.method == "POST":   # Update article
        body = json.loads(request.body)
        print(body)
        with connection.cursor() as cursor:
            cursor.execute("UPDATE Article SET PrimaryAuthorId = %s, "
                           "CitedBy = %s, Citations = %s, Title = %s, "
                           "Year = %s, Url = %s, Publisher = %s, Journal = %s "
                           "WHERE articleid = %s",
                           [body['PrimaryAuthorId'], body['CitedBy'],
                            body['Citations'], body['Title'], body['Year'],
                            body['Url'], body['Publisher'], body['Journal'],
                            articleid])

        graph_conn.update_article_title(articleid, body['Title'])
        response = { 'result': 'SUCCESS'}
        return JsonResponse(response)

# TODO: write method for GET (i.e. specific article page)
    return HttpResponse('stub')

@csrf_exempt
def new_author(request):
    #print(request.body)
    author = json.loads(request.body)
    with connection.cursor() as cursor:
        cursor.execute("INSERT INTO Author"
                       "(Name, Affiliation, CitedBy, HIndex, I10Index) "
                       "VALUES (%s, %s, %s, %s, %s)",
                       [
                           author['Name'],
                           author['Affiliation'],
                           author['CitedBy'],
                           author['HIndex'],
                           author['I10Index']
                       ])
        cursor.execute("SELECT LAST_INSERT_ID()")
        new_id = cursor.fetchone()[0] # Integer AuthorId of newly inserted author

        interests = author['Interests'] # array of strings
        for interest in interests:
            # Insert a new row into InterestedIn with the author ID (new_id)
            # and the interest (interest)
            cursor.execute("INSERT INTO InterestedIn(AuthorId, Interest) VALUES (%s, %s)", [new_id, interest])


    graph_conn.insert_new_author(new_id, author['Name'])
    return JsonResponse({'result': 'SUCCESS', 'AuthorId': new_id})

@csrf_exempt
def new_article(request):
    article = json.loads(request.body)
    try:
        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO Article"
                           "(Title, PrimaryAuthorId, CitedBy, Citations, Year, "
                           "Url, Publisher, Journal) "
                           "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                           [
                               article['Title'],
                               article['PrimaryAuthorId'],
                               article['CitedBy'],
                               article['Citations'],
                               article['Year'],
                               article['Url'],
                               article['Publisher'],
                               article['Journal']
                           ])
            cursor.execute("SELECT LAST_INSERT_ID()")
            new_id = cursor.fetchone()[0]
        graph_conn.insert_new_article(new_id, article['Title'], article['Authors'])
    except Exception as e:
        print(e) # debug
        return JsonResponse({'result':'FAILURE', 'error': str(e)})
    return JsonResponse({'result': 'SUCCESS', 'ArticleId': new_id})

def index(request):
    return HttpResponse("This will serve the react page.")


# Test views

def graphTest(request):
    #graph_conn.print_greeting(request.GET['message'])
    result = graph_conn.return_greeting(request.GET['message'])
    return HttpResponse(result)

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

def buildArticleSearch(input):
    return ','.join(input.split(' '))
