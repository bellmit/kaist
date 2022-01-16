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



class KitechReport(db.Model):
    __tablename__ = 'tb_kitech_report'

    id = db.Column('idx', db.Integer, primary_key=True)
    create_date = db.Column('create_date', db.DateTime, default=datetime.datetime.now)
    patent_code = db.Column('patent_code', db.String(20))
    query_string = db.Column('query_string', db.String(256))
    user_id = db.Column('user_id', db.String(48))
    fk_vendor_id = db.Column('fk_vendor_id', db.Integer)


class KitechTrainResult(db.Model):
    __tablename__ = 'tb_kitech_train_result'

    id = db.Column('idx', db.Integer, primary_key=True)
    weight_name = db.Column('weight_name', db.String(1024)) # 모델이름
    result_accuracy = db.Column('result_accuracy', db.Float) #모델 정확도
    create_date = db.Column('create_date', db.DateTime) #모델 만들날짜
    memo = db.Column('memo', db.String(1024)) # 모델설명
    active = db.Column('active', db.Integer) #모델 활성화
    epoch = db.Column('epoch', db.Integer) #모델 학습 반복수
    filter_doc_count = db.Column('filter_doc_count', db.Integer) #모델 재검색 문서 수
    top_search = db.Column('top_search', db.Integer) #모든문단 검색 여부
    use_query_expend = db.Column('use_query_expend', db.Integer) #쿼리확장사용


class TB_KITECH_PATENT_PARAGRAPH(db.Model):
    __tablename__ = 'tb_kitech_patent_paragraph'
    idx = db.Column('idx', db.Integer, primary_key=True)
    patent_code = db.Column('patent_code', db.String(20))
    p_idx = db.Column('p_idx',  db.Integer)
    k_nouns_p = db.Column('k_nouns_p',  db.Integer)
    invention_title_noun = db.Column('invention_title_noun', db.String(512))
    patent_paragraph = db.Column('patent_paragraph', db.String(4096))
    patent_paragraph_expend = db.Column('patent_paragraph_expend', db.String(4096))

class KITECH_USER_ACTION(db.Model):
    __tablename__ = 'tb_kitech_user_action'

    id = db.Column('idx', db.Integer, primary_key=True)
    patent_code = db.Column('patent_code', db.String(20))
    p_idx = db.Column('p_idx',  db.Integer)
    rank = db.Column('rank',  db.Integer)
    search_string = db.Column('search_string', db.String(256))
    user_id = db.Column('user_id', db.String(48))
    action_type = db.Column('action_type',  db.Integer)
    create_date = db.Column('create_date', db.DateTime, default=datetime.datetime.now)
    fk_vendor_id = db.Column('fk_vendor_id', db.Integer)
    fk_users = db.Column('fk_users', db.Integer)

class KITECH_QUESTION(db.Model):
    __tablename__ = 'tb_kitech_question'

    id = db.Column('idx', db.Integer, primary_key=True)
    user_id = db.Column('user_id', db.String(48))
    question_title = db.Column('question_title', db.String(256))
    question_contents = db.Column('question_contents', db.String(4092))
    create_date = db.Column('create_date', db.DateTime, default=datetime.datetime.now)
    fk_vendor_id = db.Column('fk_vendor_id', db.Integer)

class TB_KITECH_SEARCH_HIST(db.Model):
    __tablename__ = 'tb_kitech_search_hist'
    idx = db.Column('idx', db.Integer, primary_key=True)
    search_string = db.Column('search_string', db.String(1024))
    kitech_count = db.Column('kitech_count', db.Integer)
    search_result = db.Column('search_result', db.String(4096))
    search_user = db.Column('search_user',db.String(50))
    weight_name = db.Column('weight_name', db.String(50))
    create_date = db.Column('create_date', db.DateTime)
    filter_doc_count = db.Column('filter_doc_count', db.Integer)
    fk_vendor_id = db.Column('fk_vendor_id', db.Integer)

class TB_KICET_PATENT_PARAGRAPH(db.Model):
    __tablename__ = 'tb_kicet_patent_paragraph'
    idx = db.Column('idx', db.Integer, primary_key=True)
    patent_code = db.Column('patent_code', db.String(20))
    p_idx = db.Column('p_idx',  db.Integer)
    k_nouns_p = db.Column('k_nouns_p',  db.Integer)
    invention_title_noun = db.Column('invention_title_noun', db.String(512))
    patent_paragraph = db.Column('patent_paragraph', db.String(4096))
    patent_paragraph_expend = db.Column('patent_paragraph_expend', db.String(4096))

class TB_VENDOR(db.Model):
    __tablename__ = 'tb_vendor'

    id = db.Column('id', db.Integer, primary_key=True)
    vendor_id = db.Column('vendor_id', db.String(128))
    vendor_name = db.Column('vendor_name', db.String(128))
    vendor_use = db.Column('vendor_use', db.Integer)
    active = db.Column('active', db.Integer)

class TB_TEMP(db.Model):
    __tablename__ = 'tb_temp'

    idx = db.Column('idx', db.Integer, primary_key=True)
    patent_code = db.Column('patent_code', db.String(20)) # 특허번호

class TB_SENSOR_UPLOAD(db.Model):
    __tablename__ = 'tb_sensor_upload'

    id = db.Column('id', db.Integer, primary_key=True)
    sender_ip = db.Column('sender_ip', db.String(128))
    company_id = db.Column('company_id', db.String(128))
    sensors_msg = db.Column('sensors_msg', db.String(2048))
    created_date = db.Column('created_date', db.DateTime)

