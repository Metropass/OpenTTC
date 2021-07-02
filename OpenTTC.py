import py_nextbus
import pandas as pd

class OpenTTC:
    client = py_nextbus.NextBusClient(output_format = 'json')

    def __init__(self, route=None, stop=None):
        self.__route = route
        self.__stop = stop

    def set_route(self, route_num):
        self.__route = route_num

    def set_stop(self, stop_num):
        self.__stop = stop_num

    def get_routes(self):
        try:
            q = client.get_route_list(agency='ttc')
            print(q)
            return q
        except RuntimeError:
            print("It seems like there's been an error: " )

    def get_route_information(self):
        try:
            if(self.__route is None):
                raise RuntimeError("You haven't set your default Route on the TTC!  \n Call set_route() with your desired route.")
            q = client.get_route_config(route_tag=self.__route, agency='ttc')
            print(q)
            return q
        except RuntimeError:
            print("It seems like there's been an error: " )

    def get_predict(self):
        try:
            if(self.__route is None):
                raise RuntimeError("You haven't set your default Route on the TTC!  \n Call set_route() with your desired route.")
            if(self.__stop is None):
                raise RuntimeError("You haven't set your default stop on the TTC!  \n Call set_stop() with youor desired stopID.")
            q = client.get_predictions(stop_tag=self.__stop, route_tag=self.__route, agency='ttc')
        except RuntimeError:
            print("It seems like there's been an error: " )
