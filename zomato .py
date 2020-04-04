#!/usr/bin/env python
# coding: utf-8

# In[1]:


get_ipython().system('pip install requests')


# In[2]:


get_ipython().system('pip install beautifulsoup4')


# In[3]:


import json
import requests
from bs4 import BeautifulSoup
import pandas
import re


# In[32]:


headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}
page = 1
list_restaurants = []
c = 1


# In[33]:


for num in range(0, 6):
    url = "https://www.zomato.com/bangalore/south-bangalore-restaurants?page={0}".format(page)
    response = requests.get(url,headers=headers)
    content = response.content
    soup = BeautifulSoup(content, "html.parser")
    s_list = soup.find_all("div", {'id': 'orig-search-list'})
    list_content = s_list[0].find_all("div", {'class': 'content'})
    for i in range(0, 15):
        restaurant_name = list_content[i].find("a", attrs={'data-result-type': 'ResCard_Name'})
        restaurant_name = restaurant_name.string.strip()
        locality = list_content[i].find("b")
        locality = locality.string.strip()
        ratings = list_content[i].find("div",attrs= {'data-variation': 'mini inverted'})
        ratings = ratings.string.split()[0]
        res_type = list_content[i].find_all("div",attrs= {'class': 'col-s-12'})
        type_ = []
        for x in res_type:
            type_ = x.find("a", attrs={'class': 'zdark ttupper fontsize6'})
            if type_ is None:
                continue
            type_ = type_.string.split()
        if ratings is None:
            continue
        votes = list_content[i].find("span",attrs= {'class': re.compile(r'rating-votes-div*')})
        if votes is None:
            continue
        dataframe = []
        dfObject = {
            "restaurant_id": c,
            "name": restaurant_name,
            "area": locality,
            "restaurant_type": type_,
            "rating": ratings,
            "votes": votes.string.split()[0],
        }
        list_restaurants.append(dfObject)
        c = c + 1
        if c == 81:
            break
    page = page + 1
with open('rest_result.json', 'w') as outfile:
    json.dump(list_restaurants, outfile, indent=4)


# In[34]:


df = pandas.DataFrame(list_restaurants)
df.to_csv("rest_result.csv", index=False, header=True)


# In[35]:


df


# In[ ]:
