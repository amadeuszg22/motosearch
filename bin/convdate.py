from datetime import date, datetime


months={
    "styczeń":"01",
    "styczen":"01",
    "stycznia":"01",
    "luty":"02",
    "lutego":"02",
    "marca":"03",
    "marzec":"03",
    "kwiecień":"04",
    "kwiecien":"04",
    "kwietnia":"04",
    "maj":"05",
    "maja":"05",
    "czerwiec":"06",
    "czerwca":"06",
    "lipiec":"07",
    "lipca":"07",
    "sierpień":"08",
    "sierpnia":"08",
    "sierpien":"08",
    "wrzesien":"09",
    "wrzesnia":"09",
    "wrzesień":"09",
    "września":"09",
    "pazdziernik":"10",
    "pazdziernika":"10",
    "październik":"10",
    "października":"10",
    "listopad":"11",
    "listopada":"11",
    "grudzien":"12",
    "grudzień":"12",
    "grudnia":"12"    
}
def date_convert(mnt):
    if mnt in months:
        return months[mnt]
    else:
        return 0

def time_delta(since,timeup): 
    #date_format = "%Y%m%d%H%M%S"
    since =datetime.strptime(since, "%Y-%m-%d %H:%M:%S.%f")
    timeup =datetime.strptime(timeup, "%Y-%m-%d %H:%M:%S.%f")
    #since=int(datetime.strftime(since, date_format))
    #timeup=int(datetime.strftime(timeup, date_format))
    diff =since-timeup
    #diff = int(timeup)-int(since)
    return diff.days

def main():
    while True:
        print("podaj miesiac:")
        mnt=input()
        date_convert(mnt)
        print("podaj 1st date")
        since =input()
        print("podaj 2st date")
        timeup =input()
        print (time_delta(since,timeup))
if __name__=="__main__":
    main()        