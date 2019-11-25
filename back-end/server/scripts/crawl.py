# AF1: Crawling ARXIV/other sites to automatically add new articles
# Use arxiv RSS feed
# Get and parse XML, and insert all new articles into the database
# Uses a trigger by incrementing the number of articles an author has written
# A column for the number of author articles can be created in the authors database
# OR: Parse the citations, and use a trigger/stored procedure to update the cited by numbers of 
# the articles it cites (and for authors of those articles?).
# Would have to add a table for particular citations
# This would also let us beef up our connections display by showing citation links and not just coauthor links

# Run using: python3 manage.py runscript crawl
# Needs chromedriver and installed requirements.txt
import feedparser
import pprint
from bs4 import BeautifulSoup
from bs4.element import Comment
import requests
from django.db import connection
from time import sleep

from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

ARCHIVE_NAMES = ['astro-ph', 'cond-mat', 'cs', 'econ', 'eess', 'gr-qc', 'hep-ex', 'hep-lat', 'hep-ph', 'hep-th', 'math', 'math-ph', 'nlin', 'nucl-ex', 'nucl-th', 'physics', 'q-bio', 'q-fin', 'quant-ph', 'stat']
URL_NAME = 'http://export.arxiv.org/rss/'

# Returns title: String
def getTitle(entry):
    title = entry['title']
    title = title[:title.rfind("(")-1]
    return title

# Returns author: String
def getAuthors(entry):
    authors = entry['authors'][0]['name']
    soup = BeautifulSoup(authors, 'html.parser')
    authors = soup.findAll('a')
    texts = []
    for author in authors:
        texts.append(author.getText())
    return texts

# Returns link: String
def getLink(entry):
    return entry['link']

# Returns abstract: String
def getAbstract(entry):
    summary = entry['summary']
    soup = BeautifulSoup(summary, 'html.parser')
    abstract = soup.findAll(text=True)[0]
    return abstract

# Returns [citations, references]
# where citations, references = [{authors: [authorId, name, url], title: String, url: String, year: Int}]
# References = publications referenced by this paper
# Citations = publications citing this paper
def getCitationsAndReferences(articleId):
    semanticResults = getSemanticScholarCitations(articleId)
    prophyResults = getProphyCitations(articleId)
    result = semanticResults
    result[0].extend(prophyResults[0])
    result[1].extend(prophyResults[1])
    return result

# Returns both citations and references
def getSemanticScholarCitations(articleId):
    url = 'https://api.semanticscholar.org/v1/paper/arXiv:{}?include_unknown_references=true'
    url = url.format(articleId)
    try:
        page = requests.get(url)
        result = page.json()
        citations = result['citations']
        references = result['references']
        return [citations, references]
    except:
        return [[], []]

# Returns both citations and references
def getProphyCitations(articleId):
    url = 'https://www.prophy.science/api/arxiv/{}?include_unknown_references=1'
    url = url.format(articleId)
    try:
        page = requests.get(url)
        result = page.json()
        citations = result['citations']
        references = result['references']
        return [citations, references]
    except:
        return [[], []]

def getYear(articleId):
    url = 'https://www.prophy.science/api/arxiv/{}?include_unknown_references=1'
    url = url.format(articleId)
    try:
        page = requests.get(url)
        result = page.json()
        year = result['year']
        return year
    except:
        return None
    

def getAuthorInfo(articleId, driver):
    url = 'https://www.prophy.science/api/arxiv/{}?include_unknown_references=1'
    url = url.format(articleId)
    page = requests.get(url)
    try:
        result = page.json()
        authors = result['authors']
    except:
        authors = []
    authorResults = []
    for author in authors:
        url = author['url'] + "/full"
        driver.get(url)
        timeout = 5
        try:
            element_present = EC.presence_of_element_located((By.CLASS_NAME, 'affiliations'))
            WebDriverWait(driver, timeout).until(element_present)
        except:
            continue
        html = driver.find_element_by_tag_name('html').get_attribute('innerHTML')
        soup = BeautifulSoup(html, 'html.parser')
        
        # Extract information from page
        name = soup.find('div', {'class': 'author'}).find('span').text

        affiliation = None
        try:
            affiliation = soup.find('ul', {'class': 'affiliations'}).find('li').text
            affiliation = affiliation[:affiliation.find(',')]
        except:
            pass

        hIndex = None
        try:
            hIndex = soup.find('h4', {'title': 'for our collection'}).text
            hIndex = hIndex[hIndex.find(':') + 2:]
        except:
            pass
        
        interests = []
        try: 
            interestsTable = soup.find('div', {'class': 'top-concepts-chart'}).findAll('tr')
            interests = []
            for tr in interestsTable:
                interests.append(tr.find('td').text)
        except:
            pass

        authorResults.append({'name': name, 'affiliation': affiliation, 'hIndex': hIndex, 'interests': interests})
    return authorResults

