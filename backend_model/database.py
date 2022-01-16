#!/usr/bin/python
# -*- coding: utf-8 -*-
print ("module [backend_model.database] loaded")
from datetime import datetime, timedelta
import random
import hashlib


from flask_sqlalchemy import SQLAlchemy

# To solve deadlock
class SQLiteAlchemy(SQLAlchemy):
    def apply_driver_hacks(self, app, info, options):
        options.update({
            'isolation_level': 'READ UNCOMMITTED',
        })
        super(SQLiteAlchemy, self).apply_driver_hacks(app, info, options)

class DBManager:
    db = None

    @staticmethod
    def init(app):
        # print "-- DBManager init()"
        db = SQLiteAlchemy(app)
        DBManager.db = db

    @staticmethod
    def init_db():
        # print "-- DBManager init_db()"
        db = DBManager.db
        db.drop_all()
        db.create_all()
        DBManager.insert_dummy_data()

    @staticmethod
    def clear_db():
        # print "-- DBManager clear_db()"
        DBManager.db.drop_all()

    @staticmethod
    def insert_dummy_data():
        print ('insert_dummy_data')
        DBManager.insert_dummy_user()
        DBManager.insert_dummy_category()
        DBManager.insert_dummy_applications()

    @staticmethod
    def password_encoder(password):
        pass1 = hashlib.sha1(password).digest()
        pass2 = hashlib.sha1(pass1).hexdigest()
        hashed_pw = "*" + pass2.upper()
        return hashed_pw

    @staticmethod
    def get_random_date():
        end = datetime.utcnow()
        start = end + timedelta(days=-60)

        random_date = start + timedelta(
            # Get a random amount of seconds between `start` and `end`
            seconds=random.randint(0, int((end - start).total_seconds())),
        )

        return random_date

    @staticmethod
    def password_encoder_512(password):
        h = hashlib.sha512()
        h.update(password.encode('utf-8'))
        return h.hexdigest()

    @staticmethod
    def get_random_ip():
        ip_list = [u'28.23.43.1', u'40.12.33.11', u'100.123.234.11', u'61.34.22.44', u'56.34.56.77', u'123.234.222.55']

        return ip_list[random.randrange(0, 6)]

    @staticmethod
    def gen_datetime(min_year=2019, max_year=datetime.now().year):
        # generate a datetime in format yyyy-mm-dd hh:mm:ss.000000
        start = datetime(min_year, 1, 1, 00, 00, 00)
        years = max_year - min_year + 1
        end = start + timedelta(days=365 * years)
        return start + (end - start) * random.random()

    def generate_token(userID):
        m = hashlib.sha1()

        m.update(userID.encode('utf-8'))
        m.update(datetime.now().isoformat().encode('utf-8'))

        return m.hexdigest()

    def insert_dummy_user():
        print ("insert_dummy_user")
        from backend_model.table_user import Users

        user = Users()
        user.user_id = "admin"
        user.user_pw = DBManager.password_encoder_512('111111')
        user.user_name = "admin"
        user.user_type = 1
        user.phone = "010-1234-5678"
        DBManager.db.session.add(user)

        user = Users()
        user.user_id = "admin2"
        user.user_pw = DBManager.password_encoder_512('111111')
        user.user_name = "admin2"
        user.user_type = 1
        user.phone = "010-1234-5678"
        DBManager.db.session.add(user)

        user = Users()
        user.user_id = "admin3"
        user.user_pw = DBManager.password_encoder_512('111111')
        user.user_name = "admin3"
        user.user_type = 1
        user.phone = "010-1234-5678"
        DBManager.db.session.add(user)

        user = Users()
        user.user_id = "prof1"
        user.user_pw = DBManager.password_encoder_512('111111')
        user.user_name = "prof1"
        user.user_type = 2
        user.phone = "010-1234-5678"
        DBManager.db.session.add(user)

        user = Users()
        user.user_id = "prof2"
        user.user_pw = DBManager.password_encoder_512('111111')
        user.user_name = "prof2"
        user.user_type = 2
        user.phone = "010-1234-5678"
        DBManager.db.session.add(user)

        user = Users()
        user.user_id = "prof3"
        user.user_pw = DBManager.password_encoder_512('111111')
        user.user_name = "prof3"
        user.user_type = 2
        user.phone = "010-1234-5678"
        DBManager.db.session.add(user)

        user = Users()
        user.user_id = "user1"
        user.user_pw = DBManager.password_encoder_512('111111')
        user.user_name = "user1"
        user.user_type = 3
        user.phone = "010-1234-5678"
        DBManager.db.session.add(user)

        user = Users()
        user.user_id = "user2"
        user.user_pw = DBManager.password_encoder_512('111111')
        user.user_name = "user2"
        user.user_type = 3
        user.phone = "010-1234-5678"
        DBManager.db.session.add(user)

        user = Users()
        user.user_id = "user3"
        user.user_pw = DBManager.password_encoder_512('111111')
        user.user_name = "user3"
        user.user_type = 3
        user.phone = "010-1234-5678"
        DBManager.db.session.add(user)

        DBManager.db.session.commit()

    def insert_dummy_category():
        print ("insert_dummy_category")
        from backend_model.table_abl import Category

        cat = Category()
        cat.depth = 0
        cat.title = "성과범주"
        DBManager.db.session.add(cat)

        cat = Category()
        cat.depth = 0
        cat.title = "산업범주"
        DBManager.db.session.add(cat)

        cat = Category()
        cat.depth = 1
        cat.title = "제품 혁신"
        cat.parent_id = 1
        DBManager.db.session.add(cat)

        cat = Category()
        cat.depth = 1
        cat.title = "프로세스 혁신"
        cat.parent_id = 1
        DBManager.db.session.add(cat)

        cat = Category()
        cat.depth = 1
        cat.title = "비지니스 모델 혁신"
        cat.parent_id = 1
        DBManager.db.session.add(cat)

        cat = Category()
        cat.depth = 1
        cat.title = "기타"
        cat.parent_id = 1
        DBManager.db.session.add(cat)

        cat = Category()
        cat.depth = 1
        cat.title = "자동차, 기계"
        cat.parent_id = 2
        DBManager.db.session.add(cat)

        cat = Category()
        cat.depth = 1
        cat.title = "정부, 공공"
        cat.parent_id = 2
        DBManager.db.session.add(cat)

        cat = Category()
        cat.depth = 1
        cat.title = "제조, 재료"
        cat.parent_id = 2
        DBManager.db.session.add(cat)

        cat = Category()
        cat.depth = 1
        cat.title = "반도체, 디스플레이"
        cat.parent_id = 2
        DBManager.db.session.add(cat)

        cat = Category()
        cat.depth = 1
        cat.title = "S/W, 콘텐츠"
        cat.parent_id = 2
        DBManager.db.session.add(cat)

        cat = Category()
        cat.depth = 1
        cat.title = "기타"
        cat.parent_id = 2
        DBManager.db.session.add(cat)

        cat = Category()
        cat.depth = 2
        cat.title = "신규 연구개발 수주"
        cat.parent_id = 3
        DBManager.db.session.add(cat)

        cat = Category()
        cat.depth = 2
        cat.title = "국내 판로 개척 매출 증대"
        cat.parent_id = 3
        DBManager.db.session.add(cat)

        cat = Category()
        cat.depth = 2
        cat.title = "국내 판매 수량 매출 증대"
        cat.parent_id = 3
        DBManager.db.session.add(cat)

        cat = Category()
        cat.depth = 2
        cat.title = "해외 판로 개척 매출"
        cat.parent_id = 3
        DBManager.db.session.add(cat)

        cat = Category()
        cat.depth = 2
        cat.title = "월가 절감액"
        cat.parent_id = 4
        DBManager.db.session.add(cat)

        cat = Category()
        cat.depth = 2
        cat.title = "정부 프로세스 혁신 지원 수주"
        cat.parent_id = 4
        DBManager.db.session.add(cat)

        cat = Category()
        cat.depth = 2
        cat.title = "창업 건수"
        cat.parent_id = 5
        DBManager.db.session.add(cat)

        cat = Category()
        cat.depth = 2
        cat.title = "기존 기업 비지니스 모델 혁신 건수"
        cat.parent_id = 5
        DBManager.db.session.add(cat)

        DBManager.db.session.commit()


    def insert_dummy_applications():
        print("insert_dummy_applications")
        from backend_model.table_abl import Applications, Projects, ProgressLogs, Reports

        appl = Applications()
        appl.name = "조영수, 이동현, 김용성"
        appl.student_id = "20165513, 20165496, 20165482"
        appl.major = "기술경영학과"
        appl.training_period = "하계"
        appl.company = "삼성디스플레이(SDC)"
        appl.ceo = "권오현"
        appl.product = "LCD/OLED Panel"
        appl.biz_category = "전자부품"
        appl.subject = "사회적 기업 창업 아카데미 운영"
        appl.contents = "퇴직 임직원(고연령 계층)을 대상으로 사회적 기업가 양성 교육 및 " \
                        "창업Program을 운영하여 사회 再진출을 지원 (Outplacement), " \
                        "장기적으로는 퇴직 임직원의 일자리 창출 및 건강한 사회적 기업을 " \
                        "육성, 발전시켜 지역사회 / 경제에 기여할 수 있는 효과를 기대"

        DBManager.db.session.add(appl)

        proj = Projects()
        proj.name = "사회적 기업 창업 아카데미 운영"
        proj.professor = "김학수 교수님, 정희운 교수님"
        proj.participants = "조영수, 이동현, 김용성"
        proj.issue = "고연령 임직원(50歲↑)이 퇴직 後사회 再진출 時 막연한 두려움 체계적 교육 부족으로 " \
                     "경력단절 및 창업기회 상실로 이어지는 경우 多 , 당사의 기업규모를 감안 지역사회와 " \
                     "연계한 건강한 사회적 기업 모델 필요"
        proj.needs = "퇴직준비 및 제2의 인생 설계에 대한 다양한 정보제공 및 실효적/실질적 교육 필요, " \
                     "장기적 Plan으로 당사 사회공헌과 연계한 사회적 기업 창업 및 육성"
        proj.purpose = "① 사회적 기업 창업 아카데미 Program운영" \
                       "- 퇴직 예정 임직원 중 희망자를 대상으로 교육 프로그램 운영" \
                       "② 프로젝트 목적" \
                       "- 아카데미 수료인원에 대해 다양한 정보제공 및 실효적/실질적 창업지원" \
                       "- 지역사회內 사회 경제 Network 참여 촉진 및 사회적 활동가 양성"
        proj.scope = "① 대상 : 퇴직예정 임직원 약 00명" \
                     "② 분야 : 6주 일반과정 + 9주 집중과정" \
                     "③ 기간 : ‘17. 3. 15 ~ ’17. 7. 6  " \
                     "※ 교육 커리큘럼 : 총 15회차로 구성예정"
        proj.plan1 = "프로그램 수요조사, 교육 Program 개발, 대상자 검토 및 선정"
        proj.plan2 = "교육 Program운영, 실무 Training 병행(교육/멘토링/컨설팅等), 과정관리를 통한 F/B"
        proj.plan3 = "교육수료 後 창업 및 사회적 활동가로서의 역량을 펼칠 수 있도록 계속적인 정보제공 및 지원"
        proj.after_project = "상기 아카데미 과정을 정례화 하여 당사의 Outplacement 과정의 하나로 " \
                             "자리 잡을 수 있도록 지속보완 / 운영할 계획, 실제 사회적 기업 창업 및 사회적 " \
                             "활동가 역할을 수행할 수 있도록 컨설팅 / 관련부분 지원 지속유지 (사회 경제 Network 확대 포함)"
        proj.benefit = "① 퇴직예정 임직원들에게 사회再진출에 대한 새로운 동기부여 제공 " \
                       "② 本 아카데미 과정이 퇴직 예정자들에게 실질적으로 필요한 과정임을 인식" \
                       "→ Outplacement에 대한 부정적인 인식전환 효과 기대" \
                       "④ 실제 사회적 기업 창업을 통해 지역사회/경제에 기여, 당사이미지 제고 기대 "
        proj.fk_app_id = 1

        DBManager.db.session.add(proj)

        log = ProgressLogs()
        log.number = 1
        log.subject = "사회적 기업 창업 아카데미 운영"
        log.student_name = "조영수, 이동현, 김용성"
        log.start_date = "2020-03-15 00:00:00"
        log.end_date = "2020-03-21 00:00:00"
        log.contents = "① 프로그램 수요조사 (설문조사)" \
                       "- 대상 : 50歲 이상 임직원 30名 " \
                       "- 설문내용 요약" \
                       "1) 창업 관련 보유 자격" \
                       "*보유 32.2% (기사,사회복지사,바리스타 等) / 未보유 67.8%" \
                       "2) 창업 관련 관심 / 전문 분야" \
                       "*자영업 34.5%(카페/플로리스트 等) / 컨설팅(Audit 等) 28.3% / 기타37.2%" \
                       "3) 교육 참여 여부 / 사유" \
                       "*참여 92.7% (제2인생 계획, 새로운 삶의 도전, 노후 준비 等 )" \
                       "※ 다른 기관에서의 교육은 신뢰하기 어려워 회사에서 " \
                       "해당 과정을 개설해 주기를 희망" \
                       "4) 사회적 기업에 대한 인지도" \
                       "*알고 있다 17.6% / 들은 적 있다 23.4% / 잘 모른다 59% " \
                       "5) 기타 궁금한 사항" \
                       "*창업아이템 선정방법/초기비용, 사회적 기업의 수익/운영방법," \
                       "사회적 기업에 대한 국가지원(법인운영/자본/기타 지원책), 각종 법규 等"
        log.personal_opinion = "설문조사결과 수요는 있으나, 사회적 기업에 대한 막연한 생각과" \
                               "창업관련 지식이 전무하여 기초부터, 이해도를 높이는 방향으로 교육 프로그램 설계 및 운영 필요"
        log.expert_opinion = "신규 기업역량을 확보하기 위해 먼저 기존의 기업 역량 및 경쟁사에 대한 파악이 필요함"
        log.professor_opinion = "데이터 센터 전력 소비 구조 분석 필요,  문헌 조사 방법 및 논문 구성 교육"
        log.fk_app_id = 1
        DBManager.db.session.add(log)

        log = ProgressLogs()
        log.number = 2
        log.subject = "사회적 기업 창업 아카데미 운영"
        log.student_name = "조영수, 이동현, 김용성"
        log.start_date = "2020-04-15 00:00:00"
        log.end_date = "2020-04-21 00:00:00"
        log.contents = ""
        log.personal_opinion = "초기 Setting이 중요한 만큼 지속적인 과정관리를 통해 기대하는 효과가 나타날 수 있도록" \
                               " 잘 Manage하는데 Focus를 두고 접근"
        log.expert_opinion = "데이터 센터 냉방이 기존 자사 역량으로 진출 가능한 분야인지 확인이 필요함."
        log.professor_opinion = "1. 기술 개발이라는 포커스도 중요하지만 이를 통한 비즈니스 모델 발굴에 대한 관점에서 접근 제안" \
                                "2. 기업의 이익 창출 및 신시장 진출이라는 측면 고려"
        log.fk_app_id = 1
        DBManager.db.session.add(log)

        report = Reports()
        report.subject = "기축 데이터 센터 외기도입 냉방시스템 분석"
        report.student_name = "나준용"
        report.start_date = "2020-03-15 00:00:00"
        report.end_date = "2020-03-21 00:00:00"
        report.guidance_contents = ""
        report.guidance_plan = ""
        report.applicant_name = "나준용"
        report.student_id = "20165478"
        report.major = "기술경영학과"
        report.contact = "010-2783-0422"
        report.training_start_date = "2020-03-15 00:00:00"
        report.training_end_date = "2020-03-21 00:00:00"
        report.training_contents = "(주)귀뚜라미범양냉방의 신시장 창출 현장 문제    " \
                                   "1) 데이터 센터 외기도입 냉방 시장 진출     " \
                                   "2) 기축 데이터 센터 진출 차별화 방안  에 대한 ABL 과제 도출 및 개선 " \
                                   "설계(안) 도출 (Action Plan)   기반 이론 및 기술 모니터링, 내부 역량 분석을 통해 " \
                                   "향후 지속 성장이 예상되는 데이터 센터를 대상으로 선정    " \
                                   "→ 차별화를 위해 충분히 진출 가능한 기축 데이터 센터 에너지 효율" \
                                   "개선 냉방 시장을 목표로 외기도입 냉방 시스템에 대한 개발과" \
                                   "그 성과로 향후 신시장 진출 가능성을 입증함."

        report.etc = "  과제 중 연구 개발 과제를 통한 성과 도출을 중심으로 진행하였으며, " \
                     "향후 교수님의 지도를 통해 회사에 적합한 비즈니스 모델을 도출할 예정임."
        report.as_was = "현장 문제(이슈)에 대한 해결 과제에 대하여 실행 방안이 구체화 되지 않았으며," \
                        "영업이나 시장환경을 고려하지 않아 막연한 구상에 불과하였음."
        report.problem = "1. 회사 내부 및 시장 현황 분석을 통한 핵심 이슈 도출" \
                         "2. 개발과제 도출"
        report.assignment = "1. 데이터 센터 최적 외기도입 냉방시스템 개발 " \
                            "2. 기축 데이터 센터 최적 차별화" \
                            "3. 연간 에너지 절감량 시뮬레이션 산출"
        report.strategy = "1. 회사 및 경쟁사 현황 분석" \
                          "2. 데이터 센터 현황 및 향후 발전 가능성 검토" \
                          "3. 데이터 센터 에너지 효율 향상 방안 도출" \
                          "4. 경쟁 기술 정보 검색" \
                          "5. 관련 이론 및 논문 검색, 모니터링" \
                          "6. 프리쿨링 유닛 구상 및 설계" \
                          "7. 프리쿨링 유닛 제어 및 항온항습기 연동 방안 구상" \
                          "8. 프리쿨링 유닛 시작품 제작 및 성능시험" \
                          "9. 연간 외기온도 검색 및 공기선도 분석" \
                          "10. 연간 에너지 절감량 시뮬레이션 산출"
        report.execution = "지도교수님의 관련 지도 편달 및 자문" \
                           "협력업체(LG U+) 서초2센터 현업 근무자 자문 "
        report.feedback = "현장 문제(이슈)에 대한 구체적 해결 방안 및 Action Plan 이 설계되었음." \
                          "특히 내부 분석 및 경쟁 기술 분석을 통해 해결 과제에 대한 실행안 도출이 조속히 될 수 있었음."
        report.as_is = "1. 비즈니스 모델 도출로 신시장 진출 계기 마련" \
                       "2. SWOT 분석 및 9 Block 모델 검토" \
                       "3. 기축 데이터 센터 최적화를 위해 경량화, 슬림화 설계 필요 "
        report.qualitative_result = "1. 데이터센터 프리쿨링 유닛 외기도입 냉방시 시뮬레이션 결과" \
                                    "- 대상: LG U+ 서초2센터 7층 상면 " \
                                    "- 항온항습기 전면 운영 대비 " \
                                    "→ 공조전력 저감률 47.2% " \
                                    "2. 프리쿨링 유닛 전열효율: 71%" \
                                    "3. 외기도입 프리쿨링 유닛 개발 시작품 확보" \
                                    "4. 외기도입 최적 제어 솔루션 확보"
        report.quantitative_result = "1. 데이터 센터 시장 현황 파악" \
                                     "2. 외기도입 최적 제어 설계 기술 확보" \
                                     "3. 타켓 소비자 니즈 파악 外"
        report.fk_app_id = 1
        DBManager.db.session.add(report)

        DBManager.db.session.commit()







