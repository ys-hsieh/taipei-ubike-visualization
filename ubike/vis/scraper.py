import json
import requests
import datetime
from django.http import HttpResponse

from . import config
from vis.models import UbikeStop, StopStatus, FetchUbikeDataRecord
from vis.models import AutoWeatherData, AutoWeatherStation, FetchAutoWeatherDataRecord
from vis.models import AutoRainData, AutoRainStation, FetchAutoRainDataRecord
from vis.models import BureauWeatherData, BureauWeatherStation, FetchBureauWeatherDataRecord

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


###############################################################################################################
# 2. Weather scraper
###############################################################################################################

# 2-1. AutoWeatherData (1 hr)
def fetchAutoWeatherDataFromAPI(request):
    # 2-1-1. Fetch data from AutoCurrentWeatherAPI URL
    r = requests.get(config.AutoCurrentWeatherAPI)
    jsonData = json.loads(r.content.decode("utf-8"))

    if jsonData["success"] == "true":
        # 2-1-2. Create datetimeObject
        rawDateString = jsonData["records"]["location"][0]["time"]["obsTime"]
        yearInt = int(rawDateString[0] + rawDateString[1] + rawDateString[2] + rawDateString[3])
        monthInt = int(rawDateString[5] + rawDateString[6])
        dayInt = int(rawDateString[8] + rawDateString[9])
        hourInt = int(rawDateString[11] + rawDateString[12])
        minuteInt = int(rawDateString[14] + rawDateString[15])
        secondInt = int(rawDateString[17] + rawDateString[18])
        datetimeObject = datetime.datetime(yearInt, monthInt, dayInt, hourInt, minuteInt, secondInt)

        # 2-1-3. Update Counter
        try:
            firstFetchDataRecordEntry = FetchAutoWeatherDataRecord.objects.get(num=1)

            FetchAutoWeatherDataRecord.objects.create(
                num = FetchAutoWeatherDataRecord.objects.count() + 1,
                mday = datetimeObject
            )
        except FetchAutoWeatherDataRecord.DoesNotExist:
            FetchAutoWeatherDataRecord.objects.create(
                num = 1,
                mday = datetimeObject
            )

        countingNum = FetchAutoWeatherDataRecord.objects.count()

        # 2-1-4. Store fetched data
        for autoWeatherData in jsonData["records"]["location"]:
            # weatherElement
            elev = 0.0
            wdir = 0.0
            wdsd = 0.0
            temp = 0.0
            humd = 0.0
            pres = 0.0
            sun = 0.0
            h_24r = 0.0
            h_fx = 0.0
            h_xd = 0.0
            h_fxt = 0.0
            d_tx = 0.0
            d_txt  = 0.0
            d_tn = 0.0
            d_tnt = 0.0

            for weatherElement in autoWeatherData["weatherElement"]:
                if weatherElement["elementName"] == "ELEV":
                    elev = float(weatherElement["elementValue"])
                elif weatherElement["elementName"] == "WDIR":
                    wdir = float(weatherElement["elementValue"])
                elif weatherElement["elementName"] == "WDSD":
                    wdsd = float(weatherElement["elementValue"])
                elif weatherElement["elementName"] == "TEMP":
                    temp = float(weatherElement["elementValue"])
                elif weatherElement["elementName"] == "HUMD":
                    humd = float(weatherElement["elementValue"])
                elif weatherElement["elementName"] == "PRES":
                    pres = float(weatherElement["elementValue"])
                elif weatherElement["elementName"] == "SUN":
                    sun = float(weatherElement["elementValue"])
                elif weatherElement["elementName"] == "H_24R":
                    h_24r = float(weatherElement["elementValue"])
                elif weatherElement["elementName"] == "H_FX":
                    h_fx = float(weatherElement["elementValue"])
                elif weatherElement["elementName"] == "H_XD":
                    h_xd = float(weatherElement["elementValue"])
                elif weatherElement["elementName"] == "H_FXT":
                    if weatherElement["elementValue"] == "null":
                        h_fxt = 0
                    else:
                        h_fxt = float(weatherElement["elementValue"])
                elif weatherElement["elementName"] == "D_TX":
                    d_tx = float(weatherElement["elementValue"])
                elif weatherElement["elementName"] == "D_TXT":
                    if weatherElement["elementValue"] == "null":
                        d_txt = 0
                    else:
                        d_txt = float(weatherElement["elementValue"])
                elif weatherElement["elementName"] == "D_TN":
                    d_tn = float(weatherElement["elementValue"])
                elif weatherElement["elementName"] == "D_TNT":
                    if weatherElement["elementValue"] == "null":
                        d_tnt = 0
                    else:    
                        d_tnt = float(weatherElement["elementValue"])

            # parameter
            city = ""
            citySN = 0
            town = ""
            townSN = 0
            
            for parameter in autoWeatherData["parameter"]:
                if parameter["parameterName"] == "CITY":
                    city = str(parameter["parameterValue"])
                elif parameter["parameterName"] == "CITY_SN":
                    citySN = int(parameter["parameterValue"])
                elif parameter["parameterName"] == "TOWN":
                    town = str(parameter["parameterValue"])
                elif parameter["parameterName"] == "TOWN_SN":
                    townSN = int(parameter["parameterValue"])
            
            if citySN != 1: # check if the station is in taipei
                continue

            AutoWeatherData.objects.create(
                lat = float(autoWeatherData["lat"]),
                lon = float(autoWeatherData["lon"]),
                locationName = str(autoWeatherData["locationName"]),
                stationId = str(autoWeatherData["stationId"]),
                obsTime = datetimeObject,
                ELEV = elev,
                WDIR = wdir,
                WDSD = wdsd,
                TEMP = temp,
                HUMD = humd,
                PRES = pres,
                SUN = sun,
                H_24R = h_24r,
                H_FX = h_fx,
                H_XD = h_xd,
                H_FXT = h_fxt,
                D_TX = d_tx,
                D_TXT = d_txt,
                D_TN = d_tn,
                D_TNT = d_tnt,
                CITY = city,
                CITY_SN = citySN,
                TOWN = town,
                TOWN_SN = townSN,
                num = countingNum
            )

        return HttpResponse("Finish updating AutoWeatherData at : " + str(jsonData["records"]["location"][0]["time"]["obsTime"]))
    
    else:
        return HttpResponse("Fail to update AutoWeatherData at : " + str(datetime.now()))


