
# coding: utf-8

# In[64]:


import threading, queue, time, urllib 
from urllib import request
from bs4 import BeautifulSoup as bs
import pandas as pd
import os
import pymysql
import re


# In[65]:


tags=[]
for i in range(13,18):
    tags.append(i)
for i in range(21,28):
    tags.append(i)
for i in range(47,55):
    tags.append(i)
for i in range(62,84):
    tags.append(i)


# In[66]:


brandname = []
product=[]
scorestepone=[]


# In[67]:


urlQueue = queue.Queue() 
for i in tags:
    url = 'https://www.urcosme.com/tags/{0}/products?page=1'.format(i)
    response = urllib.request.urlopen(url)
    html_doc = response.read()
    responseCode = response.getcode()
    soup=bs(html_doc, 'html.parser')
    divElem = soup.find_all('div','uc-container-title')[2]
    spanElem = divElem.find_all('span')[1]
    totalNum = int(re.search(r'\d+',spanElem.text).group())
    remainder = totalNum % 10
    if remainder == 0:
        pageNum = int(totalNum/10)
    else:
        pageNum = int(totalNum/10)+1
    for page in range(1,pageNum+1):
        url = 'https://www.urcosme.com/tags/{0}/products?page={1}'.format(i,page)
        urlQueue.put(url)

def fetchUrl(urlQueue): 
    while True: 
        try: 
            #不阻塞的讀取佇列資料 
            url = urlQueue.get_nowait() 
            i = urlQueue.qsize() 
        except Exception as e: 
            break 
        #print ('Current Thread Name %s, Url: %s ' % (threading.currentThread().name, url)) 
        try: 
            response = urllib.request.urlopen(url)
            html_doc = response.read()
            responseCode = response.getcode()
            soup=bs(html_doc, 'html.parser')

            for pone in soup.select('.brand-name'):
                brandname.append(pone.text)

            for prdnam in soup.select('.product-name'):
                product.append(prdnam.text)

            for prdsc in soup.select('.product-score-text'):
                scorestepone.append(prdsc.text)
                
        except Exception as e: 
            continue 
        if responseCode == 200: 
            #抓取內容的數據處理可以放到這裏 
            #爲了突出效果， 設定延時 
            time.sleep(1) 
if __name__ == '__main__': 
    startTime = time.time() 
    threads = [] 
    # 可以調節執行緒數， 進而控制抓取速度 
    threadNum = 4 
    for i in range(0, threadNum): 
        t = threading.Thread(target=fetchUrl, args=(urlQueue,)) 
        threads.append(t) 
    for t in threads: 
        t.start() 
    for t in threads: 
        #多執行緒多join的情況下，依次執行各執行緒的join方法, 這樣可以確保主執行緒最後退出， 且各個執行緒間沒有阻塞 
        t.join() 
    endTime = time.time() 
    print ('Done, Time cost: %s ' % (endTime - startTime)) 


# In[68]:


#將品牌名字中英文分開
def is_alphabet(uchar):
        #判断一个unicode是否是英文字母
        if (uchar >= u'\u0041' and uchar<=u'\u005a') or (uchar >= u'\u0061' and uchar<=u'\u007a'):
            return True
        else:
            return False      
brandname = list(map(lambda b:b.split(" "),brandname))
brandname_CH=[]
brandname_EN=[]
for i in range(len(brandname)):
    brandname_EN.append("")
    brandname_CH.append("")
    for j in range(len(brandname[i])):
        if is_alphabet(brandname[i][j]):
            brandname_EN[i] += (" "+brandname[i][j])
        else:
            brandname_CH[i] += brandname[i][j].replace("品牌活動中","")


# In[69]:


#將評價分數取出來
score =[]
for i in range(len(scorestepone)):
    if scorestepone[i] != 'UrCosme指數' :
        if scorestepone[i] == '-.-':
            score.append(float(0))
        else:
            score.append(float(scorestepone[i]))


# In[71]:


data = pd.DataFrame(columns=['brand_EN','brand_CH','product','score'])


# In[72]:


data['brand_EN']=[b.strip() for b in brandname_EN]
data['brand_CH']=brandname_CH
data['product']=[p.strip() for p in product]
data['score']=score


# In[73]:


data.to_csv("/root/cosmetic/urcosme_data.csv",sep=',', encoding='utf-8',index=False)


# In[74]:


from sqlalchemy import create_engine
from sqlalchemy.types import NVARCHAR, Float, Integer
def mapping_df_types(df):
    dtypedict = {}
    for i, j in zip(df.columns, df.dtypes):
        if "object" in str(j):
            dtypedict.update({i: NVARCHAR(length=255)})
        if "float" in str(j):
            dtypedict.update({i: Float(precision=2, asdecimal=True)})
        if "int" in str(j):
            dtypedict.update({i: Integer()})
    return dtypedict


# In[75]:


#將dataframe 寫入MySQL
engine = create_engine('mysql+pymysql://cosmetic:Mysqlpn102!@192.168.56.169:3306/CosmeticDB?charset=utf8')
dtypedict = mapping_df_types(data)
pd.io.sql.to_sql(data,name='urcosmeTest',con=engine,if_exists='replace',index=False,dtype=dtypedict)


# In[76]:


db = pymysql.connect("192.168.56.169","cosmetic","Mysqlpn102!","CosmeticDB",charset='utf8mb4' )
cursor = db.cursor()
cursor.execute("ALTER TABLE urcosmeTest ADD COLUMN id INt NOT NULL PRIMARY KEY AUTO_INCREMENT")
db.commit()
#result = cursor.fetchall()
#print ("Database version : %s " % data)
db.close()


# In[77]:


#將各個欄位單獨寫檔
data['brand_CH'].to_csv("/root/cosmetic/brand_ch.csv",sep=',', encoding='utf-8',index=False)
data['brand_EN'].to_csv("/root/cosmetic/brand_en.csv",sep=',', encoding='utf-8',index=False)
data['product'].to_csv("/root/cosmetic/product.csv",sep=',', encoding='utf-8',index=False,header=0)
data[['brand_EN','brand_CH']].to_csv("/root/cosmetic/brand.csv",sep=',', encoding='utf-8',index=False,header=0)

