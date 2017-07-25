#!/usr/bin/python
import time
import subprocess
import telepot
import os
import urllib2
import re
import json
import requests
from bs4 import BeautifulSoup
from urllib2 import urlopen
import youtube_dl

def handle(msg):
        chat_id = msg['chat']['id']
        command = msg['text']

        print "Command from client : %s " %command

    #youtube search
        if command.startswith('yt'):
            param = command[3:]
            response = urlopen("https://www.youtube.com/results?search_query="+param)
            data = response.read()
            response.close()
            soup = BeautifulSoup(data,"html.parser")
            vid = soup.find(attrs={'class':'yt-uix-tile-link'})
            link = "https://www.youtube.com"+vid['href']
            watchid = vid['href']
            watchid = watchid.replace('/watch?v=','')
            title = vid['title']
            print title
            print link
            bot.sendMessage(chat_id,title+"\n"+link)

            options = {
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '320'
                }]
            }
            filename = title+"-"+watchid+".mp3"
            filename = filename.replace(" ","_")
            filename = filename.replace("'","")
            filename = filename.replace("&","")
            with youtube_dl.YoutubeDL(options) as ydl:
                ydl.download([link])
                bot.sendAudio(chat_id,audio=open(filename,'rb'))
                print "Sent!"
    #end youtube search



#api credentials
api = open('api.txt','r')
api_cont = api.read().strip()
bot = telepot.Bot(api_cont)
bot.message_loop(handle)
print '[+] Server is Listenining [+]'
print '[=] Type Command from Telegram [=]'

while 1:
        time.sleep(10)
