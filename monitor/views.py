# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import get_object_or_404,render,redirect
from django.http import HttpResponse,JsonResponse,HttpResponseRedirect
from django.contrib import messages

import json
import random
import datetime

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

from accounts.models import User,MyRoles

from legacy.models import HdbFlowDataDay,HdbFlowDataMonth

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

        lastmonth = datetime.datetime(year=today.year,month=today.month-1,day=today.day)
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

        
class MapMonitorView(TemplateView):
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


class MapMonitorView2(TemplateView):
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
