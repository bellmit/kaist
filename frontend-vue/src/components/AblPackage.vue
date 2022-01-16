<template>
    <div class="d-flex align-start">
        <div class="report-cont">
            <div class="report-inner">
                <abl-document ref="0" class="abl-page" :class="{active: active === 0}">
                    <div class="abl-doc-title">
                        <div class="title-text-underline">
                            사이버보안진단의날 진단 결과서
                        </div>
                    </div>
                    <div class="abl-doc-body">
                        <table class="abl-table-title">
                            <colgroup>
                                <col style="width:50%" />
                            </colgroup>
                            <tr>
                                <th >일시</th>
                                <td >{{report_objs.created_date|moment('YYYY-MM-DD')}}</td>
                            </tr>
                            <tr>
                                <th >부서명</th>
                                <td ><input type="text" disabled placeholder="부서명" class="abl-input" v-model="report_objs.dept_name"></td>
                            </tr>
                        </table>
                    </div>

                    <div class="abl-doc-title-sub">
                        <div class="title-text">
                            1. 임직원 자체진단 결과
                        </div>
                    </div>
                    <div class="abl-doc-body">
                        <table class="abl-table">
                            <colgroup>
                                <col style="width:12.5%" />
                                <col style="width:12.5%" />
                                <col style="width:12.5%" />
                                <col style="width:12.5%" />
                                <col style="width:12.5%" />
                                <col style="width:12.5%" />
                                <col style="width:12.5%" />
                                <col style="width:12.5%" />
                            </colgroup>
                            <tr>
                                <th class="s-h" colspan="2">대상 인원(부서 총 인원)</th>
                                <td colspan="2"><input type="text" placeholder="명" class="abl-input" v-model="self_diagnosis_data.dept_total_count"></td>
                                <th class="s-h" colspan="3">진단 인원</th>
                                <td colspan="2"><input type="text" placeholder="명" class="abl-input" v-model="self_diagnosis_data.diagnosis_total_count"></td>
                            </tr>

                            <tr>
                                <th class="s-h" colspan="1" rowspan="7">망 구분</th>
                            </tr>
                            <tr>
                                <th class="s-h" colspan="1" rowspan="1">업무망</th>
                                <td colspan="2"><input type="text" placeholder="대" class="abl-input" v-model="self_diagnosis_data.network_work"></td>
                                <th class="s-h" colspan="1" rowspan="6">망 구분</th>
                                <th class="s-h" colspan="2" rowspan="1">e나라도움운영망</th>
                                <td colspan="2"><input type="text" placeholder="대" class="abl-input" v-model="self_diagnosis_data.network_e_op"></td>
                            </tr>
                            <tr>
                                <th class="s-h" colspan="1" rowspan="1">인터넷망</th>
                                <td colspan="2"><input type="text" placeholder="대" class="abl-input" v-model="self_diagnosis_data.network_inet"></td>
                                <th class="s-h" colspan="2" rowspan="1">e나라도움운영망 <br>(사용자지원센터)</th>
                                <td colspan="2"><input type="text" placeholder="대" class="abl-input" v-model="self_diagnosis_data.network_e_op_helper"></td>
                            </tr>
                            <tr>
                                <th class="s-h" colspan="1" rowspan="1">무선인터넷망</th>
                                <td colspan="2"><input type="text" placeholder="대" class="abl-input" v-model="self_diagnosis_data.network_wiress"></td>
                                <th class="s-h" colspan="2" rowspan="1">사이버안전센터(업무)</th>
                                <td colspan="2"><input type="text" placeholder="대" class="abl-input" v-model="self_diagnosis_data.network_cyber_work"></td>
                            </tr>
                            <tr>
                                <th class="s-h" colspan="1" rowspan="1">dBrain운영망</th>
                                <td colspan="2"><input type="text" placeholder="대" class="abl-input" v-model="self_diagnosis_data.network_dbrain_internal"></td>
                                <th class="s-h" colspan="2" rowspan="1">사이버안전센터(인터넷)</th>
                                <td colspan="2"><input type="text" placeholder="대" class="abl-input" v-model="self_diagnosis_data.network_cyber_inet"></td>
                            </tr>
                            <tr>
                                <th class="s-h" colspan="1" rowspan="1">dBrain운영망(용역)</th>
                                <td colspan="2"><input type="text" placeholder="대" class="abl-input" v-model="self_diagnosis_data.network_dbrain_external"></td>
                                <th class="s-h" colspan="2" rowspan="1">네트워크 미연결</th>
                                <td colspan="2"><input type="text" placeholder="대" class="abl-input" v-model="self_diagnosis_data.network_disconnect"></td>
                            </tr>
                            <tr>
                                <th class="s-h" colspan="1" rowspan="1">대국민망</th>
                                <td colspan="2"><input type="text" placeholder="대" class="abl-input" v-model="self_diagnosis_data.network_public"></td>
                                <th class="s-h" colspan="2" rowspan="1">그 외</th>
                                <td colspan="2"><input type="text" placeholder="대" class="abl-input" v-model="self_diagnosis_data.network_etc"></td>
                            </tr>
                            <tr>
                                <th class="s-h" colspan="2">합계(점검PC 총 대수)</th>
                                <td colspan="2"><input type="text" placeholder="대" class="abl-input" v-model="self_diagnosis_data.pc_total_count"></td>
                                <th class="s-h" colspan="1">비고</th>
                                <td colspan="3"><input type="text" placeholder="대" class="abl-input" v-model="self_diagnosis_data.etc"></td>
                            </tr>
                            <tr>
                                <th class="s-h" colspan="2" rowspan="7">진단불가자</th>
                            </tr>
                            <tr>
                                <th class="s-h" colspan="2">성명</th>
                                <th class="s-h" colspan="4">사유</th>
                            </tr>
                            <tr>
                                <td colspan="2"><input type="text" placeholder="" class="abl-input" v-model="self_diagnosis_data.no_diagnosis_name_1"></td>
                                <td colspan="4"><input type="text" placeholder="" class="abl-input" v-model="self_diagnosis_data.no_diagnosis_name_1_reason"></td>
                            </tr>
                            <tr>
                                <td colspan="2"><input type="text" placeholder="" class="abl-input" v-model="self_diagnosis_data.no_diagnosis_name_2"></td>
                                <td colspan="4"><input type="text" placeholder="" class="abl-input" v-model="self_diagnosis_data.no_diagnosis_name_2_reason"></td>
                            </tr>
                            <tr>
                                <td colspan="2"><input type="text" placeholder="" class="abl-input" v-model="self_diagnosis_data.no_diagnosis_name_3"></td>
                                <td colspan="4"><input type="text" placeholder="" class="abl-input" v-model="self_diagnosis_data.no_diagnosis_name_3_reason"></td>
                            </tr>
                            <tr>
                                <td colspan="2"><input type="text" placeholder="" class="abl-input" v-model="self_diagnosis_data.no_diagnosis_name_4"></td>
                                <td colspan="4"><input type="text" placeholder="" class="abl-input" v-model="self_diagnosis_data.no_diagnosis_name_4_reason"></td>
                            </tr>
                            <tr>
                                <td colspan="2"><input type="text" placeholder="" class="abl-input" v-model="self_diagnosis_data.no_diagnosis_name_5"></td>
                                <td colspan="4"><input type="text" placeholder="" class="abl-input" v-model="self_diagnosis_data.no_diagnosis_name_5_reason"></td>
                            </tr>
                            <tr>
                                <th class="s-h" colspan="4" rowspan="1">진단항목</th>
                                <th class="s-h" colspan="1">결과</th>
                                <th class="s-h" colspan="3">비고</th>
                            </tr>
                            <tr>
                                <th class="s-h p-left" colspan="4" rowspan="1">(1.1) 내PC 지키미</th>
                                <td colspan="1"><input type="text" placeholder="" class="abl-input" v-model="self_diagnosis_data.diagnosis_mypc_result"></td>
                                <td colspan="3"><input type="text" placeholder="" class="abl-input" v-model="self_diagnosis_data.diagnosis_mypc_remark"></td>
                            </tr>
                            <tr>
                                <th class="s-h p-left" colspan="4" rowspan="1">(1.2) 매체제어 프로그램 설치</th>
                                <td colspan="1"><input type="text" placeholder="" class="abl-input" v-model="self_diagnosis_data.diagnosis_program_result"></td>
                                <td colspan="3"><input type="text" placeholder="" class="abl-input" v-model="self_diagnosis_data.diagnosis_program_remark"></td>
                            </tr>
                            <tr>
                                <th class="s-h p-left" colspan="4" rowspan="1">(2.1) 인터넷 PC</th>
                                <td colspan="1"><input type="text" placeholder="" class="abl-input" v-model="self_diagnosis_data.diagnosis_ipc_result"></td>
                                <td colspan="3"><input type="text" placeholder="" class="abl-input" v-model="self_diagnosis_data.diagnosis_ipc_remark"></td>
                            </tr>
                            <tr>
                                <th class="s-h p-left" colspan="4" rowspan="1">(3.1) 개인정보 파일 보호</th>
                                <td colspan="1"><input type="text" placeholder="" class="abl-input" v-model="self_diagnosis_data.diagnosis_file_result"></td>
                                <td colspan="3"><input type="text" placeholder="" class="abl-input" v-model="self_diagnosis_data.diagnosis_file_remark"></td>
                            </tr>
                        </table>
                    </div>
                    <div class="abl-doc-title-sub">
                        <div class="title-text">
                            2. 부서별 진단결과 <br>
                            (1.1.1) 휴대용저장매체 수량·관리 (보유 수량 없는 경우 공란 제출)

                        </div>
                    </div>
                    <table class="abl-table">
                        <colgroup>
                            <col style="width:14.28%" />
                            <col style="width:14.28%" />
                            <col style="width:14.28%" />
                            <col style="width:14.28%" />
                            <col style="width:14.28%" />
                            <col style="width:14.28%" />
                            <col style="width:14.28%" />
                        </colgroup>
                        <tr>
                            <th class="s-h" colspan="3">휴대용 저장매체 보유 수량</th>
                            <th class="s-h" rowspan="2" colspan="1">보유 저장매체 적정성 확인*</th>
                            <th class="s-h" rowspan="2" colspan="1">보관상태확인**</th>
                            <th class="s-h" rowspan="2" colspan="1">고장여부 확인</th>
                            <th class="s-h" rowspan="2" colspan="1">사용종료일</th>
                        </tr>
                        <tr>
                            <th class="s-h" colspan="1">일반용</th>
                            <th class="s-h" colspan="1">비밀용(대외비이상)</th>
                            <th class="s-h" colspan="1">일련번호</th>
                        </tr>
                        <tr>
                            <td rowspan="6" colspan="1"><input type="text" placeholder="" class="abl-input" v-model="form.application.company"></td>
                            <td rowspan="6" colspan="1"><input type="text" placeholder="" class="abl-input" v-model="form.application.company"></td>
                        </tr>
                        <tr>
                            <td rowspan="1" colspan="1"><input type="text" placeholder="" class="abl-input" v-model="form.application.company"></td>
                            <td rowspan="1" colspan="1"><input type="text" placeholder="" class="abl-input" v-model="form.application.company"></td>
                            <td rowspan="1" colspan="1"><input type="text" placeholder="" class="abl-input" v-model="form.application.company"></td>
                            <td rowspan="1" colspan="1"><input type="text" placeholder="" class="abl-input" v-model="form.application.company"></td>
                            <td rowspan="1" colspan="1"><input type="text" placeholder="" class="abl-input" v-model="form.application.company"></td>
                        </tr>
                        <tr>
                            <td rowspan="1" colspan="1"><input type="text" placeholder="" class="abl-input" v-model="form.application.company"></td>
                            <td rowspan="1" colspan="1"><input type="text" placeholder="" class="abl-input" v-model="form.application.company"></td>
                            <td rowspan="1" colspan="1"><input type="text" placeholder="" class="abl-input" v-model="form.application.company"></td>
                            <td rowspan="1" colspan="1"><input type="text" placeholder="" class="abl-input" v-model="form.application.company"></td>
                            <td rowspan="1" colspan="1"><input type="text" placeholder="" class="abl-input" v-model="form.application.company"></td>
                        </tr>
                        <tr>
                            <td rowspan="1" colspan="1"><input type="text" placeholder="" class="abl-input" v-model="form.application.company"></td>
                            <td rowspan="1" colspan="1"><input type="text" placeholder="" class="abl-input" v-model="form.application.company"></td>
                            <td rowspan="1" colspan="1"><input type="text" placeholder="" class="abl-input" v-model="form.application.company"></td>
                            <td rowspan="1" colspan="1"><input type="text" placeholder="" class="abl-input" v-model="form.application.company"></td>
                            <td rowspan="1" colspan="1"><input type="text" placeholder="" class="abl-input" v-model="form.application.company"></td>
                        </tr>
                        <tr>
                            <td rowspan="1" colspan="1"><input type="text" placeholder="" class="abl-input" v-model="form.application.company"></td>
                            <td rowspan="1" colspan="1"><input type="text" placeholder="" class="abl-input" v-model="form.application.company"></td>
                            <td rowspan="1" colspan="1"><input type="text" placeholder="" class="abl-input" v-model="form.application.company"></td>
                            <td rowspan="1" colspan="1"><input type="text" placeholder="" class="abl-input" v-model="form.application.company"></td>
                            <td rowspan="1" colspan="1"><input type="text" placeholder="" class="abl-input" v-model="form.application.company"></td>
                        </tr>
                        <tr>
                            <td rowspan="1" colspan="1"><input type="text" placeholder="" class="abl-input" v-model="form.application.company"></td>
                            <td rowspan="1" colspan="1"><input type="text" placeholder="" class="abl-input" v-model="form.application.company"></td>
                            <td rowspan="1" colspan="1"><input type="text" placeholder="" class="abl-input" v-model="form.application.company"></td>
                            <td rowspan="1" colspan="1"><input type="text" placeholder="" class="abl-input" v-model="form.application.company"></td>
                            <td rowspan="1" colspan="1"><input type="text" placeholder="" class="abl-input" v-model="form.application.company"></td>
                        </tr>
                        <tr>
                            <th class="s-h" colspan="2" >조치내역</th>
                            <td colspan="5"><input type="text" placeholder="" class="abl-input" v-model="form.application.ceo"></td>
                        </tr>
                    </table>
                    <div class="abl-doc-title-sub2">
                        <div class="title-text">
                            * 보유 저장매체 적정성 확인 : 사용승인을 득하지 않았거나, 사용기간 종료된 보유 저장매체 확인
                            <br>
                            ** 보관상태 확인 : 휴대용 저장매체를 시건된 장소에 안전하게 보관하는지 점검
                        </div>
                    </div>
                    <div class="abl-doc-title-sub">
                        <div class="title-text">
                            (1.1.2)반·출입* 현황 점검 (반출 수량 없는 경우 공란 제출)
                            <br>
                            * 반출 : 우리원외로 반출되어 사용되는 보안USB
                        </div>
                    </div>
                    <table class="abl-table">
                        <colgroup>
                            <col style="width:14.28%" />
                            <col style="width:14.28%" />
                            <col style="width:14.28%" />
                            <col style="width:14.28%" />
                            <col style="width:14.28%" />
                            <col style="width:14.28%" />
                            <col style="width:14.28%" />
                        </colgroup>
                        <tr>
                            <th class="s-h" colspan="3">반출중인 저장매체 수량</th>
                            <th class="s-h" rowspan="2" colspan="1">외부 반출지</th>
                            <th class="s-h" rowspan="2" colspan="2">목적</th>
                            <th class="s-h" rowspan="2" colspan="1">반입예정일</th>
                        </tr>
                        <tr>
                            <th class="s-h" colspan="1">일반용</th>
                            <th class="s-h" colspan="1">비밀용(대외비이상)</th>
                            <th class="s-h" colspan="1">일련번호</th>
                        </tr>
                        <tr>
                            <td rowspan="6" colspan="1"><input type="text" placeholder="" class="abl-input" v-model="form.application.company"></td>
                            <td rowspan="6" colspan="1"><input type="text" placeholder="" class="abl-input" v-model="form.application.company"></td>
                        </tr>
                        <tr>
                            <td rowspan="1" colspan="1"><input type="text" placeholder="" class="abl-input" v-model="form.application.company"></td>
                            <td rowspan="1" colspan="1"><input type="text" placeholder="" class="abl-input" v-model="form.application.company"></td>
                            <td rowspan="1" colspan="2"><input type="text" placeholder="" class="abl-input" v-model="form.application.company"></td>
                            <td rowspan="1" colspan="1"><input type="text" placeholder="" class="abl-input" v-model="form.application.company"></td>
                        </tr>
                        <tr>
                            <td rowspan="1" colspan="1"><input type="text" placeholder="" class="abl-input" v-model="form.application.company"></td>
                            <td rowspan="1" colspan="1"><input type="text" placeholder="" class="abl-input" v-model="form.application.company"></td>
                            <td rowspan="1" colspan="2"><input type="text" placeholder="" class="abl-input" v-model="form.application.company"></td>
                            <td rowspan="1" colspan="1"><input type="text" placeholder="" class="abl-input" v-model="form.application.company"></td>
                        </tr>
                        <tr>
                            <td rowspan="1" colspan="1"><input type="text" placeholder="" class="abl-input" v-model="form.application.company"></td>
                            <td rowspan="1" colspan="1"><input type="text" placeholder="" class="abl-input" v-model="form.application.company"></td>
                            <td rowspan="1" colspan="2"><input type="text" placeholder="" class="abl-input" v-model="form.application.company"></td>
                            <td rowspan="1" colspan="1"><input type="text" placeholder="" class="abl-input" v-model="form.application.company"></td>
                        </tr>
                        <tr>
                            <td rowspan="1" colspan="1"><input type="text" placeholder="" class="abl-input" v-model="form.application.company"></td>
                            <td rowspan="1" colspan="1"><input type="text" placeholder="" class="abl-input" v-model="form.application.company"></td>
                            <td rowspan="1" colspan="2"><input type="text" placeholder="" class="abl-input" v-model="form.application.company"></td>
                            <td rowspan="1" colspan="1"><input type="text" placeholder="" class="abl-input" v-model="form.application.company"></td>
                        </tr>
                        <tr>
                            <td rowspan="1" colspan="1"><input type="text" placeholder="" class="abl-input" v-model="form.application.company"></td>
                            <td rowspan="1" colspan="1"><input type="text" placeholder="" class="abl-input" v-model="form.application.company"></td>
                            <td rowspan="1" colspan="2"><input type="text" placeholder="" class="abl-input" v-model="form.application.company"></td>
                            <td rowspan="1" colspan="1"><input type="text" placeholder="" class="abl-input" v-model="form.application.company"></td>
                        </tr>
                        <tr>
                            <th class="s-h" colspan="2" >조치내역</th>
                            <td colspan="5"><input type="text" placeholder="" class="abl-input" v-model="form.application.ceo"></td>
                        </tr>
                    </table>

                    <div class="abl-doc-title-sub">
                        <div class="title-text">
                            (1.1.3) 외부사용* 내역 검토 (외부사용 없는 경우 공란 제출)
                            <br>
                            * 외부사용 : 원내에 매체제어 전용 프로그램이 설치되지 않은 다른망/PC/노트북에서 사용
                        </div>
                    </div>
                    <table class="abl-table">
                        <colgroup>
                            <col style="width:14.28%" />
                            <col style="width:14.28%" />
                            <col style="width:14.28%" />
                            <col style="width:14.28%" />
                            <col style="width:14.28%" />
                            <col style="width:14.28%" />
                            <col style="width:14.28%" />
                        </colgroup>
                        <tr>
                            <th class="s-h" colspan="3">외부사용 허가된 저장매체 수량</th>
                            <th class="s-h" rowspan="2" colspan="1">외부사용 매체로그 확인**</th>
                            <th class="s-h" rowspan="2" colspan="2">목적</th>
                            <th class="s-h" rowspan="2" colspan="1">사용종료일</th>
                        </tr>
                        <tr>
                            <th class="s-h" colspan="1">일반용</th>
                            <th class="s-h" colspan="1">비밀용(대외비이상)</th>
                            <th class="s-h" colspan="1">일련번호</th>
                        </tr>
                        <tr>
                            <td rowspan="6" colspan="1"><input type="text" placeholder="" class="abl-input" v-model="form.application.company"></td>
                            <td rowspan="6" colspan="1"><input type="text" placeholder="" class="abl-input" v-model="form.application.company"></td>
                        </tr>
                        <tr>
                            <td rowspan="1" colspan="1"><input type="text" placeholder="" class="abl-input" v-model="form.application.company"></td>
                            <td rowspan="1" colspan="1"><input type="text" placeholder="" class="abl-input" v-model="form.application.company"></td>
                            <td rowspan="1" colspan="2"><input type="text" placeholder="" class="abl-input" v-model="form.application.company"></td>
                            <td rowspan="1" colspan="1"><input type="text" placeholder="" class="abl-input" v-model="form.application.company"></td>
                        </tr>
                        <tr>
                            <td rowspan="1" colspan="1"><input type="text" placeholder="" class="abl-input" v-model="form.application.company"></td>
                            <td rowspan="1" colspan="1"><input type="text" placeholder="" class="abl-input" v-model="form.application.company"></td>
                            <td rowspan="1" colspan="2"><input type="text" placeholder="" class="abl-input" v-model="form.application.company"></td>
                            <td rowspan="1" colspan="1"><input type="text" placeholder="" class="abl-input" v-model="form.application.company"></td>
                        </tr>
                        <tr>
                            <td rowspan="1" colspan="1"><input type="text" placeholder="" class="abl-input" v-model="form.application.company"></td>
                            <td rowspan="1" colspan="1"><input type="text" placeholder="" class="abl-input" v-model="form.application.company"></td>
                            <td rowspan="1" colspan="2"><input type="text" placeholder="" class="abl-input" v-model="form.application.company"></td>
                            <td rowspan="1" colspan="1"><input type="text" placeholder="" class="abl-input" v-model="form.application.company"></td>
                        </tr>
                        <tr>
                            <td rowspan="1" colspan="1"><input type="text" placeholder="" class="abl-input" v-model="form.application.company"></td>
                            <td rowspan="1" colspan="1"><input type="text" placeholder="" class="abl-input" v-model="form.application.company"></td>
                            <td rowspan="1" colspan="2"><input type="text" placeholder="" class="abl-input" v-model="form.application.company"></td>
                            <td rowspan="1" colspan="1"><input type="text" placeholder="" class="abl-input" v-model="form.application.company"></td>
                        </tr>
                        <tr>
                            <td rowspan="1" colspan="1"><input type="text" placeholder="" class="abl-input" v-model="form.application.company"></td>
                            <td rowspan="1" colspan="1"><input type="text" placeholder="" class="abl-input" v-model="form.application.company"></td>
                            <td rowspan="1" colspan="2"><input type="text" placeholder="" class="abl-input" v-model="form.application.company"></td>
                            <td rowspan="1" colspan="1"><input type="text" placeholder="" class="abl-input" v-model="form.application.company"></td>
                        </tr>
                        <tr>
                            <th class="s-h" colspan="2" >사 용 내 역 <br>검 토 결 과</th>
                            <td colspan="5"><input type="text" placeholder="" class="abl-input" v-model="form.application.ceo"></td>
                        </tr>
                    </table>
                    <div class="abl-doc-title-sub">
                        <div class="title-text">
                            (2) 용역사업 보안
                        </div>
                    </div>
                    <table class="abl-table">
                        <colgroup>
                            <col style="width:7.14%" />
                            <col style="width:7.14%" />
                            <col style="width:7.14%" />
                            <col style="width:7.14%" />
                            <col style="width:7.14%" />
                            <col style="width:7.14%" />
                            <col style="width:7.14%" />
                            <col style="width:7.14%" />
                            <col style="width:7.14%" />
                            <col style="width:7.14%" />
                            <col style="width:7.14%" />
                            <col style="width:7.14%" />
                            <col style="width:7.14%" />
                            <col style="width:7.14%" />
                        </colgroup>
                        <tr>
                            <th class="s-h" colspan="1">구분</th>
                            <th class="s-h" colspan="1">사업명</th>
                            <th class="s-h" colspan="1">계약<br>체결일</th>
                            <th class="s-h" colspan="1">계약<br>기간</th>
                            <th class="s-h" colspan="1">계약<br>업체</th>
                            <th class="s-h" colspan="1">사업<br>부서</th>
                            <th class="s-h" colspan="1">현재<br>담당부서</th>
                            <th class="s-h" colspan="1">담당자</th>
                            <th class="s-h" colspan="1">수행<br>장소</th>
                            <th class="s-h" colspan="1">(2.1) <br>정보화<br>사업<br>보안성<br>검토</th>
                            <th class="s-h" colspan="1">(2.2) <br>용역사업<br>보안교육</th>
                            <th class="s-h" colspan="1">(2.3) <br>제공자료<br>보안</th>
                            <th class="s-h" colspan="1">(2.4) <br>용역사업<br>완료 후 <br>보안조치</th>
                            <th class="s-h" colspan="1">비고</th>
                        </tr>
                        <tr>
                            <th class="s-h" colspan="1">1</th>
                            <td colspan="1"><input type="text" placeholder="" class="abl-input" v-model="form.application.company"></td>
                            <td colspan="1"><input type="text" placeholder="" class="abl-input" v-model="form.application.company"></td>
                            <td colspan="1"><input type="text" placeholder="" class="abl-input" v-model="form.application.company"></td>
                            <td colspan="1"><input type="text" placeholder="" class="abl-input" v-model="form.application.company"></td>
                            <td colspan="1"><input type="text" placeholder="" class="abl-input" v-model="form.application.company"></td>
                            <td colspan="1"><input type="text" placeholder="" class="abl-input" v-model="form.application.company"></td>
                            <td colspan="1"><input type="text" placeholder="" class="abl-input" v-model="form.application.company"></td>
                            <td colspan="1"><input type="text" placeholder="" class="abl-input" v-model="form.application.company"></td>
                            <td colspan="1"><input type="text" placeholder="" class="abl-input" v-model="form.application.company"></td>
                            <td colspan="1"><input type="text" placeholder="" class="abl-input" v-model="form.application.company"></td>
                            <td colspan="1"><input type="text" placeholder="" class="abl-input" v-model="form.application.company"></td>
                            <td colspan="1"><input type="text" placeholder="" class="abl-input" v-model="form.application.company"></td>
                            <td colspan="1"><input type="text" placeholder="" class="abl-input" v-model="form.application.company"></td>

                        </tr>
                        <tr>
                            <th class="s-h" colspan="1">2</th>
                            <td colspan="1"><input type="text" placeholder="" class="abl-input" v-model="form.application.company"></td>
                            <td colspan="1"><input type="text" placeholder="" class="abl-input" v-model="form.application.company"></td>
                            <td colspan="1"><input type="text" placeholder="" class="abl-input" v-model="form.application.company"></td>
                            <td colspan="1"><input type="text" placeholder="" class="abl-input" v-model="form.application.company"></td>
                            <td colspan="1"><input type="text" placeholder="" class="abl-input" v-model="form.application.company"></td>
                            <td colspan="1"><input type="text" placeholder="" class="abl-input" v-model="form.application.company"></td>
                            <td colspan="1"><input type="text" placeholder="" class="abl-input" v-model="form.application.company"></td>
                            <td colspan="1"><input type="text" placeholder="" class="abl-input" v-model="form.application.company"></td>
                            <td colspan="1"><input type="text" placeholder="" class="abl-input" v-model="form.application.company"></td>
                            <td colspan="1"><input type="text" placeholder="" class="abl-input" v-model="form.application.company"></td>
                            <td colspan="1"><input type="text" placeholder="" class="abl-input" v-model="form.application.company"></td>
                            <td colspan="1"><input type="text" placeholder="" class="abl-input" v-model="form.application.company"></td>
                            <td colspan="1"><input type="text" placeholder="" class="abl-input" v-model="form.application.company"></td>
                        </tr>
                        <tr>
                            <th class="s-h" colspan="1">3</th>
                            <td colspan="1"><input type="text" placeholder="" class="abl-input" v-model="form.application.company"></td>
                            <td colspan="1"><input type="text" placeholder="" class="abl-input" v-model="form.application.company"></td>
                            <td colspan="1"><input type="text" placeholder="" class="abl-input" v-model="form.application.company"></td>
                            <td colspan="1"><input type="text" placeholder="" class="abl-input" v-model="form.application.company"></td>
                            <td colspan="1"><input type="text" placeholder="" class="abl-input" v-model="form.application.company"></td>
                            <td colspan="1"><input type="text" placeholder="" class="abl-input" v-model="form.application.company"></td>
                            <td colspan="1"><input type="text" placeholder="" class="abl-input" v-model="form.application.company"></td>
                            <td colspan="1"><input type="text" placeholder="" class="abl-input" v-model="form.application.company"></td>
                            <td colspan="1"><input type="text" placeholder="" class="abl-input" v-model="form.application.company"></td>
                            <td colspan="1"><input type="text" placeholder="" class="abl-input" v-model="form.application.company"></td>
                            <td colspan="1"><input type="text" placeholder="" class="abl-input" v-model="form.application.company"></td>
                            <td colspan="1"><input type="text" placeholder="" class="abl-input" v-model="form.application.company"></td>
                            <td colspan="1"><input type="text" placeholder="" class="abl-input" v-model="form.application.company"></td>
                        </tr>
                        <tr>
                            <th class="s-h" colspan="1">4</th>
                            <td colspan="1"><input type="text" placeholder="" class="abl-input" v-model="form.application.company"></td>
                            <td colspan="1"><input type="text" placeholder="" class="abl-input" v-model="form.application.company"></td>
                            <td colspan="1"><input type="text" placeholder="" class="abl-input" v-model="form.application.company"></td>
                            <td colspan="1"><input type="text" placeholder="" class="abl-input" v-model="form.application.company"></td>
                            <td colspan="1"><input type="text" placeholder="" class="abl-input" v-model="form.application.company"></td>
                            <td colspan="1"><input type="text" placeholder="" class="abl-input" v-model="form.application.company"></td>
                            <td colspan="1"><input type="text" placeholder="" class="abl-input" v-model="form.application.company"></td>
                            <td colspan="1"><input type="text" placeholder="" class="abl-input" v-model="form.application.company"></td>
                            <td colspan="1"><input type="text" placeholder="" class="abl-input" v-model="form.application.company"></td>
                            <td colspan="1"><input type="text" placeholder="" class="abl-input" v-model="form.application.company"></td>
                            <td colspan="1"><input type="text" placeholder="" class="abl-input" v-model="form.application.company"></td>
                            <td colspan="1"><input type="text" placeholder="" class="abl-input" v-model="form.application.company"></td>
                            <td colspan="1"><input type="text" placeholder="" class="abl-input" v-model="form.application.company"></td>
                        </tr>
                        <tr>
                            <th class="s-h" colspan="1">5</th>
                            <td colspan="1"><input type="text" placeholder="" class="abl-input" v-model="form.application.company"></td>
                            <td colspan="1"><input type="text" placeholder="" class="abl-input" v-model="form.application.company"></td>
                            <td colspan="1"><input type="text" placeholder="" class="abl-input" v-model="form.application.company"></td>
                            <td colspan="1"><input type="text" placeholder="" class="abl-input" v-model="form.application.company"></td>
                            <td colspan="1"><input type="text" placeholder="" class="abl-input" v-model="form.application.company"></td>
                            <td colspan="1"><input type="text" placeholder="" class="abl-input" v-model="form.application.company"></td>
                            <td colspan="1"><input type="text" placeholder="" class="abl-input" v-model="form.application.company"></td>
                            <td colspan="1"><input type="text" placeholder="" class="abl-input" v-model="form.application.company"></td>
                            <td colspan="1"><input type="text" placeholder="" class="abl-input" v-model="form.application.company"></td>
                            <td colspan="1"><input type="text" placeholder="" class="abl-input" v-model="form.application.company"></td>
                            <td colspan="1"><input type="text" placeholder="" class="abl-input" v-model="form.application.company"></td>
                            <td colspan="1"><input type="text" placeholder="" class="abl-input" v-model="form.application.company"></td>
                            <td colspan="1"><input type="text" placeholder="" class="abl-input" v-model="form.application.company"></td>
                        </tr>
                        <tr>
                            <th class="s-h" colspan="1">6</th>
                            <td colspan="1"><input type="text" placeholder="" class="abl-input" v-model="form.application.company"></td>
                            <td colspan="1"><input type="text" placeholder="" class="abl-input" v-model="form.application.company"></td>
                            <td colspan="1"><input type="text" placeholder="" class="abl-input" v-model="form.application.company"></td>
                            <td colspan="1"><input type="text" placeholder="" class="abl-input" v-model="form.application.company"></td>
                            <td colspan="1"><input type="text" placeholder="" class="abl-input" v-model="form.application.company"></td>
                            <td colspan="1"><input type="text" placeholder="" class="abl-input" v-model="form.application.company"></td>
                            <td colspan="1"><input type="text" placeholder="" class="abl-input" v-model="form.application.company"></td>
                            <td colspan="1"><input type="text" placeholder="" class="abl-input" v-model="form.application.company"></td>
                            <td colspan="1"><input type="text" placeholder="" class="abl-input" v-model="form.application.company"></td>
                            <td colspan="1"><input type="text" placeholder="" class="abl-input" v-model="form.application.company"></td>
                            <td colspan="1"><input type="text" placeholder="" class="abl-input" v-model="form.application.company"></td>
                            <td colspan="1"><input type="text" placeholder="" class="abl-input" v-model="form.application.company"></td>
                            <td colspan="1"><input type="text" placeholder="" class="abl-input" v-model="form.application.company"></td>
                        </tr>
                        <tr>
                            <th class="s-h" colspan="1">7</th>
                            <td colspan="1"><input type="text" placeholder="" class="abl-input" v-model="form.application.company"></td>
                            <td colspan="1"><input type="text" placeholder="" class="abl-input" v-model="form.application.company"></td>
                            <td colspan="1"><input type="text" placeholder="" class="abl-input" v-model="form.application.company"></td>
                            <td colspan="1"><input type="text" placeholder="" class="abl-input" v-model="form.application.company"></td>
                            <td colspan="1"><input type="text" placeholder="" class="abl-input" v-model="form.application.company"></td>
                            <td colspan="1"><input type="text" placeholder="" class="abl-input" v-model="form.application.company"></td>
                            <td colspan="1"><input type="text" placeholder="" class="abl-input" v-model="form.application.company"></td>
                            <td colspan="1"><input type="text" placeholder="" class="abl-input" v-model="form.application.company"></td>
                            <td colspan="1"><input type="text" placeholder="" class="abl-input" v-model="form.application.company"></td>
                            <td colspan="1"><input type="text" placeholder="" class="abl-input" v-model="form.application.company"></td>
                            <td colspan="1"><input type="text" placeholder="" class="abl-input" v-model="form.application.company"></td>
                            <td colspan="1"><input type="text" placeholder="" class="abl-input" v-model="form.application.company"></td>
                            <td colspan="1"><input type="text" placeholder="" class="abl-input" v-model="form.application.company"></td>
                        </tr>
                        <tr>
                            <th class="s-h" colspan="1">8</th>
                            <td colspan="1"><input type="text" placeholder="" class="abl-input" v-model="form.application.company"></td>
                            <td colspan="1"><input type="text" placeholder="" class="abl-input" v-model="form.application.company"></td>
                            <td colspan="1"><input type="text" placeholder="" class="abl-input" v-model="form.application.company"></td>
                            <td colspan="1"><input type="text" placeholder="" class="abl-input" v-model="form.application.company"></td>
                            <td colspan="1"><input type="text" placeholder="" class="abl-input" v-model="form.application.company"></td>
                            <td colspan="1"><input type="text" placeholder="" class="abl-input" v-model="form.application.company"></td>
                            <td colspan="1"><input type="text" placeholder="" class="abl-input" v-model="form.application.company"></td>
                            <td colspan="1"><input type="text" placeholder="" class="abl-input" v-model="form.application.company"></td>
                            <td colspan="1"><input type="text" placeholder="" class="abl-input" v-model="form.application.company"></td>
                            <td colspan="1"><input type="text" placeholder="" class="abl-input" v-model="form.application.company"></td>
                            <td colspan="1"><input type="text" placeholder="" class="abl-input" v-model="form.application.company"></td>
                            <td colspan="1"><input type="text" placeholder="" class="abl-input" v-model="form.application.company"></td>
                            <td colspan="1"><input type="text" placeholder="" class="abl-input" v-model="form.application.company"></td>
                        </tr>
                        <tr>
                            <th class="s-h" colspan="1">9</th>
                            <td colspan="1"><input type="text" placeholder="" class="abl-input" v-model="form.application.company"></td>
                            <td colspan="1"><input type="text" placeholder="" class="abl-input" v-model="form.application.company"></td>
                            <td colspan="1"><input type="text" placeholder="" class="abl-input" v-model="form.application.company"></td>
                            <td colspan="1"><input type="text" placeholder="" class="abl-input" v-model="form.application.company"></td>
                            <td colspan="1"><input type="text" placeholder="" class="abl-input" v-model="form.application.company"></td>
                            <td colspan="1"><input type="text" placeholder="" class="abl-input" v-model="form.application.company"></td>
                            <td colspan="1"><input type="text" placeholder="" class="abl-input" v-model="form.application.company"></td>
                            <td colspan="1"><input type="text" placeholder="" class="abl-input" v-model="form.application.company"></td>
                            <td colspan="1"><input type="text" placeholder="" class="abl-input" v-model="form.application.company"></td>
                            <td colspan="1"><input type="text" placeholder="" class="abl-input" v-model="form.application.company"></td>
                            <td colspan="1"><input type="text" placeholder="" class="abl-input" v-model="form.application.company"></td>
                            <td colspan="1"><input type="text" placeholder="" class="abl-input" v-model="form.application.company"></td>
                            <td colspan="1"><input type="text" placeholder="" class="abl-input" v-model="form.application.company"></td>
                        </tr>
                    </table>
                    <div class="abl-doc-title-sub">
                        <div class="title-text">
                            3. 증적 제출<br>
                            [임직원 자체 보안진단 항목]<br>
                            (1.2.1) 매체제어 프로그램 설치 여부 점검(e나라도움운영망, 사이버안전센터망)

                        </div>
                    </div>
                    <table class="abl-table">
                        <tr>
                            <td>
                                <abl-textarea  v-model="form.project.k_images" height="300px" />
                            </td>
                        </tr>
                    </table>
                </abl-document>
            </div>
        </div>
