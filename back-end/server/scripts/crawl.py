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
import logging
import sys
from paperview import graph_driver
import traceback

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
    logging.info("Inside of getTitle")
    title = entry['title']
    title = title[:title.rfind("(")-1]
    logging.info("Finished getTitle")
    return title

# Returns author: String
def getAuthors(entry):
    logging.info("Inside of authors")
    authors = entry['authors'][0]['name']
    soup = BeautifulSoup(authors, 'html.parser')
    authors = soup.findAll('a')
    texts = []
    for author in authors:
        texts.append(author.getText())
    logging.info("Finished getAuthors")
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
    logging.info("Inside of getCitations")
    semanticResults = getSemanticScholarCitations(articleId)
    prophyResults = getProphyCitations(articleId)
    result = semanticResults
    result[0].extend(prophyResults[0])
    result[1].extend(prophyResults[1])
    logging.info("Finished getCitations")
    return result

# Returns both citations and references
def getSemanticScholarCitations(articleId):
    logging.info("Inside of getSemanticScholarCitations")
    url = 'https://api.semanticscholar.org/v1/paper/arXiv:{}?include_unknown_references=true'
    url = url.format(articleId)
    try:
        page = requests.get(url)
        result = page.json()
        citations = result['citations']
        references = result['references']
        logging.info("Finished getSemanticScholarCitations")
        return [citations, references]
    except:
        logging.error("Failed to get semantic citations")
        logging.info("Finished getSemanticScholarCitations")
        return [[], []]

# Returns both citations and references
def getProphyCitations(articleId):
    logging.info("Inside of getProphyCitations")
    url = 'https://www.prophy.science/api/arxiv/{}?include_unknown_references=1'
    url = url.format(articleId)
    try:
        page = requests.get(url)
        result = page.json()
        citations = result['citations']
        references = result['references']
        logging.info("Finished getProphyCitations")
        return [citations, references]
    except:
        logging.error("Failed to get prophy citations")
        logging.info("Finished getProphyCitations")
        return [[], []]

def getYear(articleId):
    logging.info("Inside getYear")
    url = 'https://www.prophy.science/api/arxiv/{}?include_unknown_references=1'
    url = url.format(articleId)
    try:
        page = requests.get(url)
        result = page.json()
        year = result['year']
        return year
    except:
        logging.error("Failed to get year")
        logging.info("Finished getYear")
        return None
    

def getAuthorInfo(articleId, driver):
    logging.info("Inside getAuthorInfo")
    url = 'https://www.prophy.science/api/arxiv/{}?include_unknown_references=1'
    url = url.format(articleId)
    page = requests.get(url)
    try:
        result = page.json()
        authors = result['authors']
    except:
        logging.error("Failed to get authors from Prophy: " + url)
        authors = []
    authorResults = []
    for author in authors:
        if author['url'] == None:
            continue
        url = author['url'] + "/full"
        driver.get(url)
        timeout = 5
        try:
            element_present = EC.presence_of_element_located((By.CLASS_NAME, 'affiliations'))
            WebDriverWait(driver, timeout).until(element_present)
        except:
            logging.error("Timed out of author url: " + url)
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
            logging.error("Failed to get affiliation")
            pass

        hIndex = None
        try:
            hIndex = soup.find('h4', {'title': 'for our collection'}).text
            hIndex = hIndex[hIndex.find(':') + 2:]
        except:
            logging.error("Failed to get hIndex")
            pass
        
        interests = []
        try: 
            interestsTable = soup.find('div', {'class': 'top-concepts-chart'}).findAll('tr')
            interests = []
            for tr in interestsTable:
                interests.append(tr.find('td').text)
        except:
            logging.error("Failed to get interests")
            pass
        authorResults.append({'name': name, 'affiliation': affiliation, 'hIndex': hIndex, 'interests': interests})
    logging.info("Finished getAuthorInfo")
    return authorResults

# Returns None if not found
def findAuthor(name, affiliation):
    logging.info("Inside findAuthor")
    with connection.cursor() as cursor:
        cursor.execute("SELECT AuthorId FROM Author WHERE Name = %s AND Affiliation = %s", [name, '%' + affiliation + '%']) # TODO: maybe use fuzzy matching to find author? affiliation can be worded different
        row = cursor.fetchone()
        authorId = row[0] if row != None else None
        logging.info("Finished findAuthor")
        return authorId

