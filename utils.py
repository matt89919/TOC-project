import os
from bs4 import BeautifulSoup
import requests
from linebot import LineBotApi, WebhookParser
from linebot.models import TextSendMessage, ImageSendMessage, TemplateSendMessage, ImageCarouselColumn, ImageCarouselTemplate, ButtonsTemplate, MessageTemplateAction, URITemplateAction, ImageSendMessage, CarouselTemplate, CarouselColumn

channel_access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", None)
line_bot_api = LineBotApi(channel_access_token)

def send_text_message(reply_token, text):
    line_bot_api.reply_message(reply_token, TextSendMessage(text=text))

    return "OK"

def push_message(userid, msg):
    line_bot_api.push_message(userid, TextSendMessage(text=msg))
    return "OK"

def send_button_message(id, img, title, uptext, labels, texts):

    acts = []
    for i, lab in enumerate(labels):
        acts.append(
            MessageTemplateAction(
                label=lab,
                text=texts[i]
            )
        )

    message = TemplateSendMessage(
        alt_text='Buttons template',
        template=ButtonsTemplate(
            thumbnail_image_url=img,
            title=title,
            text=uptext,
            actions=acts
        )
    )
    line_bot_api.push_message(id, message)
    return "OK"


def webscrape(str):
    html_text=requests.get('https://www.pttweb.cc/bbs/Coffee').text
    soup=BeautifulSoup(html_text,'lxml')
    articles=soup.find_all('div', class_='e7-right-top-container e7-no-outline-all-descendants')
    res=''
    time=0
    for article in articles:
        ss=article.find_all('span', class_='')
        for s in ss:
            if str in s.text:
                res+=s.text
                res+='\n'
                print(s.text)
                link='https://www.pttweb.cc'+article.a['href']
                res+=link
                res+='\n'
                print(link)
                time+=1
                if time>=10 :
                    break
        if time>=10 :
            break
                
    return res
                


"""
def send_image_url(id, img_url):
    pass

def send_button_message(id, text, buttons):
    pass
"""
