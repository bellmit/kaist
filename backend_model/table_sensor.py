# -*- coding: utf-8 -*-

print ("module [backend_model.table_patent.py] loaded")
from backend_model.database import DBManager
from backend_model.table_user import Users
import datetime

db = DBManager.db


class KitechSource(db.Model):
    __tablename__ = 'tb_kitech_source'

    id = db.Column('id', db.Integer, primary_key=True)
    patent_code = db.Column('patent_code', db.String(20)) # 특허번호
    person = db.Column('person', db.String(50))
    main_person = db.Column('main_person', db.String(50))
    description = db.Column('description', db.Text)
    invention_title = db.Column('invention_title', db.Text) # 특허제목
    technical_field = db.Column('technical_field', db.Text)
    background_art = db.Column('background_art', db.Text)
    citation_list = db.Column('citation_list', db.Text)
    summary_of_invention = db.Column('summary_of_invention', db.Text) # 특허요약
    description_of_drawings = db.Column('description_of_drawings', db.Text)
    description_of_embodiments = db.Column('description_of_embodiments', db.Text) # 특허본문
    maketting_file_path = db.Column('maketting_file_path', db.String(200))
    updated_date = db.Column('updated_date', db.DateTime, default=datetime.datetime.now)
    apply_date = db.Column('apply_date', db.String(50))
    tech_type = db.Column('tech_type', db.Integer)
    #check = db.Column('check', db.Integer)


class TB_VENDOR(db.Model):
    __tablename__ = 'tb_vendor'

    id = db.Column('id', db.Integer, primary_key=True)
    vendor_id = db.Column('vendor_id', db.String(128))
    vendor_name = db.Column('vendor_name', db.String(128))
    vendor_use = db.Column('vendor_use', db.Integer)
    active = db.Column('active', db.Integer)


class TB_SENSOR_UPLOAD(db.Model):
    __tablename__ = 'tb_sensor_upload'

    id = db.Column('id', db.Integer, primary_key=True)
    sender_ip = db.Column('sender_ip', db.String(128))
    company_id = db.Column('company_id', db.String(128))
    sensors_msg = db.Column('sensors_msg', db.String(2048))
    created_date = db.Column('created_date', db.DateTime)