# Return None if not found
def findArticle(title, primaryAuthorId):
    logging.info("Inside findArticle")
    with connection.cursor() as cursor:
        cursor.execute("SELECT Title FROM Article WHERE PrimaryAuthorId = %s AND Title = %s", [primaryAuthorId, title])
        row = cursor.fetchone()
        articleId = row[0] if row != None else None
        logging.info("Finished findArticle")
        return articleId

# Input:
# authors: [{name: String, affiliation: String, hIndex: Integer, interests: [interest: string]}]
# Returns primary author id
def insertAuthors(authors, graphConn):
    logging.info("Inside insertAuthors")
    primaryAuthorId = None
    writers = []
    with connection.cursor() as cursor:
        for author in authors:
            # Check if author exists:
            currentAuthorId = None
            if 'affiliation' in author:
                currentAuthorId = findAuthor(author['name'], author['affiliation'])
            if currentAuthorId != None:
                primaryAuthorId = currentAuthorId if primaryAuthorId == None else primaryAuthorId
            else: # Author does not exists in database
                cursor.execute("INSERT INTO Author (Name, Affiliation, CitedBy, HIndex, I10Index) VALUES (%s, %s, %s, %s, %s)", 
                                [author['name'], author['affiliation'] if 'affiliation' in author else None, None, author['hIndex'] if 'hIndex' in author else None, None])
                cursor.execute("SELECT LAST_INSERT_ID()")
                new_id = cursor.fetchone()[0]
                currentAuthorId = new_id
                primaryAuthorId = new_id if primaryAuthorId == None else primaryAuthorId
            # Insert interests
            if 'interests' in author:
                for interest in author['interests']:
                    if interest != '':
                        cursor.execute("INSERT IGNORE INTO InterestedIn VALUES (%s, %s)", [currentAuthorId, interest])
            writers.append(currentAuthorId)
            try:
                graphConn.insert_new_author(currentAuthorId, author['name'])
            except:
                pass
    logging.info("Finished insertAuthors")
    return primaryAuthorId, writers

# TODO: Find journal or publisher
def insertArticle(title, primaryAuthorId, link, year, writers, graphConn):
    logging.info("Inside insertArticle")
    with connection.cursor() as cursor:
        cursor.execute("INSERT INTO Article (PrimaryAuthorId, CitedBy, Citations, Title, Year, Url, Publisher, Journal) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", 
        [primaryAuthorId, 0, 0, title, year, link, None, None])
        cursor.execute("SELECT LAST_INSERT_ID()")
        new_id = cursor.fetchone()[0]
        try:
            graphConn.insert_new_article(new_id, title, writers)
        except:
            pass
        logging.info("Finished insertArticle")
        return new_id

def insertCitationGraph(graphConn, articleId, sourceId):
    logging.info("Inside insertCitationGraph")
    # Insert first article and primary author
    with connection.cursor() as cursor:
        try:
            innerCur.execute("SELECT Title, PrimaryAuthorId FROM Article WHERE articleId = %s", [articleId])
            articleInfo = innerCur.fetchone()
            innerCur.execute("SELECT Name FROM Author WHERE authorId = %s", [articleInfo[1]])
            authorName = innerCur.fetchone()[0]
            graphConn.insert_new_author(articleInfo[1], authorName)
            graphConn.insert_new_article(articleId, articleInfo[0], [articleInfo[1]])
        except:
            pass
        # Insert second article and primary author
        try:
            innerCur.execute("SELECT Title, PrimaryAuthorId FROM Article WHERE articleId = %s", [sourceId])
            articleInfo = innerCur.fetchone()
            innerCur.execute("SELECT Name FROM Author WHERE authorId = %s", [articleInfo[1]])
            authorName = innerCur.fetchone()[0]
            graphConn.insert_new_author(articleInfo[1], authorName)
            graphConn.insert_new_article(sourceId, articleInfo[0], [articleInfo[1]])
        except:
            pass

        graphConn.insert_citation_relation(articleId, sourceId)
    logging.info("Finished insertCitationGraph")

