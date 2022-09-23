#!/usr/bin/env python3
# coding: utf-8

# In[31]:


import urllib.request
from bs4 import BeautifulSoup as bs
import pandas as pd
from pandas import DataFrame
import requests
import codecs, json
import os
import operator as op


# In[32]:


# Réertoire de stockage des données 

rep_stockage = os.path.join(os.getcwd(), "dataset") # 


# Traitement et constitution des données de chaque lien.

bdd_courant = os.path.join(rep_stockage, 'dataset_lien_le_fasonet.json') 

lien = "https://lefaso.net/spip.php?rubrique459"

lien2 = "https://lefaso.net/spip.php?rubrique459"

print("-----------------------------------------")
print("Récupération du des données du faso.net ")
print("-----------------------------------------")


# Récupération des données de des pages

def recupartion_donnees(lelien):
    page=urllib.request.Request(lelien,headers={'User-Agent': 'Google Chrome/92.0.4515.131'}) 
    infile=urllib.request.urlopen(page).read()
    data = infile.decode('utf-8')
    soup = bs(data, 'lxml')
    return soup
    

#  Définition des colonnes de la base de données

colonnes = ["Title", 
            "Publish_date",
            "Content",
            "Publish_by",
            "Comments"
           ]
commentaire = ["Comment",
               "Comment_by",
               "Comment_date"
              ]

tableau = DataFrame(columns=colonnes)
tableau.to_json(bdd_courant)


#  Création et initialisation d'un dictionnaire de données

datadico = {}
domaine = "https://lefaso.net/"

datadicos = []

list_url = []
    
soup = recupartion_donnees(lien)
dernire_page = soup.findAll("a", class_='lien_pagination').pop().text
# for i in range(0,41,20):
for i in range(0,int(dernire_page),20):
    if(i>0):
        lien = lien2 + "&debut_articles="+ str(i) +"#pagination_articles"
    soup = recupartion_donnees(lien)
    contenu = soup.findAll("div", attrs={'style':'width:100%; height:160px;margin-top:10px; margin-bottom:10px;'})
    for c in contenu:
        lien_contenu = c.find('h3').find("a" )["href"]
        div_title = c.find('h3').find("a").text
        div_publish_date = c.find('abbr')["title"]
        url_contenu = domaine + lien_contenu
        list_url.append(url_contenu)
        contenu_nested= ""
        source = ""
        
        if op.countOf(url_contenu, list_url)<=1:
            soup_nested = recupartion_donnees(url_contenu)
            contenu_nested = soup_nested.findAll("h3")[0].text #soup_nested.findAll("h3").find("p").find("strong").text
            div_comment = []
            div = soup_nested.find("div", class_='article_content')
            if div:
                for p in div.findAll("p"):
                    if not p.text.startswith('Lefaso.net'):
                        if p.text.startswith('Source'):
                            source = p.text
                        else:
                            contenu_nested = contenu_nested + p.text
            
            ul = soup_nested.find("ul", class_='comments-ul comments-items')
            if ul:
                for comment in ul.findAll("li") :
                    coment_descrip = comment.find("div"  , class_ = "comment-texte").text
                    comment_by = ''
                    command_balise = comment.find("strong" , class_ = "fn n")
                    if(command_balise):
                        comment_by = command_balise.text
                    coment_date = comment.find("abbr")["title"]
                    div_comment_tab = {}
                    div_comment_tab["Comment"] = coment_descrip
                    div_comment_tab["Comment_by"] = comment_by
                    div_comment_tab["Comment_date"] = coment_date
                    div_comment.append(div_comment_tab)
                            
            div_content = contenu_nested
            div_publish_by = source
            
        datadico = {}
        datadico["Title"] = div_title
        datadico["Publish_date"] = div_publish_date
        datadico["Content"] = div_content
        datadico["Publish_by"] = div_publish_by
        datadico["Comments"] = div_comment
        datadicos.append(datadico)
with codecs.open(bdd_courant, 'w', 'utf8' ) as jsonfile:
    jsonfile.write(json.dumps(datadicos, sort_keys = True, ensure_ascii=False))
