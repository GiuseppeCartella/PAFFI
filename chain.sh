#!/usr/bin/env bash
#esempio naive connection
python3 subsample.py -l POI_sensors.txt POI_fog.txt POI_cloud.txt
python3 set_links.py -l sensors_fog fog_fog fog_cloud
python3 createScenario.py
python3 connect.py



