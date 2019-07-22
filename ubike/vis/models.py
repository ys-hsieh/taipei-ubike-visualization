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

