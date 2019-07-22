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