# 2-2. AutoWeatherStation (1 hr)
def fetchAutoWeatherStationFromAPI(request):
    # 2-2-1. Fetch data from AutoCurrentWeatherAPI URL
    r = requests.get(config.AutoCurrentWeatherAPI)
    jsonData = json.loads(r.content.decode("utf-8"))
    
    if jsonData["success"] == "true":
        # 2-2-2. Store fetched data
        for autoWeatherStationData in jsonData["records"]["location"]:

            # parameter
            city = ""
            citySN = 0
            town = ""
            townSN = 0

            for parameter in autoWeatherStationData["parameter"]:
                if parameter["parameterName"] == "CITY":
                    city = str(parameter["parameterValue"])
                elif parameter["parameterName"] == "CITY_SN":
                    citySN = int(parameter["parameterValue"])
                elif parameter["parameterName"] == "TOWN":
                    town = str(parameter["parameterValue"])
                elif parameter["parameterName"] == "TOWN_SN":
                    townSN = int(parameter["parameterValue"])

            if citySN != 1: # check if the station is in taipei
                continue

            try:
                oldStationEntry = AutoWeatherStation.objects.get(stationId=str(autoWeatherStationData["stationId"]))
                oldStationEntry.lat = float(autoWeatherStationData["lat"])
                oldStationEntry.lon = float(autoWeatherStationData["lon"])
                oldStationEntry.locationName = str(autoWeatherStationData["locationName"])
                oldStationEntry.stationId = str(autoWeatherStationData["stationId"])
                oldStationEntry.CITY = city
                oldStationEntry.CITY_SN = citySN
                oldStationEntry.TOWN = town
                oldStationEntry.TOWN_SN = townSN

            except AutoWeatherStation.DoesNotExist:
                AutoWeatherStation.objects.create(
                    lat = float(autoWeatherStationData["lat"]),
                    lon = float(autoWeatherStationData["lon"]),
                    locationName = str(autoWeatherStationData["locationName"]),
                    stationId = str(autoWeatherStationData["stationId"]),
                    CITY = city,
                    CITY_SN = citySN,
                    TOWN = town,
                    TOWN_SN = townSN
                )

        return HttpResponse("Finish updating AutoWeatherStation at : " + str(jsonData["records"]["location"][0]["time"]["obsTime"]))
    
    else:
        return HttpResponse("Fail to update AutoWeatherStation at : " + str(datetime.now()))


