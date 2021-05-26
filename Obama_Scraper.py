# -*- coding: utf-8 -*-
"""
Created on Fri Mar 26 10:28:54 2021

@author: Danny Stax
"""

from urllib.request import urlopen
from bs4 import BeautifulSoup
import re

def get_links():
    speech_links = []
    
    
    html = urlopen("https://www.americanrhetoric.com/barackobamaspeeches.htm")
    bsObj = BeautifulSoup(html.read(), 'html.parser')
    
    for a in bsObj.find_all('a', href=True):
        if "speeches/barackobama" in a['href']: 
            speech_links.append("https://www.americanrhetoric.com/" + a['href'])
    
    return speech_links

    
def get_texts(speech_links):
    speech_texts = []
    regex = re.compile(r'[\n\r\t]')
    
    for link in speech_links:
        webpage = urlopen(link)
        soup = BeautifulSoup(webpage.read(), 'html.parser')
        text = ""
        
        for font in soup.find_all('font', size=2):
            clean_text = regex.sub("", font.text)
            clean_text = clean_text.replace(u'\xa0', ' ')
            clean_text = clean_text.replace('\\', '')
            clean_text = clean_text.replace("’", "'")
            clean_text = clean_text.replace("`", "'")
            text = text + " " + clean_text
            
        speech_texts.append(text)
    
    return speech_texts


def get_titles(speech_links):
    speech_titles = []
    
    for link in speech_links:
        slash_index = link.rfind('/')
        title = link[slash_index+1:len(link)]
        title = title.replace('.htm', '')
        speech_titles.append(title)
    
    return speech_titles


#speech_links = []
#speech_links.append('https://www.americanrhetoric.com/speeches/stateoftheunion2016.htm')
speech_links = get_links()
speech_texts = get_texts(speech_links)
speech_titles = get_titles(speech_links)

for i in range(len(speech_texts)):
    file_name = "speech_texts/" + speech_titles[i] + "_scraped.txt"
    text_file = open(file_name, "w", encoding="utf8")
    text_file.write(speech_texts[i])
    text_file.close()
