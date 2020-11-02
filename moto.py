#import urllib3
import requests
from bs4 import BeautifulSoup
import mysql.connector
import datetime
from bin.convdate import date_convert,time_delta
import time
import shutil 
import os
from progress.bar import Bar
import configparser


class config:
    conf=configparser.ConfigParser()
    conf.read('config.ini')
    settings =[]
    img_src =conf.get('img','src')
    data = {}
    d_list=[]
    art_data={}
    a_list =[]
    h_list =[]
    h_data ={}
    p_list=[]
    p_data={}
    l_list=[]
    l_data={}
    log={}
    sys_log=[]
    mydb = mysql.connector.connect(
    host=conf.get('mysql','host'),
    user=conf.get('mysql','user'),
    password=conf.get('mysql','password'),
    database= conf.get('mysql','database'), 
    )
    date = datetime.datetime.now()

    
    def time_update():
        config.date=datetime.datetime.now()



class pool:
    def feth(url):
        s=requests
        req = s.get(url)
        if req.status_code == 200:
            val=[]
            val={'Timeup':config.date,'ID':req.status_code,'Category':"Info",'Activity':'Http_req','Message':"Response code:"+str(req.status_code)+"Link:"+url}
            config.sys_log.append(val)
            return req
        else:
            val=[]
            val={'Timeup':config.date,'ID':req.status_code,'Category':"Info",'Activity':'Http_req','Message':"Response code:"+str(req.status_code)+"Link:"+url}
            config.sys_log.append(val)
            return req

    def parse(url):
        data=pool.feth(url)
        sup = BeautifulSoup(data.text, features="html.parser")
        offers = sup.find('div', attrs={'class':'offers list'})
        article =offers.find_all('article')
        #offer_items =offers.find_all('div', attrs={'class':'offer-item__title'})
        return article
    def article_list(url,Sys_ID):
        for a in pool.parse(url):
            for b in a.find_all('div', attrs={'class':'offer-item__title'}):
                for h in b.find_all('a', href=True):
                    config.time_update()
                    #print ("ID:"+h['data-ad-id'])
                    #print ("Title:"+h['title'])
                    #print ("link:"+h['href'])
                    config.data['Sys_ID']=Sys_ID
                    config.data['ID']=h['data-ad-id']
                    config.data['Title']=h['title']
                    config.data['Link']=h['href']
                    config.d_list.append(config.data)
                    config.data={}
                    val=[]
                    val={'Timeup':config.date,'ID':Sys_ID,'Category':"Info",'Activity':'Link Fetch','Message':"Article links fetched for Sys_ID:"+str(Sys_ID)+" Link:"+url}
                    config.sys_log.append(val)
                      
    def article_fetch():
        #with Bar('       Getting articles and pictures',max = len(config.d_list)) as bar:
        for a in config.d_list:
               config.time_update()
               raw= pool.feth(a['Link']+"")
               sup = BeautifulSoup(raw.text, features="html.parser")
               try:
                config.art_data['ID']= sup.find_all('span', attrs={'class':'offer-meta__value'})[1].text.strip()
                tmptime = sup.find('span', attrs={'class':'offer-meta__value'}).text.strip().partition(',')
                #print(tmptime[0])
                tmpdate=tmptime[2]
                tmpday=(tmpdate.partition(' ')[2]).partition(" ")[0]
                tmpmonth=date_convert((((tmpdate.partition(' ')[2]).partition(" ")[2]).partition(" ")[0]))
                tmpyear = ((tmpdate.partition(' ')[2]).partition(" ")[2]).partition(" ")[2]
                config.art_data['Since']= tmpyear+"-"+tmpmonth+"-"+tmpday+" "+str(tmptime[0])
                #print(config.art_data) #sup.find('span', attrs={'class':'offer-meta__value'}).text.strip()
                art = sup.find('div', attrs={'class':'offer-header__row hidden-xs visible-tablet-up'})
                config.art_data['Title'] =art.find('h1', attrs={'class':'offer-title big-text'}).text.strip()
                config.art_data['Price'] = art.find('div', attrs={'class':'offer-price'})['data-price']
                config.art_data['Year'] = art.find_all('span', attrs={'class': 'offer-main-params__item'})[0].text.strip()
                config.art_data['Milage'] = art.find_all('span', attrs={'class': 'offer-main-params__item'})[1].text.strip()
                config.art_data['Fuel'] = art.find_all('span', attrs={'class': 'offer-main-params__item'})[2].text.strip()
                config.art_data['Type'] = art.find_all('span', attrs={'class': 'offer-main-params__item'})[3].text.strip()
                
                detloc=sup.find('span', attrs={'class': 'seller-box__seller-address__label'}).text.strip()
                detloc_gps=sup.find('div', attrs={'class': 'map-box'}).find('input',attrs={'type':'hidden'})
                detloc_long = detloc_gps['data-map-lon']
                detloc_lat =  detloc_gps['data-map-lat']
                #print (detloc_long, detloc_lat)
                if sup.find('a', attrs={'class': 'map-picture link-blue'},href=True) is not None: # href=True
                    detmap =sup.find('a', attrs={'class': 'map-picture link-blue'},href=True)['href']
                    #print (detmap)
                else:
                    detmap ="empty"
                val=[]
                val={'Timeup':config.date,'ID':config.art_data['ID'],'Category':"Info",'Activity':'location Fetch','Message':"location fetched for"+str(config.p_data)+":"}
                config.sys_log.append(val)
                config.l_data={'ID':config.art_data['ID'],'Title':str(detloc),'Link':str(detmap) ,'Long':str(detloc_long),'Lat':str(detloc_lat)}
                config.l_list.append(config.l_data)
                config.l_data ={}

                img=sup.find_all('img', attrs={'class': 'bigImage'})
                val=[]
                val={'Timeup':config.date,'ID':config.art_data['ID'],'Category':"Info",'Activity':'Article Fetch','Message':"Article fetched for"+str(config.art_data)+":"}
                config.sys_log.append(val)
                c=0
                for i in img:
                    config.time_update()
                    #print(i['data-lazy'])
                    config.p_data['ID']=config.art_data['ID']
                    config.p_data['IMG_ID']=config.art_data['ID']+str(c)
                    config.p_data['F_Name']=config.art_data['ID']+"_"+str(c)
                    config.p_data['Link']=i['data-lazy']
                    config.p_data['Image']=config.img_src+config.art_data['ID']+"/"+config.p_data['F_Name']+".jpeg"
                    pool.img_fetch(config.p_data['Link'],config.art_data['ID'],config.p_data['F_Name']+".jpeg")
                    c=c+1
                    val=[]
                    val={'Timeup':config.date,'ID':config.art_data['ID'],'Category':"Info",'Activity':'Image Fetch','Message':"Image fetched for"+str(config.p_data)+":"}
                    config.sys_log.append(val)
                    config.p_list.append(config.p_data)
                    config.p_data ={}
                        
                config.a_list.append(config.art_data)
                config.art_data={}
               except(IndexError): 
                   print (sup)
               #bar.next()
           
    def hist_article_check():
        dbmoto.check_exist()
        with Bar('Checking historical data:',max = len(config.h_list)) as bar:
            for a in config.h_list:
                config.time_update()
                if a['Timeup'] < (config.date - datetime.timedelta(days=1)) or a['Status'] == "Inactive":
                    raw= pool.feth(a['Link'])
                    sup = BeautifulSoup(raw.text, features="html.parser")
                    try:
                        error=sup.find('span', attrs={'class':'subtitle'}).text.strip()
                    except(AttributeError):
                        error=sup.find('span', attrs={'class':'subtitle'})
                    try:
                        tmpid=sup.find_all('span', attrs={'class':'offer-meta__value'})[1].text.strip()
                    except(IndexError):
                        tmpid = False
                    #print (raw.status_code,a['ID'])
                    if raw.status_code == 404 or error == "404 Strona nie została odnaleziona" or tmpid == False:
                        #print (error)
                        dbmoto.update_items("m_article&link_incative",a['ID'],data={'Since':str(a['Since']),'Status':'Inactive'})
                        val=[]
                        val={'Timeup':config.date,'ID':a['ID'],'Category':"Info",'Activity':'History check','Message':"Article status change to Inactive"}
                        config.sys_log.append(val)
                    else:
                        dbmoto.update_items("m_article&link_incative",a['ID'],data={'Since':str(a['Since']),'Status':'Active'})
                        val=[]
                        val={'Timeup':config.date,'ID':a['ID'],'Category':"Info",'Activity':'History check','Message':"Article status changed to Active for"+str(a['ID'])}
                        config.sys_log.append(val)
                bar.next()
            config.h_list=[]

    def img_fetch(link,ID,filename):
        filename = config.img_src+ID+"/"+filename
        if  os.path.isfile(filename) == False:
            r = requests.get(link, stream = True)
            if r.status_code == 200:
            # Set decode_content value to True, otherwise the downloaded image file's size will be zero.
                r.raw.decode_content = True
                try:
                    os.mkdir(config.img_src+ID+"/")
                except OSError:
                    #print ("Creation of the directory %s failed"+config.img_src+ID+"/")
                    val=[]
                    val={'Timeup':config.date,'ID':ID,'Category':"Error",'Activity':'Directory creation','Message':"Creation of the directory failed"+config.img_src+ID+"/"}
                    config.sys_log.append(val)
                else:
                    #print ("Successfully created the directory %s "+config.img_src+ID+"/")
                    val=[]
                    val={'Timeup':config.date,'ID':ID,'Category':"Info",'Activity':'Directory creation','Message':"Successfully created the directory "+config.img_src+ID+"/"}
                    config.sys_log.append(val)
                
                #filename = "./images/"+filename
                #print (filename)
            # Open a local file with wb ( write binary ) permission.
                with open(filename,'wb+') as f:
                    shutil.copyfileobj(r.raw, f)
            
                #print('Image sucessfully Downloaded: ',filename)
                val=[]
                val={'Timeup':config.date,'ID':ID,'Category':"Info",'Activity':'Image download','Message':"Image sucessfully Downloaded: "+filename}
                config.sys_log.append(val)
            else:
                #print('Image Couldn\'t be retreived')
                val=[]
                val={'Timeup':config.date,'ID':ID,'Category':"Error",'Activity':'Image download','Message':"Image Couldn\'t be retreived"+filename}
                config.sys_log.append(val)
        #else:
         #   print (filename+" Exist")

