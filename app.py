
import os
from notion.client import NotionClient
from notion.block import *
from notion.collection import *
from datetime import datetime, date
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
    client = NotionClient(token)
    page = client.get_block(parent_page_url)
    a = page.children.add_new(TextBlock, title=" ")
    b = page.children.add_new(DividerBlock)
    c = page.children.add_new(TextBlock, title="**{data}** {msg}".format(data = datetime.now().strftime("%d-%m-%Y %H:%M"), msg = message))
    d = page.children.add_new(DividerBlock)
    a.move_to(page, "first-child")
    b.move_to(a, "after")
    c.move_to(b, "after")
    d.move_to(c, "after")
         


def createMessageDATE(token, parent_page_url, message):
    # notion
    client = NotionClient(token)
    
#    monday = datetime.date.now()
#    tuesday = moday + datetime.timedelta(days=1)
#    wednesday = tuesday + datetime.timedelta(days=1)
#    thursday = wednesday + datetime.timedelta(days=1)
#    friday = thursday + datetime.timedelta(days=1)
#    saturday = friday + datetime.timedelta(days=1)
#    sunday = saturday + datetime.timedelta(days=1)
    
    page = client.get_block(parent_page_url)
    dateblock = None
    
    for part in page.get().get('properties').get('title'):
           if len(part) > 1:
               if part[0] == '‣':
                   if part[1][0][0] == 'd':  # date
                       dateblock = part[1][0][1]
#    mon = page.children.add_new(HeaderBlock, title="")
#    mon.move_to(dateblock, "before")
#    mon.title= dateblock.get().get('properties').get('title')
#    mon.title[1][0][1].set('start_date')=monday
#    a = page.children.add_new(ToDoBlock, title=" ")
#    a.move_to(mon, "after")
                
#    
#    a = page.children.add_new(TextBlock, title=" ")
#    b = page.children.add_new(TextBlock, title = "{data} {msg}".format(data = NotionDate.to_notion('2019-10-04'), msg = message))
#    b = page.children.add_new(TextBlock, title = "{start}{data}{end} {msg}".format(start = '[["‣", [["d", {"type": "date", "start_date": "', data = datetime.now().strftime("%Y-%m-%d"), end = '", "date_format": "relative"}]]]]' , msg = message))
#    a.move_to(page, "first-child")
#    b.move_to(a, "after")
    


@app.route('/messagedate', methods=['GET'])
def messagedate():
    parent_page_url = request.args.get("parent_page_url")
    token_v2 = os.environ.get("TOKEN")
    message = request.args.get("message")
    createMessageDATE(token_v2, parent_page_url, message)
    return f'added {dateblock} receipt to Notion'    




@app.route('/message', methods=['GET'])
def message():
    parent_page_url = request.args.get("parent_page_url")
    token_v2 = os.environ.get("TOKEN")
    message = request.args.get("message")
    createMessage(token_v2, parent_page_url, message)
    return f'added {message} receipt to Notion'    


    
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
