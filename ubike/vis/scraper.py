import json
import requests
import datetime
from django.http import HttpResponse

from . import config
from vis.models import UbikeStop, StopStatus, FetchUbikeDataRecord
###############################################################################################################
# Ubike scraper
###############################################################################################################

def ViewTaipeiYouBikeAPIData():
    r = requests.get(config.TaipeiYouBikeAPI)
    print(r.status_code)  
    print(r.headers['content-type'])  
    print(r.encoding)
    jsonData = json.loads(r.content.decode("utf-8"))
    print (jsonData["retVal"]["0005"])


def show(request):
    r = requests.get(config.TaipeiYouBikeAPI)
    #print(r.status_code)  
    #print(r.headers['content-type'])  
    #print(r.encoding)
    jsonData = json.loads(r.content.decode("utf-8"))
    #print (jsonData["retVal"]["0005"])
    #return HttpResponse(jsonData["retVal"]["0005"])
    #return HttpResponse(str(jsonData["retVal"]["0005"]))
    return HttpResponse(str(jsonData))


def fetchTaipeiYouBikeAPIData(request):
    r = requests.get(config.TaipeiYouBikeAPI)
    jsonData = json.loads(r.content.decode("utf-8"))

    for stopDataIndex in jsonData["retVal"]:
        stopData = jsonData["retVal"][stopDataIndex]
        
        # Formate datetime object
        #dateString = str(stopData["mday"]).split("")
        yearInt = int(stopData["mday"][0] + stopData["mday"][1] + stopData["mday"][2] + stopData["mday"][3])
        monthInt = int(stopData["mday"][4] + stopData["mday"][5])
        dayInt = int(stopData["mday"][6] + stopData["mday"][7])
        hourInt = int(stopData["mday"][8] + stopData["mday"][9])
        minuteInt = int(stopData["mday"][10] + stopData["mday"][11])
        secondInt = int(stopData["mday"][12] + stopData["mday"][13])
        
        UbikeStop.objects.create(
            sno = int(stopData["sno"]),
            sna = str(stopData["sna"]),
            tot = int(stopData["tot"]),
            sbi = int(stopData["sbi"]),
            sarea = str(stopData["sarea"]),
            mday = datetime.datetime(yearInt, monthInt, dayInt, hourInt, minuteInt, secondInt),
            lat = float(stopData["lat"]),
            lng = float(stopData["lng"]),
            ar = str(stopData["ar"]),
            sareaen = str(stopData["sareaen"]),
            snaen = str(stopData["snaen"]),
            aren = str(stopData["aren"]),
            bemp = int(stopData["bemp"]),
            act = (stopData["act"] == "1")
        )

    return HttpResponse("Finished at : " + str(jsonData["retVal"]["0001"]["mday"]))


def fetchUbikeStopDataFromAPI(request):
    r = requests.get(config.TaipeiYouBikeAPI)
    jsonData = json.loads(r.content.decode("utf-8"))

    rawDateString = jsonData["retVal"]["0001"]["mday"]
    yearInt = int(rawDateString[0] + rawDateString[1] + rawDateString[2] + rawDateString[3])
    monthInt = int(rawDateString[4] + rawDateString[5])
    dayInt = int(rawDateString[6] + rawDateString[7])
    hourInt = int(rawDateString[8] + rawDateString[9])
    minuteInt = int(rawDateString[10] + rawDateString[11])
    secondInt = int(rawDateString[12] + rawDateString[13])
    datetimeObject = datetime.datetime(yearInt, monthInt, dayInt, hourInt, minuteInt, secondInt)

    # Update Counting
    try:
        firstFetchDataRecordEntry = FetchUbikeDataRecord.objects.get(num=1)

        FetchUbikeDataRecord.objects.create(
            num = FetchUbikeDataRecord.objects.count() + 1,
            mday = datetimeObject
        )
    except FetchUbikeDataRecord.DoesNotExist:
        FetchUbikeDataRecord.objects.create(
            num = 1,
            mday = datetimeObject
        )

    countingNum = FetchUbikeDataRecord.objects.count()

    # Update UbilkeStop
    for stopDataIndex in jsonData["retVal"]:
        stopData = jsonData["retVal"][stopDataIndex]
        
        # Formate datetime object
        #dateString = str(stopData["mday"]).split("")
        #yearInt = int(stopData["mday"][0] + stopData["mday"][1] + stopData["mday"][2] + stopData["mday"][3])
        #monthInt = int(stopData["mday"][4] + stopData["mday"][5])
        #dayInt = int(stopData["mday"][6] + stopData["mday"][7])
        #hourInt = int(stopData["mday"][8] + stopData["mday"][9])
        #minuteInt = int(stopData["mday"][10] + stopData["mday"][11])
        #secondInt = int(stopData["mday"][12] + stopData["mday"][13])
        
        UbikeStop.objects.create(
            sno = int(stopData["sno"]),
            sna = str(stopData["sna"]),
            tot = int(stopData["tot"]),
            sbi = int(stopData["sbi"]),
            sarea = str(stopData["sarea"]),
            #mday = datetime.datetime(yearInt, monthInt, dayInt, hourInt, minuteInt, secondInt),
            mday = datetimeObject,
            lat = float(stopData["lat"]),
            lng = float(stopData["lng"]),
            ar = str(stopData["ar"]),
            sareaen = str(stopData["sareaen"]),
            snaen = str(stopData["snaen"]),
            aren = str(stopData["aren"]),
            bemp = int(stopData["bemp"]),
            act = (stopData["act"] == "1"),
            num = countingNum
        )

    return HttpResponse("Finish updating UbikeStop data at : " + str(jsonData["retVal"]["0001"]["mday"]))


def fetchStopStatusDataFromAPI(request):
    r = requests.get(config.TaipeiYouBikeAPI)
    jsonData = json.loads(r.content.decode("utf-8"))

    for stopDataIndex in jsonData["retVal"]:
        stopData = jsonData["retVal"][stopDataIndex]
        
        try:
            oldStopEntry = StopStatus.objects.get(sno=int(stopData["sno"]))
            oldStopEntry.sno = int(stopData["sno"])
            oldStopEntry.sna = str(stopData["sna"])
            oldStopEntry.tot = int(stopData["tot"])
            oldStopEntry.sarea = str(stopData["sarea"])
            oldStopEntry.lat = float(stopData["lat"])
            oldStopEntry.lng = float(stopData["lng"])
            oldStopEntry.ar = str(stopData["ar"]),
            oldStopEntry.sareaen = str(stopData["sareaen"])
            oldStopEntry.snaen = str(stopData["snaen"])
            oldStopEntry.aren = str(stopData["aren"])
            oldStopEntry.act = (stopData["act"] == "1")

            oldStopEntry.save()

        except StopStatus.DoesNotExist:
            StopStatus.objects.create(
                sno = int(stopData["sno"]),
                sna = str(stopData["sna"]),
                tot = int(stopData["tot"]),
                sarea = str(stopData["sarea"]),
                lat = float(stopData["lat"]),
                lng = float(stopData["lng"]),
                ar = str(stopData["ar"]),
                sareaen = str(stopData["sareaen"]),
                snaen = str(stopData["snaen"]),
                aren = str(stopData["aren"]),
                act = (stopData["act"] == "1")
            )
    
    return HttpResponse("Finish updating StopStatus data at : " + str(jsonData["retVal"]["0001"]["mday"]))


