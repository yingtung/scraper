
# coding: utf-8

# In[111]:


import json
import requests
import datetime


# In[112]:


#整理skill_tags，只保留技能名字 
def orgnize_skilltags(tmp_list):
    for i in range(len(tmp_list)):
        tmp_list[i]['skill_tags'] = [x['name'] for x in tmp_list[i]['skill_tags']]
    return tmp_list                                                               


# In[129]:


i = 1
url = "https://www.yourator.co/api/v2/jobs?page="+str(i)
headers =  {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                          'AppleWebKit/537.36 (KHTML, like Gecko) ''Chrome/59.0.3071.115 Safari/537.36'}
jobs_list =[]
resp_jobs = requests.get(url,headers).json()
tmp_list = resp_jobs['jobs']
orgnize_skilltags(tmp_list)
resp_jobs['jobs'] = tmp_list
jobs_list.append(resp_jobs)

try:
    while resp_jobs != []:
        i=i+1
        url = "https://www.yourator.co/api/v2/jobs?page="+str(i)
        resp_jobs = requests.get(url,headers).json()
        if resp_jobs['jobs'] == []:
                     break

        #整理skill_tags，只保留技能名字        
        list_jobs = resp_jobs['jobs']
        orgnize_skilltags(list_jobs)
        resp_jobs['jobs'] = list_jobs
        jobs_list.append(resp_jobs['jobs'])
except:
    print("Error")
today = datetime.datetime.now()

try:
    with open('youratorJobs_{0}-{1}-{2}.json'.format(today.year,today.month,today.day), 'w', encoding='utf-8') as f:
            json.dump(jobs_list, f, indent=2, sort_keys=True, ensure_ascii=False)
except IOError:
    print("IOError")
                 


# In[132]:


#透過api skill_tags 取得各個技能職缺數
skill_url = 'https://www.yourator.co/api/v2/job_skill_tags'
resp = requests.get(skill_url,headers).json()
try:
    with open('youratorSkillTags_{0}-{1}-{2}.json'.format(today.year,today.month,today.day), 'w', encoding='utf-8') as f:
            json.dump(resp, f, indent=2, sort_keys=True, ensure_ascii=False)
except IOError:
    print("IOError")


# In[133]:


get_ipython().magic('pinfo json')

