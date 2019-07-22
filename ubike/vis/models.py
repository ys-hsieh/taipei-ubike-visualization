from django.db import models

# Create your models here.
###############################################################################################################
# Ubike models
###############################################################################################################
# All Ubike data from Taipei City Government (https://www.gov.taipei/)
# All open data fetched from Taipei city traffic realtime Data (https://taipeicity.github.io/traffic_realtime/)
# The following Ubike data is updated in every 10 mins:
#   1. UbikeStop      (10 min)
###############################################################################################################

class UbikeStop(models.Model):
    ###########################################################################################################
    # Meaning for these variables
    ###########################################################################################################
    # sno(站點代號)
    # sna(中文場站名稱)
    # tot(場站總停車格)
    # sbi(可借車位數)
    # sarea(中文場站區域)
    # mday(資料更新時間)
    # lat(緯度)
    # lng(經度)
    # ar(中文地址)
    # sareaen(英文場站區域)
    # snaen(英文場站名稱)
    # aren(英文地址)
    # bemp(可還空位數)
    # act(場站是否暫停營運)
    # num
    ###########################################################################################################
    # Example
    ###########################################################################################################
    # 'sno': '0001', 
    # 'sna': '捷運市政府站(3號出口)',
    # 'tot': '180', 
    # 'sbi': '0',
    # 'sarea': '信義區',
    # 'mday': '20190622032019',
    # 'lat': '25.0408578889',
    # 'lng': '121.567904444',
    # 'ar': '忠孝東路/松仁路(東南側)', 
    # 'sareaen': 'Xinyi Dist.',
    # 'snaen': 'MRT Taipei City Hall Stataion(Exit 3)-2', 
    # 'aren': 'The S.W. side of Road Zhongxiao East Road & Road Chung Yan.', 
    # 'bemp': '180', 
    # 'act': '1'

    sno = models.IntegerField()
    sna = models.TextField()
    tot = models.IntegerField()
    sbi = models.IntegerField()
    sarea = models.TextField()
    mday = models.DateTimeField()
    lat = models.FloatField()
    lng = models.FloatField()
    ar = models.TextField()
    sareaen = models.TextField()
    snaen = models.TextField()
    aren = models.TextField()
    bemp = models.IntegerField()
    act = models.BooleanField()
    num = models.BigIntegerField()


    class Meta:
        ordering = ['-sno']


    def __str__(self):
        return self.sna

    
class StopStatus(models.Model):
    sno = models.IntegerField(unique=True)
    sna = models.TextField()
    tot = models.IntegerField()
    sarea = models.TextField()
    lat = models.FloatField()
    lng = models.FloatField()
    ar = models.TextField()
    sareaen = models.TextField()
    snaen = models.TextField()
    aren = models.TextField()
    act = models.BooleanField()


    class Meta:
        ordering = ['-sno']

    
    def __str__(self):
        return self.sna


class FetchUbikeDataRecord(models.Model):
    num = models.BigIntegerField()
    mday = models.DateTimeField()

    class Meta:
        ordering = ['-num']

    def __str__(self):
        return self.num


###############################################################################################################
# Weather models
###############################################################################################################
# All weather data from Central Weather Bureau (https://www.cwb.gov.tw/V7/forecast/)
# All open data fetched from CWB Open Weather Data (https://opendata.cwb.gov.tw/index)
# The following are three different weather data:
#   1. AutoWeatherData      (1 hr)
#   2. AutoRainData         (10 min)
#   3. BureauWeatherData    (10 min)
###############################################################################################################

