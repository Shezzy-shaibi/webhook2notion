
import os
from notion.client import NotionClient
import datetime 
from flask import Flask
from flask import request
import re


app = Flask(__name__)

def trackWeather(token, URL, weather):
    # notion
    client = NotionClient(token)
    block = client.get_block(URL)
    block.title = weather

def createTweet(token, collectionURL, tweet, author, followers):
    # notion
    client = NotionClient(token)
    cv = client.get_collection_view(collectionURL)
    row = cv.collection.add_row()
    row.tweet = tweet
    row.author = author
    row.followers = followers


def createTask(token, collectionURL, content):
    # notion
    client = NotionClient(token)
    cv = client.get_collection_view(collectionURL)
    row = cv.collection.add_row()
    row.task = content


def createReceipt(token, collectionURL, product, content, url, date):
    # notion
    client = NotionClient(token)
    cv = client.get_collection_view(collectionURL)
    row = cv.collection.add_row()
    row.product = product
    row.content = content
    row.url = url
    row.date = date

def createEmail(token, collectionURL, sender, subject, message_url):
    # notion
    client = NotionClient(token)
    cv = client.get_collection_view(collectionURL)
    row = cv.collection.add_row()
    row.sender = sender
    row.subject = subject
    row.message_url = message_url

def createInvite(token, collectionURL, subject, description, inviteto):
    # notion
    match = re.search('https://upwork.com/applications/\d+', description) 
    url = match.group()
    id = re.search('\d+', url)
    client = NotionClient(token)
    cv = client.get_collection_view(collectionURL)
    row = cv.collection.add_row()
    row.name = subject
    row.description = description
    row.status = "New"
    row.to = inviteto
    row.link = url
    row.id = id.group()
 
def createPCJ(token, collectionURL, subject, description, inviteto, link):
    # notion
    id = re.search('%7E[\w]+', link)
    client = NotionClient(token)
    cv = client.get_collection_view(collectionURL)
    row = cv.collection.add_row()
    row.name = subject
    row.description = description
    row.status = "New"
    row.to = inviteto
    row.link = link
    row.id = id.group()[3:]
    
def createMessage(token, parent_page_url, message):
    # notion
    page = client.get_block(parent_page_url)
    page.children.add_new(DividerBlock)
    page.children.add_new(BasicBlock, title="[{} {message}]").format(datetime.date.today().strftime("%Y-%m-%d"))
    page.children.add_new(DividerBlock)
    
@app.route('/message', methods=['GET'])
def message():
    parent_page_url = request.args.get("parent_page_url")
    token_v2 = os.environ.get("TOKEN")
    message = request.args.get("message")
    createMessage(token_v2, parent_page_url, message)
    return f'added {subject} receipt to Notion'    
    
@app.route('/pcj', methods=['GET'])
def pcj():
    collectionURL = request.args.get("collectionURL")
    description = request.args.get('description')
    subject = request.args.get('subject')
    token_v2 = os.environ.get("TOKEN")
    inviteto = request.args.get('inviteto')
    link = request.args.get('link')
    createPCJ(token_v2, collectionURL, subject, description, inviteto, link)
    return f'added {subject} receipt to Notion'

@app.route('/invites', methods=['GET'])
def invites():
    collectionURL = request.args.get("collectionURL")
    description = request.args.get('description')
    subject = request.args.get('subject')
    token_v2 = os.environ.get("TOKEN")
    inviteto = request.args.get('inviteto')
    createInvite(token_v2, collectionURL, subject, description, inviteto)
    return f'added {subject} receipt to Notion'

@app.route('/twitter', methods=['GET'])
def twitter():
    tweet = request.args.get('tweet')
    author = request.args.get('author')
    followers = request.args.get('followers')
    token_v2 = os.environ.get("TOKEN")
    url = os.environ.get("URL")
    createTweet(token_v2, url, tweet, author, followers)
    return f'added {tweet} to Notion'


@app.route('/tasks', methods=['GET'])
def tasks():
    todo = request.args.get('task')
    token_v2 = os.environ.get("TOKEN")
    url = os.environ.get("URL")
    createTask(token_v2, url, todo)
    return f'added {todo} to Notion'


@app.route('/gmailreceipts', methods=['GET'])
def gmailReceipt():
    product = request.args.get('product')
    content = request.args.get('content')
    message_url = request.args.get('url')
    date = request.args.get('date')
    token_v2 = os.environ.get("TOKEN")
    url = os.environ.get("URL")
    createReceipt(token_v2, url, product, content, message_url, date)
    return f'added {product} receipt to Notion'



@app.route('/createemail', methods=['GET'])
def gmailUrgentEmail():
    sender = request.args.get('sender')
    subject = request.args.get('subject')
    message_url = request.args.get('url')
    token_v2 = os.environ.get("TOKEN")
    url = os.environ.get("URL")
    createEmail(token_v2, url, sender, subject, message_url)
    return f'added email from {sender} to Notion'

@app.route('/getweather', methods=['GET'])
def getWeather():
    weather = str(request.args.get('weather'))
    token_v2 = os.environ.get("TOKEN")
    url = os.environ.get("URL")
    trackWeather(token_v2, url, weather)
    return f'added {weather} to Notion'


if __name__ == '__main__':
    app.debug = True
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
