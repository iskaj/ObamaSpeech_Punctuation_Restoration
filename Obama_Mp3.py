# -*- coding: utf-8 -*-
"""
Created on Tue Apr  6 19:57:18 2021

@author: Danny Stax
"""

from urllib.request import urlopen
from bs4 import BeautifulSoup
import requests

def get_links():
    speech_links = []
    
    
    html = urlopen("https://www.americanrhetoric.com/barackobamaspeeches.htm")
    bsObj = BeautifulSoup(html.read(), 'html.parser')
    
    for a in bsObj.find_all('a', href=True):
        if ".mp3" in a['href']: 
            speech_links.append("https://www.americanrhetoric.com/" + a['href'])

    return speech_links

def get_titles(speech_links):
    speech_titles = []
    
    for link in speech_links:
        slash_index = link.rfind('/')
        title = link[slash_index+1:len(link)]
        speech_titles.append(title)
    
    return speech_titles

def get_audio(speech_links, speech_titles):
    with requests.Session() as req:
        for i in range(len(speech_links)):
            title = "speech_audio/" + speech_titles[i]
            download = req.get(speech_links[i], headers={'User-Agent': 'Mozilla/5.0'})
            if download.status_code == 200:
                with open(title, 'wb') as f:
                    f.write(download.content)
            else:
                print(f"Download Failed For File {title}")
                

def test_download(speech_links, speech_titles):
    with requests.Session() as req:
        title = "speech_audio/" + speech_titles[0]
        download = req.get(speech_links[0], headers={'User-Agent': 'Mozilla/5.0'})
        print("code")
        print(download.status_code)
        if download.status_code == 200:
            with open(title, 'wb') as f:
                f.write(download.content)
        else:
                print(f"Download Failed For File {title}")
                
def get_txt_links():
    txt_links = []
    
    
    html = urlopen("https://www.americanrhetoric.com/barackobamaspeeches.htm")
    bsObj = BeautifulSoup(html.read(), 'html.parser')
    
    for a in bsObj.find_all('a', href=True):
        if "speeches/barackobama" in a['href']: 
            txt_links.append("https://www.americanrhetoric.com/" + a['href'])
    
    return txt_links
                

def get_txt_titles(txt_links):
    txt_titles = []
    
    for link in txt_links:
        slash_index = link.rfind('/')
        title = link[slash_index+1:len(link)]
        title = title.replace('.htm', '')
        title = title + "_scraped.txt"
        txt_titles.append(title)
    
    return txt_titles
            

#speech_links = get_links()
#speech_titles = get_titles(speech_links)
#get_audio(speech_links, speech_titles)
    
txt_links = get_txt_links()
txt_titles = get_txt_titles(txt_links)


