# -*- coding: utf-8 -*-
print ("module [backend.api_sensor] loaded")

from backend import manager
from backend.api_common import *
from backend_model.table_sensor import *
from sqlalchemy import or_, and_,sql
import requests
import re
import os
from datetime import datetime
db = DBManager.db
import json
from time import sleep
import uuid
import sys
import pandas as pd
import csv
from sqlalchemy import or_, and_, func
from datetime import datetime, timedelta

import openpyxl
from openpyxl.styles.borders import Border, Side
from openpyxl.styles import Alignment
import random
api_headers = {'Content-type': 'application/json'}


manager.create_api(SensorFiles
                   , results_per_page=10000
                   , url_prefix='/api/v1'
                   , collection_name='sensorfiles'
                   , methods=['GET', 'DELETE', 'PATCH', 'POST']
                   , allow_patch_many=True
                   , preprocessors={
                        'POST': [check_token],
                        'PATCH_SINGLE': [check_token_single],
                        'GET_SINGLE': [check_token_single],
                   })

manager.create_api(SensorData
                   , results_per_page=10000
                   , url_prefix='/api/v1'
                   , collection_name='sensordata'
                   , methods=['GET', 'DELETE', 'PATCH', 'POST']
                   , allow_patch_many=True
                   , preprocessors={
                        'POST': [check_token],
                        'PATCH_SINGLE': [check_token_single],
                        'GET_SINGLE': [check_token_single],
                   })

@app.route('/api/v1/upload_file', methods=['POST'])
def upload_file_api():
    print("1")
    check_token()
    print("2")
    print(request.files)
    if 'file' not in request.files:
        return make_response(jsonify({'result': False}), 400)

    f = request.files['file']
    if f.filename == '':
        return make_response(jsonify({'result': False}), 400)

    upload_path = os.getcwd() + '/uploads/'

    if f and '.' in f.filename:
        filename = f.filename
        f.save(os.path.join(upload_path, filename))
        return make_response(jsonify({'result': True, 'filename': filename,'src_filename':f.filename}), 200)


@app.route('/api/v1/upload_file/<filename>', methods=['GET'])
def get_upload_fil_api(filename):
    upload_path = os.getcwd() + '/uploads/'
    return send_from_directory(upload_path, filename)

@app.route('/api/v1/download/<filename>', methods=['GET'])
def get_download_excel(filename):
    upload_path = os.getcwd() + '/download/'
    return send_from_directory(upload_path, filename)

global download_index
download_index = 0
@app.route('/api/v1/csv_download', methods=['get'])
def csv_download_api():
    print("csv_download start...")
    parser = reqparse.RequestParser()
    parser.add_argument("id", type=str, location='args', required=True)
    parser.add_argument("file_names", type=str, location='args', required=True)
    parser.add_argument("sensor_type", type=str, location='args', required=True)

    args = parser.parse_args()
    id = int(args['id'])
    file_names = args['file_names']
    sensor_type = args['sensor_type']
    make_file_name = './download/{0}'.format(file_names)
    if os.path.isfile(make_file_name):
      os.remove(make_file_name)
    with open(make_file_name, 'wt') as f:
        if sensor_type == "INJECTION":
            data_list = SensorData.query.filter_by(fk_sensor_file_id=int(id)).all()
            print("len : ",len(data_list))
            line = "CycleCount,TempZone1,TempZone2,TempZone3,TempZone4,TempZone5,CycleTime,InjectTime,Cushion(mm),Cushion(cm3),InjectPress,Alarms"
            print("line :",line)
            f.write(line + '\n')
            for data in data_list:
                msg = json.loads(data.data_msg)
                f.write(msg['msg'] + '\n')
        elif sensor_type == "CNCOSCI":
            sensor_data = SensorData.query.filter_by(fk_sensor_file_id=int(id)).first()
            if sensor_data is not None :
                msg = json.loads(sensor_data.data_msg)
                for data in msg['msg']:
                    f.write(data + '\n')
        elif sensor_type == "POWER":
            sensor_data = SensorData.query.filter_by(fk_sensor_file_id=int(id)).first()
            line = "date_time,watt"
            print("line :",line)
            f.write(line + '\n')
            if sensor_data is not None :
                msg = json.loads(sensor_data.data_msg)
                for data in msg:
                    line = data["date_time"] + "," + str(data['w'])
                    f.write(line + '\n')
    res = {
        "filename":file_names
    }
    return make_response(jsonify(res), 200)

@app.route('/api/v1/gen_injection_dat', methods=['GET'])
def gen_injection_dat_api():
    for d in range(1,11):
        file_name = './/data//injectiondata//212201{0}1500.csv'.format(str(d).zfill(2))
        with open(file_name, 'wt') as f:
            line = "CycleCount,TempZone1,TempZone2,TempZone3,TempZone4,TempZone5,CycleTime,InjectTime,Cushion(mm),Cushion(cm3),InjectPress,Alarms"
            print("line :",line)
            f.write(line + '\n')
            for i in range(0,100):
                CycleCount = str(i + 1).zfill(9)
                TempZone1 = round(random.uniform(150.0,200.0),1)
                TempZone2 = round(random.uniform(150.0,200.0),1)
                TempZone3 = round(random.uniform(150.0,200.0),1)
                TempZone4 = round(random.uniform(500.0,550.0),1)
                TempZone5 = round(random.uniform(500.0,550.0),1)
                CycleTime = round(random.uniform(10.0,15.0),1)
                InjectTime = round(float(i)  + 0.01,1)
                Cushion_mm = round(random.uniform(0.0,15.0),1)
                Cushion_cm = round(random.uniform(0.0,15.0),1)
                InjectPress = round(random.uniform(80.0,90.0),1)
                Alarms = "x"
                line = CycleCount + \
                "," + str(TempZone1) + \
                "," + str(TempZone2) + \
                "," + str(TempZone3) + \
                "," + str(TempZone4) + \
                "," + str(TempZone5) + \
                "," + str(CycleTime) + \
                "," + str(InjectTime) + \
                "," + str(Cushion_mm) + \
                "," + str(Cushion_cm) + \
                "," + str(InjectPress) + \
                ",x"
                f.write(line + '\n')
    return make_response(jsonify({}), 200)