class AutoWeatherData(models.Model):
    ###########################################################################################################
    # Meaning for these variables
    ###########################################################################################################
    # lat 緯度 (座標系統採TWD67)，單位 度
    # lon 經度 (座標系統採TWD67)，單位 度
    # locationName 測站名稱
    # stationId 測站ID
    # obsTime 觀測資料時間
    # ELE 高度，單位 公尺
    # WDIR 風向，單位 度，一般風向 0 表示無風
    # WDSD 風速，單位 公尺/秒
    # TEMP 溫度，單位 攝氏
    # HUMD 相對濕度，單位 百分比率，此處以實數 0-1.0 記錄
    # PRES 測站氣壓，單位 百帕
    # SUN 日照時數，單位 小時
    # H_24R 日累積雨量，單位 毫米
    # H_FX 小時最大陣風風速，單位 公尺/秒
    # H_XD 小時最大陣風風向，單位 度
    # H_FXT 小時最大陣風時間，yyyy-MM-ddThh:mm:ss+08:00
    # D_TX 本日最高溫，單位 攝氏
    # D_TXT 本日最高溫發生時間，hhmm (小時分鐘)
    # D_TN 本日最低溫，單位 攝氏
    # D_TNT 本日最低溫發生時間，hhmm (小時分鐘)
    # CITY 縣市
    # CITY_SN 縣市編號
    # TOWN 鄉鎮
    # TOWN_SN 鄉鎮編號
    ###########################################################################################################
    # Example
    ###########################################################################################################
    # "lat":"25.079722",
    # "lon":"121.534722",
    # "locationName":"大直",
    # "stationId":"C0A9A0",
    # "time":{"obsTime":"2019-07-19 12:00:00"},
    # "weatherElement":[
    #     {"elementName":"ELEV","elementValue":"24.0"},
    #     {"elementName":"WDIR","elementValue":"306"},
    #     {"elementName":"WDSD","elementValue":"2.2"},
    #     {"elementName":"TEMP","elementValue":"33.1"},
    #     {"elementName":"HUMD","elementValue":"0.61"},
    #     {"elementName":"PRES","elementValue":"996.5"},
    #     {"elementName":"SUN","elementValue":"-99"},
    #     {"elementName":"H_24R","elementValue":"33.0"},
    #     {"elementName":"H_FX","elementValue":"-99"},
    #     {"elementName":"H_XD","elementValue":"-99"},
    #     {"elementName":"H_FXT","elementValue":"-99"},
    #     {"elementName":"D_TX","elementValue":"34.00"},
    #     {"elementName":"D_TXT","elementValue":"null"},
    #     {"elementName":"D_TN","elementValue":"26.60"},
    #     {"elementName":"D_TNT","elementValue":"null"}
    # ],
    # "parameter":[
    #     {"parameterName":"CITY","parameterValue":"臺北市"},
    #     {"parameterName":"CITY_SN","parameterValue":"01"},
    #     {"parameterName":"TOWN","parameterValue":"中山區"},
    #     {"parameterName":"TOWN_SN","parameterValue":"026"}
    # ]
    ###########################################################################################################

    lat = models.FloatField()
    lon = models.FloatField()
    locationName = models.TextField()
    stationId = models.TextField()
    obsTime = models.DateTimeField()
    ELE = models.FloatField()
    WDIR = models.FloatField()
    WDSD = models.FloatField()
    TEMP = models.FloatField()
    HUMD = models.FloatField()
    PRES = models.FloatField()
    SUN = models.FloatField()
    H_24R = models.FloatField()
    H_FX = models.FloatField()
    H_XD = models.FloatField()
    H_FXT = models.FloatField()
    D_TX = models.FloatField()
    D_TXT = models.FloatField()
    D_TN = models.FloatField()
    D_TNT = models.FloatField()
    CITY = models.TextField()
    CITY_SN = models.FloatField()
    TOWN = models.TextField()
    TOWN_SN = models.FloatField()
    num = models.BigIntegerField()

    class Meta:
        ordering = ['-stationId']

    def __str__(self):
        return self.stationId


class AutoWeatherStation(models.Model):
    lat = models.FloatField()
    lon = models.FloatField()
    locationName = models.TextField()
    stationId = models.TextField()
    CITY = models.TextField()
    CITY_SN = models.IntegerField()
    TOWN = models.TextField()
    TOWN_SN = models.IntegerField()

    class Meta:
        ordering = ['-stationId']

    def __str__(self):
        return self.stationId


class FetchAutoWeatherDataRecord(models.Model):
    num = models.BigIntegerField()
    mday = models.DateTimeField()

    class Meta:
        ordering = ['-num']

    def __str__(self):
        return self.num