class Community(db.Model):
    __tablename__ = 'tb_community'
    id = db.Column('id', db.Integer, primary_key=True)
    title = db.Column('title', db.String(48))
    contents = db.Column('contents', db.String(4096))
    response_contents = db.Column('response_contents', db.String(4096))
    attatch_file_path = db.Column('attatch_file_path', db.String(2048))
    attatch_file_name = db.Column('attatch_file_name', db.String(2048))
    community_type = db.Column('community_type', db.Integer, default=1)
    user_id = db.Column('user_id', db.String(48))
    user_name = db.Column('user_name', db.String(48))
    created_date = db.Column('created_date', db.DateTime)
    updated_date = db.Column('updated_date', db.DateTime)
    open = db.Column('open', db.Integer, default=0)
    open_range = db.Column('open_range', db.Integer, default=0)
    view_cnt = db.Column('view_cnt', db.Integer, default=0)
    parent_id = db.Column('parent_id', db.Integer, default=-1)

    def serialize(self):
        resultJSON = {
            # property (a)
            "id": self.id
            , "title": self.title
            , "contents": self.contents
            , "response_contents": self.response_contents
            , "attatch_file_path": self.attatch_file_path
            , "attatch_file_name": self.attatch_file_name
            , "community_type": self.community_type
            , "user_id": self.user_id
            , "user_name": self.user_name
            , "created_date": self.created_date
            , "updated_date": self.updated_date
            , "open": self.open
            , "open_range": self.open_range
            , "view_cnt": self.view_cnt
            , "parent_id": self.parent_id
        }
        return resultJSON

class SmallPatent(db.Model):
    __tablename__ = 'tb_small_patent'
    id = db.Column('id', db.Integer, primary_key=True)
    title = db.Column('title', db.String(48))
    contents = db.Column('contents', db.String(4096))
    attatch_file_path = db.Column('attatch_file_path', db.String(2048))
    attatch_file_name = db.Column('attatch_file_name', db.String(2048))
    created_date = db.Column('created_date', db.DateTime)
    updated_date = db.Column('updated_date', db.DateTime)
    view_cnt = db.Column('view_cnt', db.Integer, default=0)
    patent_code = db.Column('patent_code', db.String(48))
    costcontents = db.Column('costcontents', db.String(48))

    def serialize(self):
        resultJSON = {
            # property (a)
            "id": self.id
            , "title": self.title
            , "contents": self.contents
            , "attatch_file_path": self.attatch_file_path
            , "attatch_file_name": self.attatch_file_name
            , "created_date": self.created_date
            , "updated_date": self.updated_date
            , "view_cnt": self.view_cnt
            , "patent_code": self.patent_code
            , "costcontents": self.costcontents
        }
        return resultJSON

class PopupZone(db.Model):
    __tablename__ = 'tb_popup_zone'
    id = db.Column('id', db.Integer, primary_key=True)
    title = db.Column('title', db.String(48))
    contents = db.Column('contents', db.String(4096))
    attatch_file_path = db.Column('attatch_file_path', db.String(2048))
    attatch_file_name = db.Column('attatch_file_name', db.String(2048))
    created_date = db.Column('created_date', db.DateTime)
    updated_date = db.Column('updated_date', db.DateTime)
    view_cnt = db.Column('view_cnt', db.Integer, default=0)
    def serialize(self):
        resultJSON = {
            # property (a)
            "id": self.id
            , "title": self.title
            , "contents": self.contents
            , "attatch_file_path": self.attatch_file_path
            , "attatch_file_name": self.attatch_file_name
            , "created_date": self.created_date
            , "updated_date": self.updated_date
            , "view_cnt": self.view_cnt
        }
        return resultJSON

class TechTrans(db.Model):
    __tablename__ = 'tb_tech_trans'
    id = db.Column('id', db.Integer, primary_key=True)
    company_name = db.Column('company_name', db.String(48))
    patent_code = db.Column('patent_code', db.String(48))
    bussiness_num = db.Column('bussiness_num', db.String(48))
    request_name = db.Column('request_name', db.String(48))
    request_phone = db.Column('request_phone', db.String(48))
    request_email = db.Column('request_email', db.String(48))
    techtrans_type = db.Column('techtrans_type', db.Integer, default=0)
    request_contents = db.Column('request_contents', db.String(2048))
    result_contents = db.Column('result_contents',  db.String(2048))
    techtrans_result = db.Column('techtrans_result', db.Integer, default=0)
    created_date = db.Column('created_date', db.DateTime)
    updated_date = db.Column('updated_date', db.DateTime)
    def serialize(self):
        resultJSON = {
            # property (a)
            "id": self.id
            , "company_name": self.company_name
            , "patent_code": self.patent_code
            , "bussiness_num": self.bussiness_num
            , "request_name": self.request_name
            , "request_phone": self.request_phone
            , "request_email": self.request_email
            , "techtrans_type": self.techtrans_type
            , "request_contents": self.request_contents
            , "result_contents": self.result_contents
            , "techtrans_result": self.techtrans_result
            , "created_date": self.created_date
            , "updated_date": self.updated_date
        }
        return resultJSON

class TechTypeList(db.Model):
    __tablename__ = 'tb_kitech_tech_list'
    id = db.Column('idx', db.Integer, primary_key=True)
    main_person = db.Column('main_person', db.String(50))
    patent_title = db.Column('patent_title', db.String(2048))
    patent_code = db.Column('patent_code', db.String(50))
    tech_type_name = db.Column('tech_type_name', db.String(50))
