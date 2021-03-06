#!/usr/bin/python
import requests
import ConfigParser
import time
import os
import sys
from os.path import expanduser

config = ConfigParser.SafeConfigParser()
params = {}
now = int(round(time.time()))
log_dir = expanduser('/var/log/cloudflare_logs/')
local_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
config_file = os.path.join(local_dir, "config.properties")
config.read(config_file)
zones = config.get("Zones", "key")
timenow = time.strftime("%m%d%Y-%H")

def load_config():
    if not os.path.isdir(log_dir):
        os.makedirs(log_dir)
    if os.path.exists(config_file):
        config.readfp(open(config_file))
    else:
        sys.exit('config.properties does not exist!')

def get_params():
    params['authEmail'] = config.get("Config", "auth-email")
    params['authKey'] = config.get("Config", "auth-key")
    params['startTime'] = config.get("Config", "start-time")
    params['endTime'] = config.get("Config", "end-time")
    params['fields'] = config.get("Config", "fields")
    if len(str(params["startTime"])) == 0:
        params['startTime'] = str(now - 900)
        params['startTime'] = params['startTime'][:-1] + '0'
    if len(str(params["endTime"])) == 0:
        params['endTime'] = str(now - 840)
        params['endTime'] = params['endTime'][:-1] + '0'

def make_request():
    headers = {"x-Auth-Key": params['authKey'], "x-Auth-Email": params['authEmail']}
    for zone in zones.split(","):
        url = "https://api.cloudflare.com/client/v4/zones/" + zone + "/logs/received?" \
            + "start=" + params['startTime'] + "&end=" + params['endTime'] + "&fields=" + params['fields']
        req = requests.get(url, headers=headers)
    return req

def print_stats():
    req = make_request()
    output_file = open(log_dir + 'cloudflare.log-' + timenow ,'a')
    output_file.write(req.content)
    output_file.close()

def set_time():
    start = str(now - 960)
    start = start[:-1] + '0'
    end = str(now - 900)
    end = end[:-1] + '0'
    configFile = open(config_file, 'wb')
    config.set("Config", "start-time", start)
    config.set("Config", "end-time", end)
    config.write(configFile)
    configFile.close()

def start():
    load_config()
    get_params()
    make_request()
    print_stats()
    set_time()

if __name__ == '__main__':
    start()