<!--        <input type="file" ref="fileinput" accept=".png,.jpg,.jpeg" class="fileinput" @change="onFileChangeHandler($event)"/>-->
    </div>
</template>

<script>
import AblTextarea from '@/components/AblTextarea'
import AblDocument from '@/components/AblDocument'
export default {
    props: ['pack'],
    components: {AblDocument,AblTextarea},
    methods: {
        async saveProject () {
            // validate
            let id = this.form.project.id
            if (id) await this.$http.put('projects', this.form.project)
            else await this.$http.post('projects', this.form.project)
        },

        previewHandler (idx, blob) {
            this.previews[idx] = blob
        },
        setPage (idx) {
            this.updateThumb(this.active)
            this.active = parseInt(idx, 10)
        },

        addProgress () {
            this.form.progress.push({
                number: 0,
                subject: '',
                student_name: '',
                start_date: '',
                end_date: '',
                contents: '',
                personal_opinion: '',
                expert_opinion: '',
                professor_opinion: '',
                fk_app_id: 0
            })

            let idx = (this.form.progress.length + 2)

            this.$nextTick(async () => {
                // console.log(await this.capture(idx))
                this.previews.push({id: Date.now(), data: await this.capture(idx)})
            })
        },
        
        // 썸네일 관련
        async updateThumb (id) {
            if (!this.previews[id]) return null
            this.previews[id].data = await this.capture(id)
            this.previews[id].id = Date.now()
            return true
        },
        async capture (id) {
            if (id > 2) {
                let sq = id - 3
                if (this.$refs['logs'][sq] && this.$refs['logs'][sq].capture) {
                    let blob = await this.$refs['logs'][sq].capture()
                    return blob
                }
            }
            else if (this.$refs[id] && this.$refs[id].capture) {
                let blob = await this.$refs[id].capture()
                return blob
            }
            else return null
        },

        // 편집 기능
        selectImg () {
            this.$refs.fileinput.click()
        },
        async onFileChangeHandler (evt) {
            if (evt.target && evt.target.files && evt.target.files[0]) {
                let data = await this.toDataUrl(evt.target.files[0])
                this.insertImage(data)
            }
            else return null
        },
        insertImage (path) {
            document.execCommand('InsertHtml', false, `<img class="attch-img" src="${path}">`)
        },
        toDataUrl (file) {
            return new Promise((resolve, reject) => {
                try {
                    const rd = new FileReader()
                    rd.onload = (e) => {
                        resolve(e.target.result)
                    }
                    rd.readAsDataURL(file)
                }
                catch (e) {
                    reject(e)
                }
            })
        },

        // 분류
        async getCategory () {
            this.category.options[this.category.depth].loading = true
            let filters = [{name: 'depth', op: 'eq', val: this.category.depth}]
            if (this.category.depth !== 0) {
                filters.push({name: 'parent_id', op: 'eq', val: this.category.options[this.category.depth - 1].value.id})
            }
            let q = JSON.stringify({filters})
            let params = {q}
            let {data} = await this.$http.get('category', {params})
            this.category.options[this.category.depth].list = data.objects
            this.category.options[this.category.depth].loading = false

            if (this.category.depth === 0) {
                this.category.options[0].value = data.objects[0]
                this.cg1ChangeHandler(data.objects[0])
            }
        },
        cg1ChangeHandler () {
            this.category.depth = 1
            this.category.options[1].list = []
            this.category.options[1].value = null
            this.category.options[2].list = []
            this.category.options[2].value = null
            this.getCategory()
        },
        cg2ChangeHandler () {
            this.category.depth = 2
            this.category.options[2].list = []
            this.category.options[2].value = null
            this.getCategory()
        },

        // 페이지 초기화
        async initialize () {
            this.getCategory()
            this.previews.push({id: Date.now(), data: await this.capture('0')})
            this.previews.push({id: Date.now(), data: await this.capture('1')})
            this.previews.push({id: Date.now(), data: await this.capture('2')})

            if (this.form.progress.length) {
                for (let i=0; i<this.form.progress.length; i++) {
                    this.previews.push({id: Date.now(), data: await this.capture(i + 3)})
                }
            }
        },
        async search_data () {
            try {
                let q = JSON.stringify({filters: [
                        {name: 'dept_code', op: 'eq', val: '001'}
                    ]})
                let params = {
                    page: 1,
                    results_per_page: 1,
                    q: q
                }
                let resp = await this.$http.get('cyber_report', {params})
                // console.log("cyber_report :" + JSON.stringify(resp))
                this.report_objs = resp.data.objects[0]
                this.self_diagnosis_data = JSON.parse(this.report_objs.self_diagnosis_data)
                console.log("self_diagnosis_data :" + JSON.stringify(this.self_diagnosis_data.dept_total_count))
            }
            catch (ex) {
                alert('search_data exception!!')
            }

        }
    },
    created () {
    },
    mounted () {
        this.search_data()
    },
    data () {
        return {
            previews: [],
            active: 0,

            category: {
                depth: 0,
                options: [
                    {list: [], loading: false, value: null},
                    {list: [], loading: false, value: null},
                    {list: [], loading: false, value: null}
                ]
            },
            report_objs :{},
            self_diagnosis_data:{},
            form: {
                application: {
                    id: null,
                    created: null, // 생성시간
                    updated: null, // 정보 수정시간
                    
                    // 신청자정보
                    name: '', // 이름
                    student_id: '', // 학번
                    major: '', // 전공
                    training_period: '', // 실습기간
                    
                    // 실습기업현황
                    company: '', // 기업명
                    ceo: '', // 대표자명
                    product: '', // 주요생산품
                    biz_category: '', // 업태/종목
                    subject: '', // ABL 주제
                    contents: '' // 현장실습 주요내용
                },
                project: {
                    id: null,
                    created: null,  // 생성시간
                    updated: null,  // 정보 수정시간

                    // 기술경영현장 문제해결 기본과정 기획서
                    name: '',  // 프로젝트명
                    professor: ['', '', '', ''],  // 지도교수
                    participants: '',  // 참여자

                    // 프로젝트 배경
                    issue: '',  // 이슈/문제점
                    needs: '',  // 프로젝트 Needs
                    purpose: '',  // 프로젝트 목적 & 목표
                    scope: '',  // 프로젝트 범위
                    plan1: '',  // 프로젝트 계획1
                    plan2: '',  // 프로젝트 계획2
                    plan3: '',  // 프로젝트 계획3
                    after_project: '',  // 후속 프로젝트 예상
                    benefit: ''  // 기대효과
                },
                progress: []
            }
        }
    }
}
</script>

