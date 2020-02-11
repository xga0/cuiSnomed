# -*- coding: utf-8 -*-
"""
Created on Tue Feb 11 09:21:40 2020

@author: sgaox
"""

from lxml import html
from bs4 import BeautifulSoup
import re
import pandas as pd
from os import listdir
from os.path import isfile, join

#Extract Cui-Snomed
def cuiSnomed(htmlfile):
    tree = html.parse(htmlfile)
    cui = tree.xpath('//span[@class="highlight"]/text()')
    with open(htmlfile, encoding='utf-8') as fp:
        soup = BeautifulSoup(fp)
        
    snomed = [el.text for el in soup.find_all('td')]
    snomedList = re.findall('\((.*?)\)',str(snomed))
    snomedList = [x for x in snomedList if x.isdigit()]
    snomedList = list(set(snomedList))
    
    if len(cui) == 0:
        cui = cui * len(snomedList)
        df = pd.DataFrame(columns=['cui', 'snomed'])
        df['snomed'] = snomedList
        df['cui'] = cui
        df['snomed'] = df['snomed'].astype(str)
        return df
    else:
        cui = list(set(cui))
        cui = cui * len(snomedList)
        df = pd.DataFrame(columns=['cui', 'snomed'])
        df['snomed'] = snomedList
        df['cui'] = cui
        df['snomed'] = df['snomed'].astype(str)
        return df
    
#Load Paths of All Files
mypath = "C:\\Users\\sgaox\\Desktop\\mapping\\urls\\"    
allHTML = [f for f in listdir(mypath) if isfile(join(mypath, f))]

def addPath(list, str): 
    str += '{0}'
    list = [str.format(i) for i in list] 
    return(list) 
    
allHTMLPath = addPath(allHTML, mypath)

#Extract Cui-Snomed from All Files
appended_data = []

for i in allHTMLPath:
    df = cuiSnomed(i)
    appended_data.append(df)
    
appended_data = pd.concat(appended_data)

appended_data.to_csv('C:\\Users\\sgaox\\Desktop\\mapping\\out1.csv')













