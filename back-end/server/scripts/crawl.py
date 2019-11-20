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

def getTitle(entry):
    title = entry['title']
    title = title[:title.rfind("(")-1]
    return title

def getAuthors(entry):
    authors = entry['authors'][0]['name']
    soup = BeautifulSoup(authors, 'html.parser')
    authors = soup.findAll('a')
    texts = []
    for author in authors:
        texts.append(author.getText())
    return texts

def getLink(entry):
    return entry['link']

def getAbstract(entry):
    summary = entry['summary']
    soup = BeautifulSoup(summary, 'html.parser')
    abstract = soup.findAll(text=True)[0]
    return abstract

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
    page = requests.get(url)
    result = page.json()
    citations = result['citations']
    references = result['references']
    return [citations, references]

# Returns both citations and references
def getProphyCitations(articleId):
    url = 'https://www.prophy.science/api/arxiv/{}?include_unknown_references=1'
    url = url.format(articleId)
    page = requests.get(url)
    result = page.json()
    citations = result['citations']
    references = result['references']
    return [citations, references]

def getAuthorInfo(articleId, driver):
    url = 'https://www.prophy.science/api/arxiv/{}?include_unknown_references=1'
    url = url.format(articleId)
    page = requests.get(url)
    result = page.json()
    authors = result['authors']
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

        affiliation = soup.find('ul', {'class': 'affiliations'}).find('li').text
        affiliation = affiliation[:affiliation.find(',')]

        hIndex = soup.find('h4', {'title': 'for our collection'}).text
        hIndex = hIndex[hIndex.find(':') + 2:]

        interestsTable = soup.find('div', {'class': 'top-concepts-chart'}).findAll('tr')
        interests = []
        for tr in interestsTable:
            interests.append(tr.find('td').text)

        authorResults.append({'name': name, 'affiliation': affiliation, 'hIndex': hIndex, 'interests': interests})
    return authorResults

def insertArticle(title, authors, link, abstract, citations):
    # ArticleId, PrimaryAuthorId, CitedBy, Citations, Title, Year, Url, Publisher, Journal
    # Author (AuthorId, Name, Affiliation, CitedBy, Email, h-index, i10-index)
     with connection.cursor() as cursor:
        #  ArticleId, PrimaryAuthorId, CitedBy, Citations, Title, Year, Url, Publisher, Journal
        cursor.execute("INSERT INTO Article (PrimaryAuthorId, CitedBy, Citations, Title, Year, Url, Publisher, Journal) Values (%s, %s, %s, %s, %s, %s, %s, %s)",
                       [PrimaryAuthorId, CitedBy, Citations, Title, Year, Url, Publisher, Journal])

def run():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(chrome_options=chrome_options)

    feed = feedparser.parse(URL_NAME + 'econ')
    numEntries = len(feed['entries'])
    entry = feed['entries'][numEntries-1]

    # Get article info
    title = getTitle(entry)
    authorNames = getAuthors(entry)
    link = getLink(entry)
    abstract = getAbstract(entry)

    articleId = entry['id']
    articleId = articleId[articleId.rfind("/")+1:]
    citations = getCitationsAndReferences(articleId)
    
    # Get author info
    authorInfo = getAuthorInfo(articleId, driver)
    print(authorInfo)
    insertArticle(title, authorInfo, link, abstract, citations)