# Input:
# ArticleId, citations = [citations, references]
# References = publications referenced by this paper
# Citations = publications citing this paper
def insertCitations(articleId, citations, graphConn):
    logging.info("Inside insertCitations")
    with connection.cursor() as cursor:
        for citation in citations[1]: # Articles referenced by this paper
            if citation['title'] == None:
                continue
            otherArticleId = None
            # Check if article exists
            primaryAuthorId, writers = insertAuthors(citation['authors'], graphConn)
            result = findArticle(citation['title'], primaryAuthorId)
            if result == None:
                otherArticleId = insertArticle(citation['title'], primaryAuthorId, citation['url'], citation['year'], writers, graphConn)
            else:
                otherArticleId = result[0]
            cursor.execute("INSERT IGNORE INTO Citation (Article, Cites) VALUES (%s, %s)",
            [articleId, otherArticleId])
            insertCitationGraph(graphConn, articleId, otherArticleId)
        for citation in citations[0]: # Other articles that cited this paper
            if citation['title'] == None:
                continue
            otherArticleId = None
            # Check if article exists
            primaryAuthorId, writers = insertAuthors(citation['authors'], graphConn)
            result = findArticle(citation['title'], primaryAuthorId)
            if result == None:
                otherArticleId = insertArticle(citation['title'], primaryAuthorId, citation['url'], citation['year'], writers, graphConn)
            else:
                otherArticleId = result[0]
            cursor.execute("INSERT IGNORE INTO Citation (Article, Cites) VALUES (%s, %s)",
            [otherArticleId, articleId])
            insertCitationGraph(graphConn, articleId, otherArticleId)
    logging.info("Finished insertCitations")

# Input:
# title: String
# authors: [{name: String, affiliation: String, hIndex: Integer, interests: [interest: string]}]
# link: String
# citations = [citations, references]
# where citations, references = [{authors: [authorId, name, url], title: String, url: String, year: Int}]
def insertEntries(title, authors, link, citations, year, graphConn):
    logging.info("Inside insertEntries")
    primaryAuthorId, writers = insertAuthors(authors, graphConn)
    articleId = insertArticle(title, primaryAuthorId, link, year, writers, graphConn)
    insertCitations(articleId, citations, graphConn)
    logging.info("Finished insertEntries")

def run():
    logging.basicConfig(level=logging.DEBUG, filemode='w', filename="crawlLog.log", format='%(name)s - %(levelname)s - %(message)s')
    logging.info("Inside of run")
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome('/Users/michaelvdow/Documents/chromedriver', chrome_options=chrome_options) # Update to chromedriver path

    # feed = feedparser.parse(URL_NAME + 'cs')
    # feed = feedparser.parse('http://web.archive.org/web/20191115025945/http://export.arxiv.org/rss/cs')
    # numEntries = len(feed['entries'])
    # logging.info("Number of entries: " + str(numEntries))
    graphConn = graph_driver.Neo4jConnector()

    # entry = feed['entries'][numEntries-5]
    for archive in ARCHIVE_NAMES:
        print(archive)
        feed = feedparser.parse(URL_NAME + 'cs')
        numEntries = len(feed['entries'])
        logging.info("Number of entries: " + str(numEntries))
        i = 1
        for entry in feed['entries']:
            # Get article info
            try:
                title = getTitle(entry)
                authorNames = getAuthors(entry)
                link = getLink(entry)

                articleId = entry['id']
                articleId = articleId[articleId.rfind("/")+1:]
                citations = getCitationsAndReferences(articleId)
                year = getYear(articleId)
                authorInfo = getAuthorInfo(articleId, driver)

                insertEntries(title, authorInfo, link, citations, year, graphConn)
            except KeyboardInterrupt:
                sys.exit()
            except Exception as e:
                print(e)
                print(traceback.format_exc())
                logging.info("Failed to insert entry {}: {}".format(i, entry['title']))
            print("Finished entry {}/{}".format(i, numEntries))
            i += 1
    logging.info("Finished run")
