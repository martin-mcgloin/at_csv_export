import requests
import json
from datetime import datetime, timedelta
import time
import logging
import logging.config

class AirthingsAccount:
    base_url = "https://accounts-api.airthings.com/v1"
    token_path = "/token"
    access_token = ""
    refresh_token = ""

    #Uses the machine-to-machine API Client
    def __init__(self, client_id, client_secret):
        self.logger = logging.getLogger(__name__)
        self.refresh_token = ""
        self.access_token = ""
        self.client_id = client_id
        self.client_secrete = client_secret
        self.updateAccessToken()

    def updateAccessToken(self):
        url = self.base_url + self.token_path
        self.logger.info("Getting a fresh access_token")
        body = {
            "grant_type":"client_credentials",
            "client_id":self.client_id,
            "client_secret":self.client_secrete,
        }
        r = requests.post(url, data=body)
        if (r.status_code != 200):
            self.logger.error("Request to AirthingsCloud failed. Status code: " + str(r.status_code) + ", and response: " + r.text)
        else:
            self.access_token = r.json()["access_token"]

    def getAccessToken(self):
        if self.access_token:
            self.logger.info("We have an existing access_token to use for connection")
            return self.access_token
        else:
            self.logger.error("No access_token, getting a fresh with refresh_token")
            self.updateAccessToken()
    