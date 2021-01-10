from win10toast import ToastNotifier
import time
import mysql.connector
import webbrowser
from datetime import datetime
from progress.bar import Bar
import configparser


class config:
    conf=configparser.ConfigParser()
    conf.read('../config.ini')
    mydb = mysql.connector.connect(
    host=conf.get('mysql','host'),
    user=conf.get('mysql','user'),
    password=conf.get('mysql','password'),
    database= conf.get('mysql','database'), 
    )
    data={}
    data_l=[]
    used=[]

    def db_notif_fetch():
        config.mydb.connect()
        mycursor = config.mydb.cursor()
        mycursor.execute("SELECT * FROM v_notify WHERE Days ='0'")
        myresult = mycursor.fetchall()
        config.mydb.close()
        with Bar('Getting new notifications!',max = len(myresult)) as bar:
            for i in myresult:
                if not any(d.get('ID') == i[0] for d in config.data_l):  
                    config.data['ID']=i[0]
                    config.data['Sys_ID']=i[1]
                    config.data['Link']=i[2]
                    config.data['Days']=i[3]
                    config.data['Since']=i[4]
                    config.data['Timeup']=i[5]
                    config.data_l.append(config.data)
                    config.data={}
                #else:
                    #print('exist')
                bar.next()

def toast_action(link, id):
    webbrowser.open(link, new=2)
    config.used.append(id)

def notify(msg): 
    leng=len(msg)
    with Bar('Sending notifications: ',max = len(msg)) as bar:
        for a in msg:
            if a['Days'] == 0 and a['ID'] not in config.used:
                #print (" New notification sent:")
                #print (a)
                toaster = ToastNotifier()
                toaster.show_toast(title="Nowe ogłoszenia dostępne:"+str(leng)+" szt ID: "+str(a['ID']),
                                msg=str(a['Link']),
                                callback_on_click=lambda:toast_action(a['Link'],a['ID']),
                                icon_path=None,
                                duration=10,
                                threaded=True)
                # Wait for threaded notification to finish
                while toaster.notification_active(): time.sleep(0.1)
            #else:
                #print("No new messages!")
            bar.next()


def main():
    while True:
        print(str(datetime.now())+" Processing notifications:")
        config.db_notif_fetch()
        notify(config.data_l)
        #print (config.used)
        
        time.sleep(3600)
if __name__=="__main__":
        main()