# 2-3. AutoRainData (10 min)
def fetchAutoRainDataFromAPI(request):
    # 2-3-1. Fetch data from AutoRainDataAPI URL
    r = requests.get(config.AutoCurrentRainAPI)
    jsonData = json.loads(r.content.decode("utf-8"))
    
    if jsonData["success"] == "true":
        # 2-3-2. Create datetimeObject
        rawDateString = jsonData["records"]["location"][0]["time"]["obsTime"]
        yearInt = int(rawDateString[0] + rawDateString[1] + rawDateString[2] + rawDateString[3])
        monthInt = int(rawDateString[5] + rawDateString[6])
        dayInt = int(rawDateString[8] + rawDateString[9])
        hourInt = int(rawDateString[11] + rawDateString[12])
        minuteInt = int(rawDateString[14] + rawDateString[15])
        secondInt = int(rawDateString[17] + rawDateString[18])
        datetimeObject = datetime.datetime(yearInt, monthInt, dayInt, hourInt, minuteInt, secondInt)

        # 2-3-3. Update Counter
        try:
            firstFetchDataRecordEntry = FetchAutoRainDataRecord.objects.get(num=1)

            FetchAutoRainDataRecord.objects.create(
                num = FetchAutoRainDataRecord.objects.count() + 1,
                mday = datetimeObject
            )
        except FetchAutoRainDataRecord.DoesNotExist:
            FetchAutoRainDataRecord.objects.create(
                num = 1,
                mday = datetimeObject
            )

        countingNum = FetchAutoRainDataRecord.objects.count()

        # 2-3-4. Store fetched data
        for autoRainData in jsonData["records"]["location"]:
            # weatherElement
            elev = 0.0
            rain = 0.0
            min10 = 0.0
            hour3 = 0.0
            hour6 = 0.0
            hour12 = 0.0
            hour24 = 0.0
            now = 0.0
            latest2days = 0.0
            latest3days = 0.0

            for weatherElement in autoRainData["weatherElement"]:
                if weatherElement["elementName"] == "ELEV":
                    elev = float(weatherElement["elementValue"])
                elif weatherElement["elementName"] == "RAIN":
                    rain = float(weatherElement["elementValue"])
                elif weatherElement["elementName"] == "MIN_10":
                    min10 = float(weatherElement["elementValue"])
                elif weatherElement["elementName"] == "HOUR_3":
                    hour3 = float(weatherElement["elementValue"])
                elif weatherElement["elementName"] == "HOUR_6":
                    hour6 = float(weatherElement["elementValue"])
                elif weatherElement["elementName"] == "HOUR_12":
                    hour12 = float(weatherElement["elementValue"])
                elif weatherElement["elementName"] == "HOUR_24":
                    hour24 = float(weatherElement["elementValue"])
                elif weatherElement["elementName"] == "NOW":
                    now = float(weatherElement["elementValue"])
                elif weatherElement["elementName"] == "latest_2days":
                    latest2days = float(weatherElement["elementValue"])
                elif weatherElement["elementName"] == "latest_3days":
                    latest3days = float(weatherElement["elementValue"])
            
            # parameter
            city = ""
            citySN = 0
            town = ""
            townSN = 0
            attribute = ""

            for parameter in autoRainData["parameter"]:
                if parameter["parameterName"] == "CITY":
                    city = str(parameter["parameterValue"])
                elif parameter["parameterName"] == "CITY_SN":
                    citySN = int(parameter["parameterValue"])
                elif parameter["parameterName"] == "TOWN":
                    town = str(parameter["parameterValue"])
                elif parameter["parameterName"] == "TOWN_SN":
                    townSN = int(parameter["parameterValue"])
                elif parameter["parameterName"] == "ATTRIBUTE":
                    attribute = str(parameter["parameterValue"])

            if citySN != 1: # check if the station is in taipei
                continue

            AutoRainData.objects.create(
                lat = float(autoRainData["lat"]),
                lon = float(autoRainData["lon"]),
                locationName = str(autoRainData["locationName"]),
                stationId = str(autoRainData["stationId"]),
                obsTime = datetimeObject,
                ELEV = elev,
                RAIN = rain,
                MIN_10 = min10,
                HOUR_3 = hour3,
                HOUR_6 = hour6,
                HOUR_12 = hour12,
                HOUR_24 = hour24,
                NOW = now,
                latest_2days = latest2days,
                latest_3days = latest3days,
                CITY = city,
                CITY_SN = citySN,
                TOWN = town,
                TOWN_SN = townSN,
                ATTRIBUTE = attribute,
                num = countingNum
            )

        return HttpResponse("Finish updating AutoRainData at : " + str(jsonData["records"]["location"][0]["time"]["obsTime"]))
    
    else:
        return HttpResponse("Fail to update AutoRainData at : " + str(datetime.now()))