class AutoRainData(models.Model):
    ###########################################################################################################
    # Meaning for these variables
    ###########################################################################################################
    # lat 緯度 (座標系統採TWD67)，單位 度
    # lon 經度 (座標系統採TWD67)，單位 度
    # locationName 測站名稱
    # stationId 測站ID
    # obsTime 觀測資料時間
    # elementName 中文說明
    # ELEV 高度，單位 公尺
    # RAIN 60分鐘累積雨量，單位 毫米
    # MIN_10 10分鐘累積雨量，單位 毫米
    # HOUR_3 3小時累積雨量，單位 毫米
    # HOUR_6 6小時累積雨量，單位 毫米
    # HOUR_12 12小時累積雨量，單位 毫米
    # HOUR_24 24小時累積雨量，單位 毫米
    # NOW 本日累積雨量
    # latest_2days 前1日0時到現在之累積雨量
    # latest_3days 前2日0時到現在之累積雨量
    # CITY 縣市
    # CITY_SN 縣市編號
    # TOWN 鄉鎮
    # TOWN_SN 鄉鎮編號
    # ATTRIBUTE 自動站屬性
    ###########################################################################################################
    # Example
    ###########################################################################################################
    # "lat":"25.0394",
    # "lon":"121.5067",
    # "locationName":"臺北",
    # "stationId":"466920",
    # "time":{"obsTime":"2019-07-15 17:40:00"},
    # "weatherElement":[
    #     {"elementName":"ELEV","elementValue":"6.30"},
    #     {"elementName":"RAIN","elementValue":"-998.00"},
    #     {"elementName":"MIN_10","elementValue":"-998.00"},
    #     {"elementName":"HOUR_3","elementValue":"-998.00"},
    #     {"elementName":"HOUR_6","elementValue":"-998.00"},
    #     {"elementName":"HOUR_12","elementValue":"0.00"},
    #     {"elementName":"HOUR_24","elementValue":"2.00"},
    #     {"elementName":"NOW","elementValue":"0.00"},
    #     {"elementName":"latest_2days","elementValue":"2.00"},
    #     {"elementName":"latest_3days","elementValue":"2.00"}
    # ],
    # "parameter":[
    #     {"parameterName":"CITY","parameterValue":"臺北市"},
    #     {"parameterName":"CITY_SN","parameterValue":"01"},
    #     {"parameterName":"TOWN","parameterValue":"中正區"},
    #     {"parameterName":"TOWN_SN","parameterValue":"036"},
    #     {"parameterName":"ATTRIBUTE","parameterValue":"中央氣象局"}
    # ]
    ###########################################################################################################
    
    lat = models.FloatField()
    lon = models.FloatField()
    locationName = models.TextField()
    stationId = models.TextField()
    obsTime = models.DateTimeField()
    ELEV = models.FloatField()
    RAIN = models.FloatField()
    MIN_10 = models.FloatField()
    HOUR_3 = models.FloatField()
    HOUR_6 = models.FloatField()
    HOUR_12 = models.FloatField()
    HOUR_24 = models.FloatField()
    NOW = models.FloatField()
    latest_2days = models.FloatField()
    latest_3days = models.FloatField()
    CITY = models.TextField()
    CITY_SN = models.IntegerField()
    TOWN = models.TextField()
    TOWN_SN = models.IntegerField()
    ATTRIBUTE = models.TextField()
    num = models.BigIntegerField()

    class Meta:
        ordering = ['-stationId']

    def __str__(self):
        return self.stationId


class AutoRainStation(models.Model):
    lat = models.FloatField()
    lon = models.FloatField()
    locationName = models.TextField()
    stationId = models.TextField()
    CITY = models.TextField()
    CITY_SN = models.IntegerField()
    TOWN = models.TextField()
    TOWN_SN = models.IntegerField()
    ATTRIBUTE = models.TextField()

    class Meta:
        ordering = ['-stationId']

    def __str__(self):
        return self.stationId


class FetchAutoRainDataRecord(models.Model):
    num = models.BigIntegerField()
    mday = models.DateTimeField()

    class Meta:
        ordering = ['-num']

    def __str__(self):
        return self.num


