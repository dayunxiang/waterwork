# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import get_object_or_404,render,redirect
from django.http import HttpResponse,JsonResponse,HttpResponseRedirect
from django.contrib import messages

import json
import random
import datetime
import time
from django.template.loader import render_to_string
from django.shortcuts import render,HttpResponse
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView,DeleteView,FormView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import admin
from django.contrib.auth.models import Permission
from django.utils.safestring import mark_safe
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from accounts.models import User,MyRoles

from legacy.models import HdbFlowDataDay,HdbFlowDataMonth,Bigmeter,Alarm

from entm.models import Organizations
# from django.core.urlresolvers import reverse_lazy


def dmastasticinfo():
    organ = Organizations.objects.first()
    organs = organ.get_descendants(include_self=True)

    dmas = None
    for o in organs:
        if dmas is None:
            dmas = o.dma.all()
        else:
            dmas |= o.dma.all()

    data = []
    for dma in dmas:

        dmastation = dma.dmastation.first()
        if dmastation is None:
            continue
        commaddr = dmastation.station_id

        dmaflow = 0
        month_sale = 0
        lastmonth_sale = 0
        bili = 0
        today = datetime.date.today()
        today_str = today.strftime("%Y-%m-%d")
        today_flow = HdbFlowDataDay.objects.filter(commaddr=commaddr).filter(hdate=today_str)
        if today_flow.exists():
            dmaflow = today_flow.first().dosage

        month_str = today.strftime("%Y-%m")
        month_flow = HdbFlowDataMonth.objects.filter(commaddr=commaddr).filter(hdate=month_str)
        if month_flow.exists():
            month_sale = month_flow.first().dosage

        lastmonth = datetime.datetime(year=today.year,month=today.month-1,day=1)
        lastmonth_str = lastmonth.strftime("%Y-%m")
        lastmonth_flow = HdbFlowDataMonth.objects.filter(commaddr=commaddr).filter(hdate=lastmonth_str)
        if lastmonth_flow.exists():
            lastmonth_sale = lastmonth_flow.first().dosage

        if float(month_sale) > 0 and float(lastmonth_sale) > 0:
            bili =  (float(month_sale) - float(lastmonth_sale) ) / float(lastmonth_sale)

        data.append(
            {
                "dma_name":dma.dma_name,
                "belongto":dma.belongto.name,
                "dma_level":"二级",
                "dma_status":"在线",
                "dmaflow":round(float(dmaflow),2),
                "month_sale":round(float(month_sale),2),
                "lastmonth_sale":round(float(lastmonth_sale),2),
                "bili":round(bili,2)
            }
        )

    return data

        
class MapMonitorView(LoginRequiredMixin,TemplateView):
    template_name = "monitor/mapmonitor.html"

    def get_context_data(self, *args, **kwargs):
        context = super(MapMonitorView, self).get_context_data(*args, **kwargs)
        context["page_menu"] = "数据监控"
        # context["page_submenu"] = "组织和用户管理"
        context["page_title"] = "地图监控"

        stat_list = dmastasticinfo()
        statsinfo = json.dumps({"statsinfo":stat_list})
        
        context["dmastasticinfo"] = statsinfo

        

        return context          


class MapMonitorView2(LoginRequiredMixin,TemplateView):
    template_name = "monitor/mapmonitor2.html"

    def get_context_data(self, *args, **kwargs):
        context = super(MapMonitorView2, self).get_context_data(*args, **kwargs)
        context["page_menu"] = "数据监控"
        # context["page_submenu"] = "组织和用户管理"
        context["page_title"] = "地图监控"

        stat_list = dmastasticinfo()
        statsinfo = json.dumps({"statsinfo":stat_list})
        
        context["dmastasticinfo"] = statsinfo
        

        return context          



class MapStationView(LoginRequiredMixin,TemplateView):
    template_name = "monitor/mapstation.html"

    def get_context_data(self, *args, **kwargs):
        context = super(MapStationView, self).get_context_data(*args, **kwargs)
        context["page_menu"] = "数据监控"
        # context["page_submenu"] = "组织和用户管理"
        context["page_title"] = "站点监控"

        stat_list = dmastasticinfo()
        statsinfo = json.dumps({"statsinfo":stat_list})
        
        context["dmastasticinfo"] = statsinfo

        

        return context          


class RealTimeDataView(LoginRequiredMixin,TemplateView):
    template_name = "monitor/realtimedata.html"

    def get_context_data(self, *args, **kwargs):
        context = super(RealTimeDataView, self).get_context_data(*args, **kwargs)
        context["page_menu"] = "数据监控"
        # context["page_submenu"] = "组织和用户管理"
        context["page_title"] = "实时数据"

        stations = self.request.user.station_list_queryset('')

        total_station_num = stations.count()
        online_station = stations.filter(meter__state=1)
        online_station_num = online_station.count()
        biguser_station = stations.filter(biguser=1)
        biguser_station_num = biguser_station.count()
        focus_station = stations.filter(focus=1)
        focus_station_num = focus_station.count()

        alarm_station_num = 0

        context["total_station_num"] = total_station_num
        context["online_station_num"] = online_station_num
        context["offline_station_num"] = total_station_num - online_station_num
        context["biguser_station_num"] = biguser_station_num
        context["focus_station_num"] = focus_station_num
        context["alarm_station_num"] = alarm_station_num

        return context          

