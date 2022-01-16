# -*- coding: utf-8 -*-
from backend import manager
from backend.api_common import *
from backend_model.table_user import *
from backend_model.table_patent import *
from flask_restless import ProcessingException

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import random
print("module [backend.api_user] loaded")

db = DBManager.db

import shutil
@app.route('/api/v1/update_tech_type', methods=["GET"])
def update_tech_type_api():
    print('update_tech_type run')
    data_list = KitechSource.query.all()
    for data in data_list :
        obj = {
            "tech_type":random.randint(0,5)
        }
        db.session.query(KitechSource).filter_by(id=data.id).update(obj)
    db.session.commit()
    print('api end')
    return make_response(jsonify({}), 200)