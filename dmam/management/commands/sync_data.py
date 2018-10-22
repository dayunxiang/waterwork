from django.core.management.base import BaseCommand, CommandError


from legacy.models import (HdbFlowData,HdbFlowDataDay,HdbFlowDataHour,HdbFlowDataMonth,HdbPressureData,Bigmeter,
    Watermeter,HdbWatermeterDay,HdbWatermeterMonth,Concentrator,Community,
    HdbFlowDataMonth)

import time
import datetime
import logging
import string

from dmam.models import VConcentrator,VWatermeter,VCommunity,Station,Meter,SimCard,DMABaseinfo,DmaStation
from entm.models import Organizations

logger_info = logging.getLogger('info_logger')


def random_string_generator(size=10, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

class Command(BaseCommand):
    help = 'import data from A to B'

    def add_arguments(self, parser):
        # parser.add_argument('sTime', type=str)

        

        parser.add_argument(
            '--dmastation',
            action='store_true',
            dest='dmastation',
            default=False,
            help='import dmastation to new db'
        )


        parser.add_argument(
            '--station-bigmeter',
            action='store_true',
            dest='station-bigmeter',
            default=False,
            help='import station-bigmeter to new db'
        )

        parser.add_argument(
            '--listname',
            action='store_true',
            dest='listname',
            default=False,
            help='import listname to new db'
        )


    def handle(self, *args, **options):
        # sTime = options['sTime']
        t1=time.time()
        count = 0
        aft = 0
        

        if options['station-bigmeter']:
            
            organ = Organizations.objects.get(name="歙县自来水公司")
            # data_qset=HdbFlowData.objects.using("virvo").filter(readtime__range=[sTime,'2018-09-20'])
            data_qset=Bigmeter.objects.using("zncb").values_list('commaddr','commstate','meterstate','gprsv','meterv',
                'signlen','lastonlinetime','pressure','plustotalflux','reversetotalflux','flux','totalflux','pressurereadtime',
                'fluxreadtime','username')
            
            for d in data_qset:
                commaddr = d[0]
                username = d[14]

                # query station find if commaddr exist
                stations=Station.objects.filter(username=username)
                if not stations.exists():
                    print(" {} {} not in station list".format(username,commaddr))

                    # check if commaddr exist in meter
                    meters=Meter.objects.filter(simid__simcardNumber=commaddr)
                    if not meters.exists():
                        print(" {} {} not in meters list".format(username,commaddr))
                        
                        # check if commaddr exist in simcards
                        simcards = SimCard.objects.filter(simcardNumber=commaddr)
                        if not simcards.exists():
                            print(" {} {} not in simcards list".format(username,commaddr))
                            count += 1
                            sd = SimCard.objects.create(simcardNumber=commaddr,belongto=organ)
                        else:
                            sd =SimCard.objects.get(simcardNumber=commaddr)
                        
                        m = Meter.objects.create(serialnumber=commaddr,simid=sd,belongto=organ)

                    else:
                        m = Meter.objects.get(simid__simcardNumber=commaddr)

                    # and then add to Station
                    try:
                        s = Station.objects.create(username=username,belongto=organ,meter=m)
                    except:
                        print("-------------{} {} may duplication".format(username,commaddr))

        if options['listname']                :
            organ = Organizations.objects.get(name="歙县自来水公司")
            # data_qset=HdbFlowData.objects.using("virvo").filter(readtime__range=[sTime,'2018-09-20'])
            data_qset=Bigmeter.objects.using("zncb").values_list('commaddr','commstate','meterstate','gprsv','meterv',
                'signlen','lastonlinetime','pressure','plustotalflux','reversetotalflux','flux','totalflux','pressurereadtime',
                'fluxreadtime','username')
            
            for d in data_qset:
                commaddr = d[0]
                username = d[14]

                sb = Station.objects.filter(meter__simid__simcardNumber=commaddr)
                s=sb.first()
                if sb. count() > 1:
                    print("----------multiple station {} {}".format(sb.count(),commaddr),sb)
                # if s.username != username:
                #     print("{} {}".format(s.username,username))
                
                    

        

        if options['dmastation']:
            
            dmabs = DMABaseinfo.objects.all()
            for d in dmabs:
                print(d.dma_name)
                stations = d.station_set.all()
                # print(stations.count(),stations)
                for s in stations:
                    station_id = s.meter.simid.simcardNumber
                    meter_type = s.dmametertype
                    station_type = 1
                    print(d.dma_name,station_id,meter_type,station_type)
                    DmaStation.objects.create(dmaid=d,station_id=station_id,meter_type=meter_type,station_type=station_type)
                    

        
                    
                
        
        # print('cnt=',cnt,cnt2)
        t2 = time.time() - t1
        self.stdout.write(self.style.SUCCESS(f'total {count}  Affected {aft} row(s)!,elapsed {t2}'))
