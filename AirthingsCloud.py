from AirthingsAccount import AirthingsAccount
import requests
import json
from datetime import datetime, timedelta
import time
import logging
import logging.config

class AirthingsCloud:
    base_url = "https://ext-api.airthings.com/v1"
    segments_path = "/segments"
    threshold_breaches_path = "/devices/{serialNumber}/threshold-breaches"

    def __init__(self, AirthingsAccount):
        self.logger = logging.getLogger(__name__)
        self.AirthingsAccount = AirthingsAccount
        pass

    def _sendRequest(self, path, body=None, params=None):
        url = self.base_url + path
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36', 
            'Authorization' : self.AirthingsAccount.getAccessToken()
        }
        r = requests.get(url, headers=headers, params=params)
        if r.status_code == 401:
            self.logger.error("Invalid access_code. Status code: " + str(r.status_code) + ", and response: " + r.text)            
            self.AirthingsAccount.updateAccessToken()
            headers["Authorization"] = self.AirthingsAccount.getAccessToken()
            r = requests.get(url, headers=headers)
        if r.status_code != 200:
            self.logger.error("Request to AirthingsCloud failed. Status code: " + str(r.status_code) + ", and response: " + r.text)            
            return
        return r.json()

    def getSegmentForDevice(self, sn):
        response = self._sendRequest(self.segments_path)
        if response:
            data = response["segments"]
            self.logger.info("Got data for device " + str(sn))
            for segment in data:
                print(segment)
                if int(segment["deviceId"]) == int(sn):
                    return {'id': segment["id"], 'name' : segment["name"]}

    def getDevices(self):
        path =  "/devices"
        self.logger.info("Getting devices for current account")       
        response = self._sendRequest(path)
        if response:
            data = response['devices']
            return data


    def getDeviceSamples(self, sn, start=None, end=None):
        path =  "/devices/" + str(sn)+ "/samples"
        params = {
            "start": start,
            "end": end,
        }
        self.logger.info("Getting latest samples for " + str(sn))       
        response = self._sendRequest(path, params=params)
    
        if response:
            data = response['data']
            return data