class dbmoto:
    mycursor = config.mydb.cursor()
    def get_config():
        myresult=0
        dbmoto.mycursor.execute("SELECT * FROM searches")
        myresult = dbmoto.mycursor.fetchall()
        #print (myresult)
        settings={}
        with Bar('Getting searches!',max = len(myresult)) as bar:
            for i in myresult:
                config.time_update()
                settings['Sys_ID']=i[0]
                settings['Title']=i[1]
                settings['Links']=i[2]
                settings['User']=i[3]
                settings['Status']=i[4]
                settings['L_up']=i[5]
                config.settings.append(settings)
                settings={}
                #print(i[4])
                bar.next()
   
    def check_id(id,table):
        if table == "link":
            dbmoto.mycursor.execute("SELECT * FROM link WHERE ID ='"+id+"'")
            myresult = dbmoto.mycursor.fetchall()
            lst =[]
            for x in myresult:
                lst.append(str(x[1]))         
            if str(id) in lst :
                return True

            else:
                return False
        elif table == "m_article":    
            dbmoto.mycursor.execute("SELECT * FROM m_article WHERE ID ='"+id+"'")
            myresult = dbmoto.mycursor.fetchall()
            lst =[]
            for x in myresult:
                lst.append(str(x[0]))          
            if str(id) in lst :
                return True
            else:
                return False
        elif table == "m_pictures":    
            dbmoto.mycursor.execute("SELECT * FROM m_pictures WHERE IMG_ID ='"+id+"'")
            myresult = dbmoto.mycursor.fetchall()
            lst =[]
            for x in myresult:
                lst.append(str(x[1]))          
            if str(id) in lst :
                return True
            else:
                return False
        elif table == "m_location":    
            dbmoto.mycursor.execute("SELECT * FROM m_location WHERE ID ='"+id+"'")
            myresult = dbmoto.mycursor.fetchall()
            lst =[]
            for x in myresult:
                lst.append(str(x[0]))          
            if str(id) in lst :
                return True
            else:
                return False
                
    def add_items():
        #with Bar('      Updateing links table!',max = len(config.d_list)) as bar:
        for a in config.d_list:
            config.time_update()
            #print (dbmoto.check_id(a['ID']))
            if dbmoto.check_id(a['ID'],"link") is not True:
                val=[]
                sql = "INSERT INTO link (Sys_ID ,ID, Title, Link,Status,Timeup) VALUES (%s,%s, %s, %s,%s,%s)"
                val = (a['Sys_ID'],int(a['ID']),a['Title'],a['Link'],"Active",config.date)
                dbmoto.mycursor.execute(sql,val)
                config.mydb.commit()
                #print(dbmoto.mycursor.rowcount, "record inserted to links table.")
                config.d_list=[]
            else:
                #print ("exist:",a['ID'])
                dbmoto.update_items("link",a['ID'])
                config.d_list=[]
                #bar.next()
        #with Bar('      Updateing m_article table!',max = len(config.a_list)) as bar:
        for a in config.a_list:
            config.time_update()
            if dbmoto.check_id(a['ID'],"m_article") is not True:
                val=[]
                days= time_delta(str(config.date),a['Since']+":00.100001")
                sql = "INSERT INTO m_article (ID, Since, Title, Price, Year, Milage, Fuel, Type,Timeup,Days) VALUES (%s, %s, %s,%s, %s, %s,%s,%s,%s,%s)"
                val = (int(a['ID']),a['Since'],a['Title'],a['Price'],a['Year'],a['Milage'],a['Fuel'],a['Type'],config.date,days)
                dbmoto.mycursor.execute(sql,val)
                config.mydb.commit()
                #print(dbmoto.mycursor.rowcount, "record inserted to m_article table.")
                config.a_list=[]
            else:
                #print ("exist",a['ID'])
                dbmoto.update_items("m_article",a['ID'],data={'Since':a['Since'],'Title':a['Title'],'Price':a['Price'],'Year':a['Year'],'Milage':a['Milage'],'Fuel':a['Fuel'],'Type':a['Type']})
                config.a_list=[]
            #bar.next()
        #with Bar('      Updateing m_pictures table!',max = len(config.p_list)) as bar:
        for a in config.p_list:
               if dbmoto.check_id(a['IMG_ID'],"m_pictures") is not True:
                   config.time_update()
                   val=[]
                   sql = "INSERT INTO m_pictures (ID,IMG_ID,F_Name,Link,Image,Timeup) Values (%s,%s,%s,%s,%s,%s)"
                   val = (int(a['ID']),a['IMG_ID'],a['F_Name'],a['Link'],a['Image'],config.date)
                   dbmoto.mycursor.execute(sql,val)
                   config.mydb.commit()
                   #print(dbmoto.mycursor.rowcount, "record inserted to m_pictures table.")
                   config.p_list=[]
                   #bar.next()
        config.p_list=[]
        for a in config.l_list:
            #print (config.l_list)
            if dbmoto.check_id(a['ID'],"m_location") is not True:
                   config.time_update()
                   val=[]
                   sql = "INSERT INTO m_location (ID,Title,Link,Lng,Lat,Timeup) Values (%s,%s,%s,%s,%s,%s)"
                   val = (int(a['ID']),a['Title'],a['Link'],'"'+a['Long']+'"','"'+a['Lat']+'"',config.date)
                   dbmoto.mycursor.execute(sql,val)
                   config.mydb.commit()
                   #print(dbmoto.mycursor.rowcount, "record inserted to m_pictures table.")
                   config.l_list=[]

    def get_since(id):
        dbmoto.mycursor.execute("SELECT Since FROM m_article WHERE ID ='"+id+"'")
        myresult = dbmoto.mycursor.fetchall()
        for i in myresult:
            since = i[0]
        return str(since.strftime("%Y-%m-%d %H:%M:%S.%f"))

    def update_items(table,ID,*args, **kwargs):
        config.time_update()
        if table =="link":
            sql = "UPDATE link SET Timeup = '"+str(config.date)+"' WHERE link.ID = '"+ID+"'"
            dbmoto.mycursor.execute(sql)
            config.mydb.commit()
            #print(dbmoto.mycursor.rowcount, "record updated in links table.")
        elif table == "m_article":
            config.time_update()
            if kwargs:
                val=kwargs.get('data')
                #print (dbmoto.get_since(ID))
                days= time_delta(str(config.date),dbmoto.get_since(ID))
                sql = "UPDATE m_article SET Title = '"+val['Title']+"', Price = '"+val['Price']+"', Year = '"+val['Year']+"', Milage = '"+val['Milage']+"', Fuel = '"+val['Fuel']+"', Type = '"+val['Type']+"', Timeup = '"+str(config.date)+"', `Days` = '"+str(days)+"' WHERE m_article.ID = '"+ID+"'"
                #val = (int(a['ID']),a['Since'],a['Title'],a['Price'],a['Year'],a['Milage'],a['Fuel'],a['Type'],config.date,days)
                dbmoto.mycursor.execute(sql)
                config.mydb.commit()
                #print(dbmoto.mycursor.rowcount, "record updated in m_article table.")
        elif table == "m_article&link_incative":
            if kwargs:
                val=kwargs.get('data')
                config.time_update()
                if val['Status'] == 'Inactive':
                    days= time_delta(str(config.date),val['Since']+".100001")
                    sql1 = "UPDATE link SET Timeup = '"+str(config.date)+"', Status='Inactive' WHERE link.ID = '"+str(ID)+"'"
                    dbmoto.mycursor.execute(sql1)
                    sql2 = "UPDATE m_article SET Timeup = '"+str(config.date)+"', `Days` = '"+str(days)+"' WHERE m_article.ID = '"+str(ID)+"'"
                    dbmoto.mycursor.execute(sql2)
                    config.mydb.commit()
                    #print(dbmoto.mycursor.rowcount, "record updated in m_article and links table due to inactive datacheck.")
                elif val['Status'] == 'Active':
                    days= time_delta(str(config.date),val['Since']+".100001")
                    sql1 = "UPDATE link SET Timeup = '"+str(config.date)+"', Status='Active' WHERE links.ID = '"+str(ID)+"'"
                    dbmoto.mycursor.execute(sql1)
                    sql2 = "UPDATE m_article SET Timeup = '"+str(config.date)+"', `Days` = '"+str(days)+"' WHERE m_article.ID = '"+str(ID)+"'"
                    dbmoto.mycursor.execute(sql2)
                    config.mydb.commit()
                    #print(dbmoto.mycursor.rowcount, "record updated in m_article and links table due to inactive datacheck.")

    def add_log():
        if len(config.sys_log) >0:
            for a in config.sys_log:
                config.time_update()      
                val=[]
                sql = "INSERT INTO sys_log (Timeup,ID,Category,Activity,Message ) VALUES (%s,%s, %s, %s,%s)"
                val = (a['Timeup'],int(a['ID']),a['Category'],a['Activity'],a['Message'])
                dbmoto.mycursor.execute(sql,val)
                config.mydb.commit()
                #print(dbmoto.mycursor.rowcount, "record inserted to Sys_log table.")
                val1=[]
                sql1 = "INSERT INTO sys_log (Timeup,ID,Category,Activity,Message ) VALUES (%s,%s, %s, %s,%s)"
                val1 = (a['Timeup'],int(a['ID']),"Info","SQL Insert","record inserted to Sys_log table.")
                dbmoto.mycursor.execute(sql1,val1)
                config.mydb.commit()
            #timen=datetime.datetime.now()
            config.sys_log =[]
            

    def check_exist():
        dbmoto.mycursor.execute("SELECT * FROM v_notify")
        myresult = dbmoto.mycursor.fetchall()
        #print (myresult)
        for i in myresult:
            config.time_update()
            config.h_data['ID']=i[0]
            config.h_data['Sys_ID']=i[1]
            config.h_data['Link']=i[2]
            config.h_data['Days']=i[3]
            config.h_data['Since']=i[4]
            config.h_data['Timeup']=i[5]
            config.h_data['Status']=i[6]
            config.h_list.append(config.h_data)
            config.h_data={}
def main():
    while True:
        config.time_update()
        print("Processing started at: "+str(config.date))
        config.time_update()
        config.mydb.connect()
        config.settings=[]
        dbmoto.get_config()
        pool.hist_article_check()
        with Bar('Processing searches!',max = len(config.settings)) as bar:
            for a in config.settings:
                if int(a['Status']) == 1:
                    pool.article_list(a['Links'],a['Sys_ID'],)
                    #print(len(config.d_list))
                    #for a in config.d_list:
                    #    print (a)
                    pool.article_fetch()
                    #print(len(config.a_list))
                    #for a in config.a_list:
                    #    print (a)
                        
                    dbmoto.add_items()
                else:
                    print("No active searches for!:"+a['Title'],a['Status'])
                    config.mydb.close()
                bar.next()
        dbmoto.add_log()
        time.sleep(3600)
if __name__=="__main__":
        main()
       