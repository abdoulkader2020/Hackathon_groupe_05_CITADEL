#!/usr/bin/env python
# coding: utf-8

# In[2]:


import pandas as pd
import numpy as np
import os
import json
import nltk
nltk.download('udhr')
from nltk.corpus import udhr
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from nltk.stem.snowball import FrenchStemmer
from nltk.stem.snowball import SnowballStemmer
import matplotlib.pyplot as plt
import seaborn as sns
import re
regex = r"\b[aà]\b"


# In[3]:


def to_lower(array_string):
    ret_value = []
    for i in array_string:
        ret_value.append(i.lower())
    return ret_value


# In[4]:


def get_all_comment(comment_column):
    commentaires = []
    for i in comment_column:
        for j in i:
            comment = j['Comment'].lower()
            commentaires.append(comment)
    return commentaires


# In[5]:


def tokenize(messages):
    tokenize_message = []
    for i in messages:
        tokenize_message.append(nltk.word_tokenize(i, language='french'))
    return tokenize_message


# In[6]:


def cleaning(messages, stopWords):
    clean_words = []
    for i in messages:
        tokens = []
        for token in i:
            if token not in stopWords:
                token = token.replace('’', '')
                token = re.sub(regex, '', token, flags=re.MULTILINE)
                tokens.append(token)
        clean_words.append(tokens)
    return clean_words


# In[7]:


def stemisation(messages):
    # stemmer = SnowballStemmer(language='french')
    stemmer = FrenchStemmer()
    stemmer_words = []
    for i in messages:
        stems = []
        for stem in i:
            stems.append(stemmer.stem(stem))
        # stems = set(stems)
        stemmer_words.append(stems)
    return stemmer_words
    


# In[8]:


file_path = os.path.join(os.getcwd(), "dataset/dataset_lien_le_fasonet.json") 


# In[9]:


data = pd.read_json(file_path)


# In[10]:


#data.head(10)


# In[11]:


commentaires_corpus = get_all_comment(data['Comments'])


# In[12]:


french_words = udhr.words('French_Francais-Latin1')


# In[13]:


words = to_lower(french_words)


# In[14]:


text = nltk.Text(words)


# In[15]:


nltk.download('stopwords')
stpw = stopwords.words('french')
stpw.append(',')
stpw.append(';')
stpw.append('.')
stpw.append('%')
stpw.append("'")
stpw.append(':')
stpw.append('l')
stpw.append('qu')
stpw.append('au')
stpw.append('!')
stpw.append('?')
stpw.append('d')
stpw.append('(')
stpw.append(')')
stpw.append('`')
stpw.append("'")
stpw.append(itm for itm in ['’',"''",'a'])
stpw.append(itm for itm in ["’","a","plus","comme","cet","bien","san","être","''","``","leur","cel","peut","dit","ceux","bon", 'ça','à'])
stpw = set(stpw)


# ## Chargement des données de tendances

# In[16]:


tendances = ['EI','EIS','FAMa','FAR','FDS','GANE','IED','JNIM','MINUSMA','MPSR','RN','VDP','ZIM','etat islamique','etat islamique du sahel','Forces armees du Mali','Forces armees regulieres','Groupes Arme Non Etatique','Engins explosifs improvises','Jamaat Nasr Al islam wa Al mouslimin','Mission Multidimensionnelle Integree des Nations Unies pour la Stabilisation au Mali','Mouvement Patriotique pour la Sauvegarde et la Restauration','Route Nationale','Volontaires de defense pour la Patrie','Zone d\'interet militaire']


# In[17]:


tendances= to_lower(tendances)


# In[18]:


## Cleanning data


# In[ ]:





# ## Tokenisation

# In[19]:


#tokenized_commentaire = nltk.word_tokenize(commentaires_corpus, language='french')
tokenize_comment = tokenize(commentaires_corpus)
tokenize_tendance = tokenize(tendances)


# In[20]:


commentaire_clean = cleaning(tokenize_comment, stpw)
tendance_clean = cleaning(tokenize_tendance, stpw)


# ## racinisation

# In[22]:


# comment_stems= stemisation([['commentaire', 'commenter']])
comment_stems= stemisation(commentaire_clean)
tendance_stems= stemisation(tendance_clean)
flat_tendance = [item for line in tendance_stems for item in line]


# In[23]:


flat_comment = [item for line in comment_stems for item in line]


# In[24]:


df_comment = pd.DataFrame(flat_comment)
df_comment.value_counts()[0]
top_50 = df_comment.value_counts().iloc[2:52]
top_50.plot(kind='bar')


# In[298]:





# In[25]:


from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer


# In[26]:


tfidvectorizer = TfidfVectorizer(ngram_range=(1,3))
countvectorizer = CountVectorizer()


# In[29]:


X = comment_stems
y = flat_tendance
comments_rec = []
for k in comment_stems:
    comments_rec.append(' '.join(k))
# X = vectorizer.fit_transform(comments_rec)
count_wm = countvectorizer.fit_transform(comments_rec)
tfidf_wm = tfidvectorizer.fit_transform(comments_rec)


# In[35]:


count_tokens = countvectorizer.get_feature_names()
tfidf_tokens = tfidvectorizer.get_feature_names()


# In[ ]:


df_countvect = pd.DataFrame(data = count_wm.toarray(),columns = count_tokens)
df_tfidfvect = pd.DataFrame(data = tfidf_wm.toarray(),columns = tfidf_tokens)

print("Count Vectorizer\n")
print(df_countvect)
print("\nTD-IDF Vectorizer\n")
print(df_tfidfvect)
