
# coding: utf-8

# In[12]:


import requests
import json
import time
import datetime
import random


# In[17]:


#comp_code目前只有 電腦╱網路類 中的 程式設計類以及網頁技術類

comp_code={'12001003001':'A+',
             '12001003002':'ActionScript',
             '12001003003':'ADA',
             '12001003004':'AJAX',
             '12001003005':'ASP',
             '12001003006':'ASP.NET',
             '12001003007':'ATL',
             '12001003008':'C',
             '12001003009':'C#',
             '12001003010':'C++',
             '12001003011':'C++.Net',
             '12001003012':'CGI',
             '12001003013':'Clipper',
             '12001003014':'COBOL',
             '12001003015':'COM/DCOM',
             '12001003016':'COOL:Gen',
             '12001003017':'CORBA',
             '12001003018':'Delphi',
             '12001003019':'Developer/ Designer 2000',
             '12001003020':'DirectX',
             '12001003021':"FORTRAN",
             '12001003022':"Fox Pro",
             '12001003023':"FoxBASE+",
             '12001003024':"Infobasic",
             '12001003025':"Java",
             '12001003026':"JCL",
             '12001003027':"JCreator Pro",
             '12001003028':"JMS",
             '12001003029':"JSF",
             '12001003030':"JSP",
             '12001003031':"Kylix",
             '12001003032':"Lotus Notes",
             '12001003033':"LotusScript",
             '12001003034':"Matlab",
             '12001003035':"MFC",
             '12001003036':"PAL",
             '12001003037':"Pascal",
             '12001003038':"PECL",
             '12001003039':"PeopleCode",
             '12001003040':"Perl",
             '12001003041':"PHP",
             '12001003042':"PL/1",
             '12001003043':"PowerBuilder",
             '12001003044':"Pro*C",
             '12001003045':"Python",
             '12001003046':"Rexx",
             '12001003047':"RMI",
             '12001003048':"RPG",
             '12001003049':"Ruby",
             '12001003050':"Simula",
             '12001003051':"SIR",
             '12001003052':"Smalltalk",
             '12001003053':"Spring",
             '12001003054':"SQR",
             '12001003055':"StarTeam",
             '12001003056':"Struts",
             '12001003057':"TCL",
             '12001003058':"VBA",
             '12001003059':"Visual Basic",
             '12001003060':"Visual Basic .net",
             '12001003061':"Visual C#",
             '12001003062':"Visual C++",
             '12001003063':"Visual J#",
             '12001003064':"Visual J++",
             '12001003065':"Visual SourceSafe",
             '12001003066':"Visual Studio",
             '12001003067':"Visual Studio .net",
             '12001003068':"Win32",
             '12001003069':"WinForm",
             '12001003070':"WML",
             '12001003071':"XSL",
             '12001003072':"XSLT",
             '12001003073':"LabVIEW",
             '12001003074':"Silverlight",
             '12001003075':"Objective-C",
             '12001003076':"SWIFT",
             '12001003077':"X++",
             '12001003078':"R",
             '12001006001':'ActiveX',
             '12001006002':"Apache SOAP",
             '12001006005':"Cold Fusion",
             '12001006006':"DHTML",
             '12001006007':"Dreamweaver",
             '12001006008':"EJB",
             '12001006009':"Electronic Payment",
             '12001006010':"Fireworks",
             '12001006011':"FrontPage",
             '12001006012':"GoLive",
             '12001006013':"HTML",
             '12001006014':"J2EE",
             '12001006015':"J2ME",
             '12001006016':"J2SE",
             '12001006017':"JavaScript",
             '12001006018':"NetObjects Fusion",
             '12001006019':"RoboHelp",
             '12001006020':"SGML",
             '12001006021':"Shtml",
             '12001006022':"SMIL",
             '12001006023':"VBScript",
             '12001006024':"VRML",
             '12001006025':"Web Master/Developer",
             '12001006026':"XHTML",
             '12001006027':"XML",
             '12001006028':"XML Web services",
             '12001006029':"XSP",
             '12001006030':"jQuery",
             '12001006031':"Flex"
              }


# In[18]:


def jobscraper(comp) :
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                             'AppleWebKit/537.36 (KHTML, like Gecko) ''Chrome/59.0.3071.115 Safari/537.36'}
    url = 'http://www.104.com.tw/i/apis/jobsearch.cfm?fmt=8&comp='+comp
    totalpage = int(requests.get(url,headers).json()['TOTALPAGE'])
    for i in range(1,totalpage+1):
        sec = random.uniform(1, 4)    
        time.sleep(sec)                #隨機秒數休息
        resp_jobs = requests.get(url+'&page='+str(i),headers).json()
        resp_jobs['COMP']=comp_code[comp]
        jobs.append(resp_jobs)
    return jobs


# In[19]:


jobs=[]
for comp in list(comp_code):    #爬蟲時間測試:2018/03/04(日) 粗估一個小時(晚上九點半到十點半)
    jobscraper(comp)
    time.sleep(1)
today = datetime.datetime.now()
with open('104data_{0}-{1}-{2}.json'.format(today.year,today.month,today.day),'w', encoding='utf-8') as f:
    json.dump(jobs, f, indent=2, sort_keys=True, ensure_ascii=False)