<style lang="scss">
.attch-img {
    width: 140px;
    display: block;
    float: left;
    margin: 10px;
}
</style>

<style lang="scss" scoped>
$control-width: 200px;
.abl-page {
    position: absolute;
    left: -2000px; top: -2000px;

    &.active {
        position: relative;
        left: auto; top: auto;
    }
}

.report-cont {
    height: 100vh;
    margin: -12px;
    overflow-y: auto;

    .report-inner {
        padding: 12px 10px;
    }

    &::-webkit-scrollbar { width: 2px; }
    &::-webkit-scrollbar-thumb { background-color: rgba(0,0,0,0.2); }
}

.control-cont {
    width: $control-width; height: 1px;
    padding: 5px 8px; margin-right: 15px;
    border-radius: 3px;
    user-select: none;
    position: relative;

    .control-inner {
        position: absolute;
    }

    .abl-divider {
        margin-top: 20px;
        font-size: 12px;
    }

    .category-select {
        width: $control-width;
    }
}

.preview-cont {
    min-width: 142px;
    padding: 5px 8px; margin-left: 20px;
    background-color: #494949;
    border-radius: 3px;
    user-select: none;

    max-height: calc(100vh - 24px);
    overflow-y: auto;

    &::-webkit-scrollbar { width: 2px; }
    &::-webkit-scrollbar-thumb { background-color: white; }

    .preview-item {
        position: relative;
        border: 3px solid transparent;
        margin: 5px 0;
        cursor: pointer;

        &.active {
            border-color: #00ffe8;
            .preview { opacity: 1; }
        }

        &:hover {
            border-color: #1d9187;
        }

        .preview-seq {
            position: absolute;
            top: 0; left: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            width: 28px; height: 28px;
            background-color: white;
            z-index: 5;
        }

        .preview {
            width: 120px;
            display: block;
            background-color: #d2d2d2;
            min-height: 160px;
            opacity: 0.6;
        }
    }
}

.fileinput {
    position: fixed;
    top: -1000px; left: 0;
}
</style>
