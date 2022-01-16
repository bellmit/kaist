# -*- coding: utf-8 -*-
from backend import manager
from backend.api_common import *
from backend_model.table_user import *
from flask_restless import ProcessingException

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

print("module [backend.api_user] loaded")

db = DBManager.db


def pre_check_duplicate_userid(instance_id=None, data=None, **kw):

    if "user_status" in data:
        if data['user_status'] == 2:
            pass
        else:
            check_token()
    else:
        check_token()

    if "user_pw" in data:
        data['user_pw'] = password_encoder_512(data['user_pw'])

    if "user_id" in data:
        chk_user = Users.query.filter(Users.user_id == data['user_id']).first()

        if instance_id is None:  # Post
            if chk_user is not None:
                raise ProcessingException(description="User ID is duplicated", code=413)
        else:  # Patch
            if (chk_user is not None) and (int(instance_id) != chk_user.id):
                raise ProcessingException(description="User ID is duplicated", code=413)

        data['token'] = generate_token(data['user_id'])


def post_post_user(result=None, **kw):
    if result['user_status'] == 2:
        message = "아래의 링크를 클릭하여 인증을 한 후에 로그인 하세요.<br><br>"
        link_str = "링크 : <a href='%s?id=%s&token=%s'>이메일인증하기</a>" % (app.config["AUTH_URL"], result['user_id'], result['token'])
        message += link_str

        server = smtplib.SMTP_SSL(app.config['SMTP_ADDR'], app.config['SMTP_PORT'])
        server.login(app.config['SMTP_LOGIN_ID'], app.config['SMTP_LOGIN_PW'])

        msg = MIMEMultipart('alternative')
        msg['From'] = "%s <%s>" % ("", app.config['SMTP_SENDER'])
        msg['To'] = result['email']
        msg['Subject'] = "특허검색 회원가입 인증메일"
        msg.attach(MIMEText(message, 'html', 'utf-8'))  # 내용 인코딩
        server.sendmail(app.config['SMTP_SENDER'], result['email'], msg.as_string())


manager.create_api(Users
                   , url_prefix='/api/v1'
                   , collection_name='users'
                   , methods=['GET', 'PUT', 'DELETE', 'PATCH', 'POST']
                   , allow_patch_many=True
                   , preprocessors={
                        'POST': [pre_check_duplicate_userid],
                        'PATCH_SINGLE': [pre_check_duplicate_userid],
                        'GET_SINGLE': [check_token_single],
                        'GET_MANY': [check_token]
                   }, postprocessors={
                        'POST': [post_post_user]
                   })


def pre_get_many_access_history(search_params=None, **kw):
    user = check_token()

    if 'filters' not in search_params:
        search_params['filters'] = []

    filt = dict(name='fk_user_id', op='eq', val=user.id)
    search_params['filters'].append(filt)


manager.create_api(AccessHistory
                   , url_prefix='/api/v1'
                   , collection_name='access_history'
                   , methods=['GET', 'PUT', 'DELETE', 'PATCH', 'POST']
                   , allow_patch_many=True
                   , preprocessors={
                        'POST': [check_token],
                        'PATCH_SINGLE': [check_token_single],
                        'GET_SINGLE': [check_token],
                        'GET_MANY': [pre_get_many_access_history]
                   })


@app.route('/api/v1/profile', methods=['GET'])
def profile_api():
    user = check_token()

    result = {'id': user.id, 'user_id': user.user_id, 'user_name': user.user_name, 'phone': user.phone,
             'user_type': user.user_type, 'email': user.email}

    return make_response(jsonify(result), 200)


@app.route('/api/ext/auth', methods=['GET'])
def email_auth_api():
    id = request.args.get('id')
    token = request.args.get('token')

    if id is None or token is None:
        return make_response("<script>alert('유효하지 않은 접속입니다.(1)');</script>", 200)

    user = Users.query.filter(Users.user_id == id).filter(Users.token == token).first()

    if user is None:
        return make_response("<script>alert('유효하지 않은 접속입니다.(2)');</script>", 200)

    Users.query.filter(Users.id == user.id).update({'user_status': 1})
    db.session.commit()

    return make_response("<script>alert('인증이 완료되었습니다.');</script>", 200)

@app.route('/api/v1/users_passwd_clear', methods=['GET'])
def users_passwd_clear_api():
    print("users_passwd_clear start")
    user_id = request.args.get('user_id')
    user_name = request.args.get('user_name')
    email = request.args.get('email')

    user = Users.query.filter_by(user_id=user_id).filter_by(user_name=user_name).filter_by(email=email).first()
    if user is not None :
        passwd = 'chrlghk12!@'
        message = "패스워드가 초기화 되었습니다.<br><br>"
        link_str = "초기화 패스워드 : "  + str(passwd)
        message += link_str
        print("message :",message)
        server = smtplib.SMTP_SSL(app.config['SMTP_ADDR'], app.config['SMTP_PORT'])
        server.login(app.config['SMTP_LOGIN_ID'], app.config['SMTP_LOGIN_PW'])

        msg = MIMEMultipart('alternative')
        msg['From'] = "%s <%s>" % ("", app.config['SMTP_SENDER'])
        msg['To'] = email
        msg['Subject'] = "특허검색 패스워드 초기화 메일"
        msg.attach(MIMEText(message, 'html', 'utf-8'))  # 내용 인코딩
        server.sendmail(app.config['SMTP_SENDER'], email, msg.as_string())
        print("msg :",msg)
        Users.query.filter(Users.id == user.id).update({'user_pw': password_encoder_512(passwd)})
        db.session.commit()
        print("complete passwd :", password_encoder_512(passwd))
    else :
        return make_response("<script>alert('유효하지 않는 등록정보입니다..');</script>", 413)
    return make_response("<script>alert('인증이 완료되었습니다.');</script>", 200)






