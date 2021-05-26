# -*- coding: utf-8 -*-
"""
Created on Sun Apr 11 13:15:51 2021

@author: Danny Stax
"""

from urllib.request import urlopen
from bs4 import BeautifulSoup
import os

def create_dictionary():    
    html = urlopen("https://www.americanrhetoric.com/barackobamaspeeches.htm")
    bsObj = BeautifulSoup(html.read(), 'html.parser')
    
    dictionary_items = []
    
    for a in bsObj.find_all('a', href=True):
        if "speeches/barackobama" in a['href']:
            txt_link = a['href']
            slash_index = txt_link.rfind('/')
            txt = txt_link[slash_index+1:len(txt_link)]
            txt = txt.replace('.htm', '')
            txt = txt + "_scraped.txt"
            
            table_row = a.find_parent('tr')
            mp3 = ""
            for attribute in table_row.find_all('a', href=True):
                if ".mp3" in attribute['href']:
                    mp3_link = attribute['href']
                    mp3_slash_index = mp3_link.rfind('/')
                    mp3 = mp3_link[mp3_slash_index+1:len(mp3_link)]
                    
            dict_item = {
                    "txt": txt,
                    "mp3": mp3
                    }
            
            dictionary_items.append(dict_item)
    
    return dictionary_items

def rename_files(dictionary_items):
    for i in range(len(dictionary_items)):
        item = dictionary_items[i]
        txt = item["txt"]
        mp3 = item["mp3"]
        
        txt_directory = 'D:/University/Master/Automatic Speech Recognition/Web Crawler/speech_texts/'
        txt_file = txt_directory + txt
        if os.path.isfile(txt_file):
            os.rename(txt_file, txt_directory + str(i) + "_scraped.txt")
        else:
            print(txt_file + " does not exist")
            
        mp3_directory = 'D:/University/Master/Automatic Speech Recognition/Web Crawler/speech_audio/'
        mp3_file = mp3_directory + mp3
        if os.path.isfile(mp3_file):
            os.rename(mp3_file, mp3_directory + str(i) + ".mp3")
        else: print(mp3_file + " does not exist")

dictionary_items = create_dictionary()
rename_files(dictionary_items)