# 返回实时数据页面站点列表
def stationlist(request):
    
    draw = 1
    length = 0
    start=0
    
    if request.method == "GET":
        draw = int(request.GET.get("draw", 1))
        length = int(request.GET.get("length", 10))
        start = int(request.GET.get("start", 0))
        search_value = request.GET.get("search[value]", None)
        # order_column = request.GET.get("order[0][column]", None)[0]
        # order = request.GET.get("order[0][dir]", None)[0]
        groupName = request.GET.get("groupName")
        simpleQueryParam = request.POST.get("simpleQueryParam")
        # print("simpleQueryParam",simpleQueryParam)

    if request.method == "POST":
        draw = int(request.POST.get("draw", 1))
        length = int(request.POST.get("length", 10))
        start = int(request.POST.get("start", 0))
        pageSize = int(request.POST.get("pageSize", 10))
        search_value = request.POST.get("search[value]", None)
        order_column = int(request.POST.get("order[0][column]", None))
        order = request.POST.get("order[0][dir]", None)
        groupName = request.POST.get("groupName")
        districtId = request.POST.get("districtId")
        simpleQueryParam = request.POST.get("simpleQueryParam")
        # print(request.POST.get("draw"))
        # print("groupName",groupName)
        # print("districtId:",districtId)
        # print("post simpleQueryParam",simpleQueryParam)
    
    
    user = request.user
    organs = user.belongto

    stations = user.station_list_queryset(simpleQueryParam) 
    
    if groupName != "":
        stations = stations.filter(belongto__uuid=groupName)
    
    # 一次获取全部所需数据，减少读取数据库耗时
    stations_value_list = stations.values_list('meter__simid__simcardNumber','username','belongto__name','meter__serialnumber','meter__dn')
    
    bgms = Bigmeter.objects.all().order_by('-fluxreadtime').values_list('commaddr','commstate','fluxreadtime','pickperiod','reportperiod',
        'flux','plustotalflux','reversetotalflux','pressure','meterv','gprsv','signlen')
    
    alams_sets = Alarm.objects.values('commaddr').annotate(Count('id'))
    alarm_dict = {}
    for alm in alams_sets:
        alarm_dict[alm['commaddr']] = alm['id__count']
    
    

    # 用户权限拥有的站点通讯识别号
    commaddrs = [s[0] for s in stations_value_list ]
    # print("commaddrs",commaddrs)
    tmp_bgms = [b for b in bgms if b[0] in commaddrs]
    # print("tmp_bgms",tmp_bgms)
    # print("stations",stations)
    
    def bgm_data(b):
        # query station from bigmeter commaddrss
        commaddr = b[0]
        alarm_count = alarm_dict[commaddr]

        # print('alarm_count',alarm_count,commaddr)
        s=None
        for s0 in stations_value_list:
            if s0[0] == commaddr:
                s=s0
        # try:
        #     s =  stations.select_related("meter__simid").select_related("belongto").get(meter__simid__simcardNumber=commaddr)   #meter__simid__simcardNumber
        # except :
        #     s = None
        if s:
        
            return {
                "stationname":s[1],
                "belongto":s[2],
                "serialnumber":s[3],#
                "alarm":alarm_count,
                "status":b[1],
                "dn":s[4],
                "readtime":b[2] ,
                "collectperiod":b[3],
                "updataperiod":b[4],
                "influx":round(float(b[5]),2) if b[5] else '',
                "plusflux":round(float(b[6]),2)  if b[6] else '',
                "revertflux":round(float(b[7]),2) if b[7] else '',
                "press":round(float(b[8]),2) if b[8] else '',
                "baseelectricity":round(float(b[9]),2) if b[9] else '',
                "remoteelectricity":round(float(b[10]),2) if b[10] else '',
                "signal":round(float(b[11]),2) if b[11] else '',
                
            }
        else:
            return None
    data = []
    
    
    for b in tmp_bgms[start:start+length]:  #[start:start+length]
        
        ret=bgm_data(b)
        
        if ret is not None:
            data.append(ret)
    
    
    recordsTotal = stations.count()
    # recordsTotal = bgms.count()
    
    result = dict()
    result["records"] = data
    result["draw"] = draw
    result["success"] = "true"
    result["pageSize"] = pageSize
    result["totalPages"] = recordsTotal/pageSize
    result["recordsTotal"] = recordsTotal
    result["recordsFiltered"] = recordsTotal
    result["start"] = 0
    result["end"] = 0

    # print(draw,pageSize,recordsTotal/pageSize,recordsTotal)
    
    return HttpResponse(json.dumps(result))





class RealcurlvView(LoginRequiredMixin,TemplateView):
    template_name = "monitor/realcurlv.html"

    def get_context_data(self, *args, **kwargs):
        context = super(RealcurlvView, self).get_context_data(*args, **kwargs)
        context["page_title"] = "实时曲线"
        context["page_menu"] = "数据监控"
        
        return context  




class VehicleView(LoginRequiredMixin,TemplateView):
    template_name = "monitor/vehicle.html"

    def get_context_data(self, *args, **kwargs):
        context = super(VehicleView, self).get_context_data(*args, **kwargs)
        context["page_title"] = "车辆监控"
        context["page_menu"] = "数据监控"
        
        return context  

 

class VedioView(LoginRequiredMixin,TemplateView):
    template_name = "monitor/vedio.html"

    def get_context_data(self, *args, **kwargs):
        context = super(VedioView, self).get_context_data(*args, **kwargs)
        context["page_title"] = "实时视频"
        context["page_menu"] = "数据监控"
        
        return context  

 

class SecondwaterView(LoginRequiredMixin,TemplateView):
    template_name = "monitor/secondwater.html"

    def get_context_data(self, *args, **kwargs):
        context = super(SecondwaterView, self).get_context_data(*args, **kwargs)
        context["page_title"] = "二次供水"
        context["page_menu"] = "数据监控"
        
        return context  

 