# 2-4. AutoRainStation (10 min)
def fetchAutoRainStationFromAPI(request):
    # 2-4-1. Fetch data from AutoRainDataAPI URL
    r = requests.get(config.AutoCurrentRainAPI)
    jsonData = json.loads(r.content.decode("utf-8"))
    
    if jsonData["success"] == "true":
        # 2-4-2. Store fetched data
        for autoRainStationData in jsonData["records"]["location"]:

            # parameter
            city = ""
            citySN = 0
            town = ""
            townSN = 0
            attribute = ""

            for parameter in autoRainStationData["parameter"]:
                if parameter["parameterName"] == "CITY":
                    city = str(parameter["parameterValue"])
                elif parameter["parameterName"] == "CITY_SN":
                    citySN = int(parameter["parameterValue"])
                elif parameter["parameterName"] == "TOWN":
                    town = str(parameter["parameterValue"])
                elif parameter["parameterName"] == "TOWN_SN":
                    townSN = int(parameter["parameterValue"])
                elif parameter["parameterName"] == "ATTRIBUTE":
                    attribute = str(parameter["parameterValue"])

            if citySN != 1: # check if the station is in taipei
                continue

            try:
                oldStationEntry = AutoRainStation.objects.get(stationId=str(autoRainStationData["stationId"]))
                oldStationEntry.lat = float(autoRainStationData["lat"])
                oldStationEntry.lon = float(autoRainStationData["lon"])
                oldStationEntry.locationName = str(autoRainStationData["locationName"])
                oldStationEntry.stationId = str(autoRainStationData["stationId"])
                oldStationEntry.CITY = city
                oldStationEntry.CITY_SN = citySN
                oldStationEntry.TOWN = town
                oldStationEntry.TOWN_SN = townSN
                oldStationEntry.ATTRIBUTE = attribute

            except AutoRainStation.DoesNotExist:
                AutoRainStation.objects.create(
                    lat = float(autoRainStationData["lat"]),
                    lon = float(autoRainStationData["lon"]),
                    locationName = str(autoRainStationData["locationName"]),
                    stationId = str(autoRainStationData["stationId"]),
                    CITY = city,
                    CITY_SN = citySN,
                    TOWN = town,
                    TOWN_SN = townSN,
                    ATTRIBUTE = attribute
                )

        return HttpResponse("Finish updating AutoRainStation at : " + str(jsonData["records"]["location"][0]["time"]["obsTime"]))
    
    else:
        return HttpResponse("Fail to update AutoRainStation at : " + str(datetime.now()))