# Returns None if not found
def findAuthor(name, affiliation):
    cursor.execute("SELECT AuthorId, Name FROM Author WHERE Name = %s AND Affiliation LIKE %s", [name, '%' + affiliation + '%']) # TODO: maybe use fuzzy matching to find author? affiliation can be worded different
    row = cursor.fetchone()
    authorId = row[0] if len(row) > 0 else None
    return authorId

# Return None if not found
def findArticle(title):
    cursor.execute("SELECT Title FROM Article WHERE Title = %s", [title])
    row = cursor.fetchone()
    articleId = row[0] if len(row) > 0 else None
    return articleId

# Input:
# authors: [{name: String, affiliation: String, hIndex: Integer, interests: [interest: string]}]
# Returns primary author id
def insertAuthors(authors):
    primaryAuthorId = None
    with connection.cursor() as cursor:
        for author in authors:
            # Check if author exists:
            currentAuthorId = findAuthor(name, affiliation)
            if currentAuthorId != None:
                primaryAuthorId = currentAuthorId if primaryAuthorId == None else primaryAuthorId
            else: # Author does not exists in database
                cursor.execute("INSERT INTO Author (Name, Affiliation, CitedBy, HIndex, I10Index) VALUES (%s, %s, %s, %s, %s)", 
                                [author['name'], author['affiliation'] or None, None, author['hIndex'] or None, None])
                cursor.execute("SELECT LAST_INSERT_ID()")
                new_id = cursor.fetchone()[0]
                currentAuthorId = new_id
                primaryAuthorId = new_id if primaryAuthorId == None else primaryAuthorId
            # Insert interests
            if interests in author:
                for interest in author['interests']:
                    if interest != '':
                        cursor.execute("INSERT IGNORE INTO InterestedIn VALUES (%s, %s)", [currentAuthorId, interest])
    return primaryAuthorId

# TODO: Find journal or publisher
def insertArticle(title, primaryAuthorId, link, citations, year):
    with connection.cursor() as cursor:
        cursor.execute("INSERT INTO Article (PrimaryAuthorId, CitedBy, Citations, Title, Year, Url, Publisher, Journal) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", 
        [primaryAuthorId, len(citations[0]), len(citations[1]), title, year, link, None, None])
        cursor.execute("SELECT LAST_INSERT_ID()")
        new_id = cursor.fetchone()[0]
        return new_id

# Input:
# ArticleId, citations = [citations, references]
# References = publications referenced by this paper
# Citations = publications citing this paper
def insertCitations(articleId, citations):
    pprint.pprint(citations)
    with connection.cursor() as cursor:
        for citation in citations[1]: # Articles referenced by this paper
            otherArticleId = None
            # Check if article exists
            result = findArticle(citations['title'])
            if result == None:
                primaryAuthorId = insertAuthors(citations['authors'])
                otherArticleId = insertArticle(citation['title'], primaryAuthorId, citation['url'], None, citation['year'])
            else:
                otherArticleId = result[0]
            cursor.execute("INSERT IGNORE INTO Citation (Article, Cites) VALUES (%s, %s)",
            [articleId, otherArticleId])

        for citation in citations[0]: # Other articles that cited this paper
            otherArticleId = None
            # Check if article exists
            result = findArticle(citations['title'])
            if result == None:
                primaryAuthorId = insertAuthors(citations['authors'])
                otherArticleId = insertArticle(citation['title'], primaryAuthorId, citation['url'], None, citation['year'])
            else:
                otherArticleId = result[0]
            cursor.execute("INSERT IGNORE INTO Citation (Article, Cites) VALUES (%s, %s)",
            [otherArticleId, articleId])
    print("Citations Added")

# Input:
# title: String
# authors: [{name: String, affiliation: String, hIndex: Integer, interests: [interest: string]}]
# link: String
# citations = [citations, references]
# where citations, references = [{authors: [authorId, name, url], title: String, url: String, year: Int}]
def insertEntries(title, authors, link, citations, year):
    primaryAuthorId = insertAuthors(authors)
    articleId = insertArticle(title, primaryAuthorId, link, citations, year)
    insertCitations(articleId, citations)

def run():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome('/Users/michaelvdow/Documents/chromedriver', chrome_options=chrome_options) # Update to chromedriver path

    feed = feedparser.parse(URL_NAME + 'cs')
    numEntries = len(feed['entries'])
    print(numEntries)
    # entry = feed['entries'][numEntries-5]
    for entry in feed['entries']:
        # Get article info
        title = getTitle(entry)
        authorNames = getAuthors(entry)
        link = getLink(entry)

        articleId = entry['id']
        articleId = articleId[articleId.rfind("/")+1:]
        citations = getCitationsAndReferences(articleId)
        year = getYear(articleId)
        # Get author info
        authorInfo = getAuthorInfo(articleId, driver)

        # print(title)
        print(authorNames)
        # print(link)
        pprint.pprint(authorInfo)
        # print(year)
        # print('\n\n\n\n')
        insertEntries(title, authorInfo, link, citations, year)