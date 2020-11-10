from AirthingsAccount import AirthingsAccount
from AirthingsCloud import AirthingsCloud
from datetime import datetime, timedelta
import logging
import logging.config
import pandas as pd
import os


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, filename='AirthingsCloud.log', filemode='a', format='"%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    OUTPUT_FOLDER = "csv_files"

    ### Credentials
    ## Find API Client info: https://dashboard.airthings.com/integrations/api-integration
    CLIENT_ID = ""
    CLIENT_SECRET = ""

    #Step 1: Create an API connection and fresh access_token
    account = AirthingsAccount(CLIENT_ID, CLIENT_SECRET)
    #Step 2: Instantiate a Cloud connection
    cloudConnection = AirthingsCloud(account)
    #Step 3: Get latest data for all devices

    ## Specify the time period
    START_TIME = "2020-01-22T23:03:49.735Z"
    END_TIME ="2020-10-29T23:03:49.735Z"

    ## Will only include devices from this location name
    location_to_include = "Preståsen skole"

    ## Create an output folder if not existing
    if not os.path.exists(OUTPUT_FOLDER):
            os.makedirs(OUTPUT_FOLDER)

    # Get device info and device names
    devices = cloudConnection.getDevices()
    #Look through all devices and create CSV files
    for device in devices:
        if device['location']['name'] != location_to_include:
            #Skipping - device not at location we are interested in
            continue
        
        if device['deviceType'] == "HUB":
            #We only want to include Wave Plus devices 
            continue
        
        #Get info about the device
        device_id = device['id']
        device_name = device['segment']['name']

        #Get Device sample data and store in CSV
        df = cloudConnection.getDeviceSamples(device_id, START_TIME, END_TIME)

        if df.empty:
            #No data for device, we skip it
            continue
        
        df['time'] = pd.to_datetime(df['time'], unit='s')
        
        # We set the sensor data order based on the device type
        if device['deviceType'] == "WAVE_PLUS":
            df = df[['time', 'co2', 'humidity', 'light', 'pressure', 'radonShortTermAvg', 'temp','voc']]
        if device['deviceType'] == "WAVE_MINI":
            df = df[['time', 'humidity', 'light', 'pressure', 'temp','voc']]

        df.to_csv(OUTPUT_FOLDER + "/" + str(device_id) +"-"+ device_name + ".csv", index=False)