# 2-5. BureauWeatherData    (10 min)
def fetchBureauWeatherDataFromAPI(request):
    # 2-5-1. Fetch data from BureauCurrentWeatherAPI URL
    r = requests.get(config.BureauCurrentWeatherAPI)
    jsonData = json.loads(r.content.decode("utf-8"))
    
    if jsonData["success"] == "true":
        # 2-5-2. Create datetimeObject
        rawDateString = jsonData["records"]["location"][0]["time"]["obsTime"]
        yearInt = int(rawDateString[0] + rawDateString[1] + rawDateString[2] + rawDateString[3])
        monthInt = int(rawDateString[5] + rawDateString[6])
        dayInt = int(rawDateString[8] + rawDateString[9])
        hourInt = int(rawDateString[11] + rawDateString[12])
        minuteInt = int(rawDateString[14] + rawDateString[15])
        secondInt = int(rawDateString[17] + rawDateString[18])
        datetimeObject = datetime.datetime(yearInt, monthInt, dayInt, hourInt, minuteInt, secondInt)

        # 2-5-3. Update Counter
        try:
            firstFetchDataRecordEntry = FetchBureauWeatherDataRecord.objects.get(num=1)

            FetchBureauWeatherDataRecord.objects.create(
                num = FetchBureauWeatherDataRecord.objects.count() + 1,
                mday = datetimeObject
            )
        except FetchBureauWeatherDataRecord.DoesNotExist:
            FetchBureauWeatherDataRecord.objects.create(
                num = 1,
                mday = datetimeObject
            )

        countingNum = FetchBureauWeatherDataRecord.objects.count()

        # 2-5-4. Store fetched data
        for bureauWeatherData in jsonData["records"]["location"]:
            # weatherElement
            elev = 0.0
            wdir = 0.0
            wdsd = 0.0
            temp = 0.0
            humd = 0.0
            pres = 0.0
            r24r = 0.0
            h_fx = 0.0
            h_xd = 0.0
            h_fxt = 0.0
            h_f10 = 0.0
            h_10d = 0.0
            h_f10T = 0.0
            h_uvi = 0.0
            d_tx = 0.0
            d_txt = 0.0
            d_tn = 0.0
            d_tnt = 0.0
            d_ts = 0.0
            h_vis = 0.0
            h_weather = ""
            
            for weatherElement in bureauWeatherData["weatherElement"]:
                if weatherElement["elementName"] == "ELEV":
                    elev = float(weatherElement["elementValue"])
                elif weatherElement["elementName"] == "WDIR":
                    wdir = float(weatherElement["elementValue"])
                elif weatherElement["elementName"] == "WDSD":
                    wdsd = float(weatherElement["elementValue"])
                elif weatherElement["elementName"] == "TEMP":
                    temp = float(weatherElement["elementValue"])
                elif weatherElement["elementName"] == "HUMD":
                    humd = float(weatherElement["elementValue"])
                elif weatherElement["elementName"] == "PRES":
                    pres = float(weatherElement["elementValue"])
                elif weatherElement["elementName"] == "24R":
                    r24r = float(weatherElement["elementValue"])
                elif weatherElement["elementName"] == "H_FX":
                    h_fx = float(weatherElement["elementValue"])
                elif weatherElement["elementName"] == "H_XD":
                    h_xd = float(weatherElement["elementValue"])
                elif weatherElement["elementName"] == "H_FXT":
                    if weatherElement["elementValue"] == "null":
                        h_fxt = 0
                    else:
                        h_fxt = float(weatherElement["elementValue"])
                elif weatherElement["elementName"] == "H_F10":
                    h_f10 = float(weatherElement["elementValue"])
                elif weatherElement["elementName"] == "H_10D":
                    h_10d = float(weatherElement["elementValue"])
                elif weatherElement["elementName"] == "H_F10T":
                    if weatherElement["elementValue"] == "null":
                        h_f10T = 0
                    else:
                        h_f10T = float(weatherElement["elementValue"])
                elif weatherElement["elementName"] == "H_UVI":
                    h_uvi = float(weatherElement["elementValue"])
                elif weatherElement["elementName"] == "D_TX":
                    d_tx = float(weatherElement["elementValue"])
                elif weatherElement["elementName"] == "D_TXT":
                    if weatherElement["elementValue"] == "null":
                        d_txt = 0
                    else:
                        d_txt = float(weatherElement["elementValue"])
                elif weatherElement["elementName"] == "D_TN":
                    d_tn = float(weatherElement["elementValue"])
                elif weatherElement["elementName"] == "D_TNT":
                    if weatherElement["elementValue"] == "null":
                        d_tnt = 0
                    else:
                        d_tnt = float(weatherElement["elementValue"])
                elif weatherElement["elementName"] == "D_TS":
                    d_ts = float(weatherElement["elementValue"])
                elif weatherElement["elementName"] == "H_VIS":
                    h_vis = float(weatherElement["elementValue"])
                elif weatherElement["elementName"] == "H_Weather":
                    h_weather = str(weatherElement["elementValue"])
            
            
            # parameter
            city = ""
            citySN = 0
            town = ""
            townSN = 0

            for parameter in bureauWeatherData["parameter"]:
                if parameter["parameterName"] == "CITY":
                    city = str(parameter["parameterValue"])
                elif parameter["parameterName"] == "CITY_SN":
                    citySN = int(parameter["parameterValue"])
                elif parameter["parameterName"] == "TOWN":
                    town = str(parameter["parameterValue"])
                elif parameter["parameterName"] == "TOWN_SN":
                    townSN = int(parameter["parameterValue"])

            if citySN != 1: # check if the station is in taipei
                continue

            BureauWeatherData.objects.create(
                lat = float(bureauWeatherData["lat"]),
                lon = float(bureauWeatherData["lon"]),
                locationName = str(bureauWeatherData["locationName"]),
                stationId = str(bureauWeatherData["stationId"]),
                obsTime = datetimeObject,
                ELEV = elev,
                WDIR = wdir,
                WDSD = wdsd,
                TEMP = temp,
                HUMD = humd,
                PRES = pres,
                R24R = r24r,
                H_FX = h_fx,
                H_XD = h_xd,
                H_FXT = h_fxt,
                H_F10 = h_f10,
                H_10D = h_10d,
                H_F10T = h_f10T,
                H_UVI = h_uvi,
                D_TX = d_tx,
                D_TXT = d_txt,
                D_TN = d_tn,
                D_TNT = d_tnt,
                D_TS = d_ts,
                H_VIS = h_vis,
                H_Weather = h_weather,
                CITY = city,
                CITY_SN = citySN,
                TOWN = town,
                TOWN_SN = townSN,
                num = countingNum
            )

        return HttpResponse("Finish updating BureauWeatherData at : " + str(jsonData["records"]["location"][0]["time"]["obsTime"]))
    
    else:
        return HttpResponse("Fail to update BureauWeatherData at : " + str(datetime.now()))

