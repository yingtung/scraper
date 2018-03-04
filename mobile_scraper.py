
# coding: utf-8

# In[20]:


import urllib.request
from bs4 import BeautifulSoup
import selenium
import time
import json


# In[2]:


def get_data(mobile_url):
    f = urllib.request.urlopen(mobile_url)
    html_doc = f.read()
    soup = BeautifulSoup(html_doc, 'html.parser')
    
    tablelist_elems = soup.find_all('div','tablelist forumlist')
    for tablelist_elem in tablelist_elems:
           
        subject_elems = tablelist_elem.find_all('a','topic_gen')
        subject_list = [subject_elem.getText() for subject_elem in subject_elems]
        url_list =['https://www.mobile01.com/'+subject_elem.get('href') for subject_elem in subject_elems]
        if mobile_url == "https://www.mobile01.com/forumtopic.php?c=20&p=1":
            subjectTop_elems = subject_elems = tablelist_elem.find_all('a','topic_top') 
            subjectTop_list = [subjectTop_elem.getText() for subjectTop_elem in subjectTop_elems]
            urlTop_list = ['https://www.mobile01.com/'+subjectTop_elem.get('href') for subjectTop_elem in subjectTop_elems]
            for i in range(len(subjectTop_list)):
                subject_list.insert(i,subjectTop_list[i])  
                url_list.insert(i,urlTop_list[i])
    
        reply_elems = tablelist_elem.find_all('td','reply')
        reply_list = [reply_elem.getText() for reply_elem in reply_elems]
    
        author_elems = tablelist_elem.find_all('td','authur')
        authorTime_list = [author_elem.find_all('p')[0].getText() for author_elem in author_elems]
        author_list =  [author_elem.find_all('p')[1].getText() for author_elem in author_elems]
    
        latestReply_elems = author_elems = tablelist_elem.find_all('td','latestreply')
        latestReplyTime_list = [latestReply_elem.find_all('p')[0].getText() for latestReply_elem in latestReply_elems]
        latestReplyAuthor_list = [latestReply_elem.find_all('p')[1].getText() for latestReply_elem in latestReply_elems]
    
        for i in range(len(subject_list)):
            data.append({
                '主題':subject_list[i],
                '回覆數':reply_list[i],
                '作者':author_list[i],
                '發佈時間':authorTime_list[i],
                '最新回應者':latestReplyAuthor_list[i],
                '最新回應時間':latestReplyTime_list[i],
                '連結':url_list[i] 
        })
    return data


# In[84]:


def get_intReply(data):
    for i in range(len(data)):
        if len(data[i]['回覆數']) > 3:
            data[i]['回覆數'] = int(data[i]['回覆數'].replace(',',''))
        else:
            data[i]['回覆數'] = int(data[i]['回覆數'])
    return data


# In[85]:


data = list()

for i in range(1,21):
    mobile_url = "https://www.mobile01.com/forumtopic.php?c=20&p="+str(i)
    get_data(mobile_url)
    time.sleep(1)
get_intReply(data)


# In[86]:


len(data)


# In[87]:


with open("mobileData.json","w",encoding='utf-8') as f:
     json.dump(data,f,ensure_ascii=False)

