# Tanner Sirota 61932813, Steven Le 51942618

from os import listdir
from bs4 import BeautifulSoup
from collections import defaultdict
from math import log10
from ast import literal_eval
from json import dumps
import re
from tkinter import *

def Index():
    docCount = 0
    indexes = defaultdict(dict)
    bkd = eval(open('bookkeeping.json', 'r').read())
    for direct in listdir('WEBPAGES_RAW'):
        if direct != '.DS_Store':
            for docs in listdir('WEBPAGES_RAW/' + direct):
                if docs != '.DS_Store':
                    if bkd[direct + '/' + docs].endswith(".txt") or bkd[direct + '/' + docs].endswith(".java") or bkd[direct + '/' + docs].endswith(".py"):
                        continue
                    docCount += 1
                    file = open('WEBPAGES_RAW/' + direct + "/" + docs, 'r', encoding="utf-8")
                    soup = BeautifulSoup(file.read(), 'html.parser')
                    tf = defaultdict(int)
                    for words in soup.get_text().split():
                        if re.match("^[A-Za-z]+$", words) or re.match("^[0-9]+$", words):
                            if len(words) > 1:
                                tf[words.lower()] += 1
                    for words in tf:
                        indexes[words][direct + '/' + docs] = 1 + log10(tf[words])
                        if soup.title is not None:
                            if words in soup.title:
                                indexes[words][direct + '/' + docs] = indexes[words][direct + '/' + docs] + .3
                    file.close()
    for unique in indexes:
        for docID in indexes[unique]:
            indexes[unique][docID] = indexes[unique][docID] * log10(docCount / len(indexes[unique]))
    
    jsonString = dumps(dict(indexes))
    newFile = open("IndexDict.json", "w")
    newFile.write(jsonString)
    newFile.close()
    
    
def search(fileDictIndex):
    for i in list(searchGUI.children.values()):
        if type(i) != Entry and type(i) != Button:
            i.destroy()
    bkd = eval(open('bookkeeping.json', 'r').read())
    try:
        userSearchTerm = searchInput.get()
        searchList = userSearchTerm.lower().split()
        rankDict = defaultdict(int)
        for term in searchList:
            for docID in fileDictIndex[term]:
                rankDict[docID] += fileDictIndex[term][docID]
        counter = 0
        for k, v in sorted(rankDict.items(), key=lambda item: item[1], reverse=True):
            if counter == 5:
                break
            Label(searchGUI, text=bkd[k]).pack()
            print(bkd[k])
            counter += 1
    except:
        print("No matches found.")
         
            
if __name__ == '__main__':
    FDI = eval(open("IndexDict.json", 'r').read())
    searchGUI = Tk()
    searchGUI.title("CS 121 Project 3 - Search Engine")
    searchGUI.geometry("500x500")
    searchInput = StringVar()
    searchEntry = Entry(searchGUI, textvariable=searchInput).pack()
    serachButton = Button(searchGUI, text="Search", command=lambda: search(FDI)).pack()
    searchGUI.mainloop()
    
    
