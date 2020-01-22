import xml.etree.ElementTree as ET
import datetime as times
import os
from urllib3 import request as url
import copy
import js2py as js


def elements_bool(tree1, tree2):
    if tree1.tag != tree2.tag: return False
    if tree1.text != tree2.text: return False
    if tree1.tail != tree2.tail: return False
    if tree1.attrib != tree2.attrib: return False
    if len(tree1) != len(tree2): return False
    return all(elements_bool(recur1, recur2) for recur1, recurc2 in zip(tree1, tree2))




class TTC:
    def __init__(self, routeNum = None):
        self.routeNum = routeNum
        self.routeName = routeName
        self.routeNameShort = routeNameShort
        self.routeStopName = None
        self.stopID = None
        self.tree = None
        self.routeTag = None
        self.colour = colour
        self.latMin = None
        self.latMax = None
        self.lonMin = None
        self.lonMax = None
        self.stopLat = None
        self.stopLon = None
        self.epoch_time = None
        self.is_departure = None
        self.time_seconds = None
        self.time_minutes = None
        self.dir_tag = None
        self.vehicle = None
        self.multiple_stops = []
        file = url.urlopen('http://webservices.nextbus.com/service/publicXMLFeed?command=routeConfig&a=ttc&r={0}'.format(routeNum))
        data = file.read()
        file.close()
        self.tree = ET.fromstring(data)
        self.routeName = self.tree[0].get('title')
        self.colour = self.tree[0].get('color')
        self.latMin =  self.tree[0].get('latMin')
        self.latMax = self.tree[0].get('latMax')
        self.lonMin = self.tree[0].get('lonMin')
        self.lonMax = self.tree[0].get('lonMax')
        self.routeNameShort = self.routeName[(self.routeName.find('-') + 1):]


        # need custom <> and or cmp() operators within ElementTree, for optimization
        def redefineByTag(self, tag_arg = None):
            tag_found = False
            if(self.tree is None):
                file = url.urlopen('http://webservices.nextbus.com/service/publicXMLFeed?command=routeConfig&a=ttc&r={0}'.format(routeNum))
                data = file.read()
                file.close()
                self.tree = ET.fromstring(data)
            for tag_itr in tree.iter('stop'):
                tag_found = True
                if(tag_arg == tree[tag_itr].get('tag')):
                    self.routeTag = tree[tag_itr].get('tag')
                    self.title = tree[tag_itr].get('title')
                    self.stopID = tree[tag_itr].get('stopId')
                    self.stopLat = tree[tag_itr].get('lat')
                    self.stopLon = tree[tag_itr].get('lon')



            #tree[0] = direction xml
            #tree[0][0] = prediction child
        def grabByStopID(self, stop_arg, single_route = None, future = None):
            if(self.stopID is None):
                if(stop_arg.isnumeric() or stop_arg is None):
                    return "Error! The argument isn't a valid StopID!"
            file = url.urlopen('http://webservices.nextbus.com/service/publicXMLFeed?command=predictions&a=ttc&stopId={0}&routeTag={1}'.format(stop_arg,routeNum))
            data = file.read()
            file.close()
            self.tree = ET.fromstring(data)
            if(single_route is True):
                self.stopID = stop_arg
                if(future is True):
                    past = copy.deepcopy(self)
                file = url.urlopen('http://webservices.nextbus.com/service/publicXMLFeed?command=predictions&a=ttc&stopId={0}&routeTag={1}'.format(stop_arg,routeNum))
                data = file.read()
                file.close()
                self.tree = ET.fromstring(data)
                self.tree = self.tree.find('predictions')
                self.epoch_time = int(self.tree[0][0].get('epochTime'))
                self.is_departure = self.tree[0][0].get('isDeparture')
                self.time_seconds = self.tree[0][0].get('seconds')
                self.time_minutes = self.tree[0][0].get('minutes')
                self.dir_tag = self.tree[0][0].get('dirTag')
                self.vehicle = self.tree[0][0].get('vehicle')
                if (past in locals()):
                    return past

            else:
                stop_counter = 0
                bool_trees = False
                while bool_trees is False:
                    try:
                        self.multiple_stops.append(self.tree[stop_counter])
                        stop_counter = stop_counter + 1
                    except:
                        print("List appended")
                        bool_trees = True



        def convert_epoch(self):
            times = self.epoch_time/1000
            t = datetime.datetime.fromtimestamp(times).strftime('%H:%M:%S')
            return t

        def getTree(self):
            return self.tree

        def getRouteName(self):
            return self.routeName


        def __gt__(self, other):
            if(self.epoch_time > other.epoch_time):
                return True
            else:
                return False


        def __lt__(self, other):
            if(self.epoch_time < other.epoch_time):
                return True
            else:
                return False

        #Equates 2 trees within TTC
        def __eq__(self, other):
            return elements_bool(self.tree, other.tree)


        def __ne__(self, other):
            return not elements_bool(self.tree, other.tree)

        def __copy__(self):
            return TTC(self.routeNum)

        def __round__(self):
            return self.convert_epoch()

        def __len__(self):
            return size(self.tree)

class TTC_Subway:
    def __init__(self, subway_station = None, direction = None):
        self.subway_station = subway_station
        self.peak_indicator = None
        self.subway_direction = direction
        self.interval = None
        self.time = times.now()
        self.service_alert = []



    def set_station(self, sub):
        self.subway_station = sub

    def set_direction(self, dir):
        self.subway_direction = dir

# EarEve = Early Evening, LteEve = Late Evening, A = Afternoon Peak, M = Morning Peak, Mid = Midday Service
    def get_peak(self):
        self.time = times.now()
        if(times.time.hour >= 6 and times.time.hour < 9):
            self.peak_indicator = "M"
        else if(times.time.hour >= 9 and times.time.hour < 15):
            self.peak_indicator = "Mid"
        else if(times.time.hour >= 15 and times.time.hour < 19):
            self.peak_indicator = "A"
        else if(times.time.hour >= 19 and times.time.hour < 22):
            self.peak_indicator = "EarEve"
        else if(times.time.hour >= 22 or (times.time.hour < 1)):
            self.peak_indicator = "LteEve"
        else:
            self.peak_indicator = "O"

    def get_service_alerts(self):
        init_web = url.urlopen(http://ttc.ca/Service_Advisories/all_service_alerts.jsp).read()
       
