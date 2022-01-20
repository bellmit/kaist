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

def post_get_many_source(result=None, **kw):
    check_token()

    src_list = result['objects']

    for src in src_list:
        if src['invention_title'] is not None:
            src['invention_title'] = src['invention_title'][:100] + "..."

        if src['summary_of_invention'] is not None:
            src['summary_of_invention'] = src['summary_of_invention'][:300] + "..."

        if src['description_of_embodiments'] is not None:
            src['description_of_embodiments'] = src['description_of_embodiments'][:1000] + "..."

def post_get_many_train_result(result=None, **kw):
    check_token()
    src_list = result['objects']



@app.route('/api/v1/sensor_data_upload', methods=['POST'])
def sensor_data_upload():
    print("sensor_data_upload")
    result = {
        "ACK":"SUCCESS",
        "MSG":""
    }
    try :
        parser = reqparse.RequestParser()
        parser.add_argument("sender_ip", type=str, location="json")
        parser.add_argument("company_id", type=str, location="json")
        parser.add_argument("sensors_msg", type=str, location="json")
        input = parser.parse_args()
        print("input : ", input)
        #client = MongoClient('localhost', 27017)
        #db = client['itrc_spark']
        #collection = db.col_sensor
        obj = {
            "sender_ip": input['sender_ip'],
            "company_id": input['company_id'],
            "sensors_msg": json.dumps(input['sensors_msg']),
        }

        new_msg = TB_SENSOR_UPLOAD()
        new_msg.sender_ip = input['sender_ip']
        new_msg.company_id = input['company_id']
        new_msg.sensors_msg = json.dumps(input['sensors_msg'])
        new_msg.created_date = datetime.now()
        db.session.add(new_msg)
        db.session.commit()
    #collection.insert(obj)
    except :
        result = {
            "ACK":"FAIL",
            "MSG":"mongodb input exception"
        }

    return make_response(jsonify(result), 200)

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
    upload_path = os.getcwd() + '/download/excel/'
    return send_from_directory(upload_path, filename)

global download_index
download_index = 0
@app.route('/api/v1/patent_manage_download', methods=['get'])
def patent_manage_download_api():
    print("patent_manage_download_api start...")
    parser = reqparse.RequestParser()
    parser.add_argument("tech_type", type=str, location='args', required=True)
    parser.add_argument("years", type=str, location='args', required=True)
    parser.add_argument("search_string", type=str, location='args', required=True)
    args = parser.parse_args()
    tech_type = int(args['tech_type'])
    years = args['years']
    search_string = args['search_string']
    templete_path = './download/excel/templete/patent_manage_xl_template0.xlsx'

    #xl파일 형식지정
    center_align = Alignment(horizontal='center',
                            vertical='bottom',
                            text_rotation=0,
                            wrap_text=False,
                            shrink_to_fit=True,
                            indent=0)

    thin_border = Border(left=Side(style='thin'),
                         right=Side(style='thin'),
                         top=Side(style='thin'),
                         bottom=Side(style='thin'))

    filter_or_group = []
    filter_and_group = []
    if tech_type is not None and tech_type != -1 :
        filter_and_group.append(KitechSource.tech_type == tech_type)
    if years is not None and years != '전체' :
        filter_and_group.append(KitechSource.apply_date == years)
    if search_string is not None and search_string != '' :
        filter_or_group.append(KitechSource.person.like("%" + search_string + "%"))
        filter_or_group.append(KitechSource.patent_code.like("%" + search_string + "%"))
        filter_or_group.append(KitechSource.description.like("%" + search_string + "%"))

    source_data = KitechSource.query.filter(or_(*filter_or_group)).filter(and_(*filter_and_group)).order_by(KitechSource.id.desc()).all()
    print("len : ",len(source_data))
    wb = openpyxl.load_workbook(templete_path)
    ws = wb['Sheet1']
    xl_range = 7
    cur=0
    for rows in source_data:
        line_tuple = (
            rows.patent_code,
            rows.person,
            rows.apply_date,
            tech_types_dict[rows.tech_type],
            rows.invention_title[:30],
           rows.updated_date.strftime("%Y-%m-%d %H:%M:%S")
        )
        for i in range(xl_range):
            ws.cell(row=cur+1, column=i+1).border = thin_border
            ws.cell(row=cur+1, column=i+1).alignment = center_align
        cur+=1
        ws.append(line_tuple)

    for k in range(3):
        for i in range(xl_range):
            ws.cell(row=cur+1, column=i+1).border = thin_border
            ws.cell(row=cur+1, column=i+1).alignment = center_align
        cur+=1
    global download_index
    download_index += 1
    save_file_name = 'download_xl_file_{0}.xlsx'.format(download_index)
    save_file_path = './download/excel/' + save_file_name
    if os.path.isfile(save_file_path):
      os.remove(save_file_path)

    wb.save(save_file_path)
    res = {
        "filename":save_file_name
    }

#     print("type:",tab_item)
#     print(type(tab_item))
#     print("templete:",templete_path)
#     print('xl_range:',xl_range)
    return make_response(jsonify(res), 200)

@app.route('/api/v1/statics_report', methods=['GET'])
def statics_report_api():
    parser = reqparse.RequestParser()
    args = parser.parse_args()
    response = dict()
    print("args :",args)

    q = KitechSource.query.with_entities(
        KitechSource.tech_type,
        func.count(KitechSource.id).label('count')) \
        .group_by(KitechSource.tech_type).all()

    response['tech_types_objs'] = [dict(tech_type=item.tech_type, count=item.count) for item in q]
    print("response['tech_types_objs'] :",response['tech_types_objs'] )

    q = KitechSource.query.with_entities(
        KitechSource.person,
        func.count(KitechSource.id).label('count')) \
        .group_by(KitechSource.person).order_by(func.count(KitechSource.id).desc()).limit(5).all()

    response['person_objs'] = [dict(person=item.person, count=item.count) for item in q]
    print("response['person_objs'] :",response['person_objs'] )

    q = KitechSource.query.with_entities(
        KitechSource.apply_date,
        func.count(KitechSource.id).label('count')) \
        .group_by(KitechSource.apply_date).order_by(KitechSource.apply_date.desc()).limit(5).all()

    response['apply_date_objs'] = [dict(apply_date=str(item.apply_date) + "년", count=item.count) for item in q]
    print("response['apply_date_objs'] :",response['apply_date_objs'] )

    q = KITECH_USER_ACTION.query.with_entities(
        KITECH_USER_ACTION.create_date,
        func.count(KITECH_USER_ACTION.id).label('count')) \
        .filter(KITECH_USER_ACTION.create_date >= (datetime.now()-timedelta(days=365))) \
        .group_by(func.year(KITECH_USER_ACTION.create_date),func.month(KITECH_USER_ACTION.create_date)).order_by(KITECH_USER_ACTION.create_date.asc()).limit(12).all()

    response['user_action_months_objs'] = [dict(month=item.create_date.strftime("%Y-%m"), count=item.count) for item in q]
    print("response['user_action_months_objs'] :",response['user_action_months_objs'] )

    q = KITECH_USER_ACTION.query.with_entities(
        KITECH_USER_ACTION.search_string,
        func.count(KITECH_USER_ACTION.id).label('count')) \
        .group_by(KITECH_USER_ACTION.patent_code).order_by(func.count(KITECH_USER_ACTION.id).desc()).limit(10).all()
    response['search_rank_objs'] = [dict(search_string=item.search_string, count=item.count) for item in q]
    print("response['search_rank_objs'] :",response['search_rank_objs'] )

    return make_response(jsonify(response), 200)

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