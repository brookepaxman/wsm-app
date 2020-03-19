import numpy as np
import sys, traceback
from django.db import models
from django.utils import timezone

CONST_INT = 40 #seconds per recording of one data object

def avg(data):
    sum = 0
    datasize = len(data)
    for datapt in data:
        sum += datapt
    avg = sum/datasize
    return avg

def hr_dip(hr_data):
    min = 10000
    sleep_index = 600/CONST_INT
    awake_reference = hr_data[sleep_index] #10 minutes after user turns on monitor, this can maybe change
    while sleep_index < len(hr_data):
        if hr_data[sleep_index] < min:
            min = hr_data[sleep_index]
        sleep_index += 1
    hr_dip = np.absolute(awake_reference - min)
    return hr_dip

def hr_min_max(hr_data):
    min = 10000
    max = 0
    sleep_index = 600/CONST_INT #10 minutes into monitor time
    while sleep_index < len(hr_data):
        if hr_data[sleep_index] < min:
            min = hr_data[sleep_index]
        if hr_data[sleep_index] > max:
            max = hr_data[sleep_index]
        sleep_index += 1
    return min, max

def gradients(data):
    dx = CONST_INT
    gradients = np.diff(data)/dx
    return gradients

def main():
    #### need list of model STAT per user from db here somehow ####
    Stats = []
    hr_data = []
    rr_data = []
    try:
        for Stat in Stats:
            hr_data.append(Stat.hr)
            rr_data.append(Stat.rr)
        avg_hr = avg(hr_data)
        avg_rr = avg(rr_data)
        user_hr_dip = hr_dip(hr_data)
        hr_min, hr_max = hr_min_max(hr_data)
        print("User analytics calculated succesfully")
    except:
        traceback.print_exc(file=sys.stdout)

    ####need a way to write these values to each user's page in specific db ####

if __name__ == "__main__":
    main()