class BureauWeatherData(models.Model):
    ###########################################################################################################
    # Meaning for these variables
    ###########################################################################################################
    # lat 緯度 (座標系統採TWD67)，單位 度
    # lon 經度 (座標系統採TWD67)，單位 度
    # locationName 測站名稱
    # stationId 測站ID
    # obsTime 觀測資料時間
    # ELEV 高度，單位 公尺
    # WDIR 風向，單位 度，一般風向 0 表示無風
    # WDSD 風速，單位 公尺/秒
    # TEMP 溫度，單位 攝氏
    # HUMD 相對濕度，單位 百分比率，此處以實數 0-1.0 記錄
    # PRES 測站氣壓，單位 百帕
    # R24R 日累積雨量，單位 毫米
    # H_FX 小時最大陣風風速，單位 公尺/秒
    # H_XD 小時最大陣風風向，單位 度
    # H_FXT 小時最大陣風時間，hhmm (小時分鐘)
    # H_F10 本時最大10分鐘平均風速，單位 公尺/秒
    # H_10D 本時最大10分鐘平均風向，單位 度
    # H_F10T 本時最大10分鐘平均風速發生時間，hhmm (小時分鐘)
    # H_UVI 小時紫外線指數
    # D_TX 本日最高溫，單位 攝氏
    # D_TXT 本日最高溫發生時間，hhmm (小時分鐘)
    # D_TN 本日最低溫，單位 攝氏
    # D_TNT 本日最低溫發生時間，hhmm (小時分鐘)
    # D_TS 本日總日照時數，單位 小時
    # H_VIS 本時整點盛行能見度，單位 公里
    # H_Weather 本時整點天氣現象描述
    # CITY 縣市
    # CITY_SN 縣市編號
    # TOWN 鄉鎮
    # TOWN_SN 鄉鎮編號
    ###########################################################################################################
    # Example
    ###########################################################################################################
    # "lat":"25.039410",
    # "lon":"121.506676",
    # "locationName":"臺北",
    # "stationId":"466920",
    # "time":{"obsTime":"2019-07-15 16:10:00"},
    # "weatherElement":[
    #     {"elementName":"ELEV","elementValue":"6.2550"},
    #     {"elementName":"WDIR","elementValue":"40"},
    #     {"elementName":"WDSD","elementValue":"4"},
    #     {"elementName":"TEMP","elementValue":"31.80"},
    #     {"elementName":"HUMD","elementValue":"0.67"},
    #     {"elementName":"PRES","elementValue":"1001.10"},
    #     {"elementName":"24R","elementValue":"0"},
    #     {"elementName":"H_FX","elementValue":"8.70"},
    #     {"elementName":"H_XD","elementValue":"40"},
    #     {"elementName":"H_FXT","elementValue":"1551"},
    #     {"elementName":"H_F10","elementValue":"4"},
    #     {"elementName":"H_10D","elementValue":"40"},
    #     {"elementName":"H_F10T","elementValue":"1555"},
    #     {"elementName":"H_UVI","elementValue":"1.10"},
    #     {"elementName":"D_TX","elementValue":"36.90"},
    #     {"elementName":"D_TXT","elementValue":"1300"},
    #     {"elementName":"D_TN","elementValue":"27.50"},
    #     {"elementName":"D_TNT","elementValue":"530"},
    #     {"elementName":"D_TS","elementValue":"5.70"},
    #     {"elementName":"H_VIS","elementValue":"-99"},
    #     {"elementName":"H_Weather","elementValue":"null"}
    # ],
    # "parameter":[
    #     {"parameterName":"CITY","parameterValue":"臺北市"},
    #     {"parameterName":"CITY_SN","parameterValue":"01"},
    #     {"parameterName":"TOWN","parameterValue":"中正區"},
    #     {"parameterName":"TOWN_SN","parameterValue":"036"}
    # ]
    ###########################################################################################################
    
    lat = models.FloatField()
    lon = models.FloatField()
    locationName = models.TextField()
    stationId = models.TextField()
    obsTime = models.DateTimeField()
    ELEV = models.FloatField()
    WDIR = models.FloatField()
    WDSD = models.FloatField()
    TEMP = models.FloatField()
    HUMD = models.FloatField()
    PRES = models.FloatField()
    R24R = models.FloatField()
    H_FX = models.FloatField()
    H_XD = models.FloatField()
    H_FXT = models.FloatField()
    H_F10 = models.FloatField()
    H_10D = models.FloatField()
    H_F10T = models.FloatField()
    H_UVI = models.FloatField()
    D_TX = models.FloatField()
    D_TXT = models.FloatField()
    D_TN = models.FloatField()
    D_TNT = models.FloatField()
    D_TS = models.FloatField()
    H_VIS = models.FloatField()
    H_Weather = models.TextField()
    CITY = models.TextField()
    CITY_SN = models.IntegerField()
    TOWN = models.TextField()
    TOWN_SN = models.IntegerField()
    num = models.BigIntegerField()

    class Meta:
        ordering = ['-stationId']

    def __str__(self):
        return self.stationId