# 2-6. BureauWeatherStation    (10 min)
def fetchBureauWeatherStationFromAPI(request):
    # 2-6-1. Fetch data from BureauCurrentWeatherAPI URL
    r = requests.get(config.BureauCurrentWeatherAPI)
    jsonData = json.loads(r.content.decode("utf-8"))
    
    if jsonData["success"] == "true":
        # 2-6-2. Store fetched data
        for bureauWeatherStationData in jsonData["records"]["location"]:

            # parameter
            city = ""
            citySN = 0
            town = ""
            townSN = 0

            for parameter in bureauWeatherStationData["parameter"]:
                if parameter["parameterName"] == "CITY":
                    city = str(parameter["parameterValue"])
                elif parameter["parameterName"] == "CITY_SN":
                    citySN = int(parameter["parameterValue"])
                elif parameter["parameterName"] == "TOWN":
                    town = str(parameter["parameterValue"])
                elif parameter["parameterName"] == "TOWN_SN":
                    townSN = int(parameter["parameterValue"])

            if citySN != 1: # check if the station is in taipei
                continue

            try:
                oldStationEntry = BureauWeatherStation.objects.get(stationId=str(bureauWeatherStationData["stationId"]))
                oldStationEntry.lat = float(bureauWeatherStationData["lat"])
                oldStationEntry.lon = float(bureauWeatherStationData["lon"])
                oldStationEntry.locationName = str(bureauWeatherStationData["locationName"])
                oldStationEntry.stationId = str(bureauWeatherStationData["stationId"])
                oldStationEntry.CITY = city
                oldStationEntry.CITY_SN = citySN
                oldStationEntry.TOWN = town
                oldStationEntry.TOWN_SN = townSN

            except BureauWeatherStation.DoesNotExist:
                BureauWeatherStation.objects.create(
                    lat = float(bureauWeatherStationData["lat"]),
                    lon = float(bureauWeatherStationData["lon"]),
                    locationName = str(bureauWeatherStationData["locationName"]),
                    stationId = str(bureauWeatherStationData["stationId"]),
                    CITY = city,
                    CITY_SN = citySN,
                    TOWN = town,
                    TOWN_SN = townSN
                )

        return HttpResponse("Finish updating BureauWeatherStation at : " + str(jsonData["records"]["location"][0]["time"]["obsTime"]))
    
    else:
        return HttpResponse("Fail to update BureauWeatherStation at : " + str(datetime.now()))


def showData(request):
    returnString = ""
    oldStationEntry = FetchUbikeDataRecord.objects.all()
    for i in oldStationEntry:
        returnString = returnString + "  ////  " + str(i.mday)
    return HttpResponse(returnString)


def main():
    return

if __name__ == "__main__":
    main()