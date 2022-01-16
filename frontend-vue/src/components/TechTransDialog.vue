<template>
  <div>
    <v-card>
      <CCard :key="this.techtrans_data">
        <CCardHeader>
          기술이전문의 등록
        </CCardHeader>
        <CCardBody>
          <CForm>
            <CInput prepend="기 업 명" v-model="dialog.company_name">
              <template #append-content><CIcon name="cil-settings"/></template>
            </CInput>
<!--            <CInput prepend="사업자번호" v-model="dialog.bussiness_num">-->
<!--              <template #append-content><CIcon name="cil-settings"/></template>-->
<!--            </CInput>-->
            <CInput prepend="요청자이름" v-model="dialog.request_name">
              <template #append-content><CIcon name="cil-user"/></template>
            </CInput>
            <CInput prepend="연 락 처" v-model="dialog.request_phone">
              <template #append-content><CIcon name="cil-settings"/></template>
            </CInput>
            <CInput type="email" autocomplete="email" prepend="이  메  일" v-model="dialog.request_email">
              <template #append-content><CIcon name="cil-envelope-closed"/></template>
            </CInput>
            <CInput prepend="출원번호" v-model="dialog.patent_code">
              <template #append-content><CIcon name="cil-settings"/></template>
            </CInput>
            <v-row>
              <v-col cols="3">
                실시유형
              </v-col>

              <v-col cols="9">
                <v-select solo dense hide-details light
                          v-model="dialog.selected_trans_type"
                          :items="trans_type"
                          placeholder="-"
                          class="s-size"
                          @change="onChangeTransType(dialog.selected_trans_type)"
                >
                </v-select>
             </v-col>
            </v-row>


<!--            <CSelect-->
<!--                v-model="dialog.selected_trans_type"-->
<!--                label="실시유형"-->
<!--                horizontal-->
<!--                :options="trans_type"-->
<!--                placeholder="Please select"-->
<!--            />-->
            <CTextarea
                label="요청사항"
                placeholder="기술이전요청내용 입력..."
                horizontal
                rows="5"
                v-model="dialog.request_contents"
            />
            <v-row v-if="dialog.current_job=='MODIFY'">
              <v-col cols="3">
                처리결과
              </v-col>

              <v-col cols="9">
                <v-select solo dense hide-details light
                          v-model="dialog.selected_result_type"
                          :items="result_type"
                          placeholder="-"
                          class="s-size"
                          @change="onChangeResultType(dialog.selected_result_type)"
                >
                </v-select>
              </v-col>
            </v-row>
            <br>
            <div class="form-group form-actions pos-center">
              <CButton type="submit" @click="onSummit()" class="btn btn-no btn-primary">
                {{ getButtonName() }}
              </CButton>
              <CButton type="submit" @click="onClose()" class="btn btn-no btn-secondary left-m">
                닫기
              </CButton>
            </div>
            <CCard>
              <CCardHeader>
                <div><strong>기술이전담당자(융합, 청정, 서남, 전북, 강원, 제주)</strong></div>
                <div><strong>이름 : 박헌수 / 메일 : honsu@kitech.re.kr / 전화번호 : 041-589-8089</strong></div>
              </CCardHeader>
            </CCard>
            <CCard>
              <CCardHeader>
                <div><strong>기술이전담당자(뿌리, 대경, 동남, 울산)</strong></div>
                <div><strong>이름 : 송세헌 / 메일 : ssh@kitech.re.kr / 전화번호 : 041-589-8062</strong></div>
              </CCardHeader>
            </CCard>
<!--            <CWidgetIcon-->
<!--                header="기술이전담당자(융합, 청정, 서남, 전북, 강원, 제주)"-->
<!--                text="이름 : 박헌수 / 메일 : honsu@kitech.re.kr / 전화번호 : 041-589-8089"-->
<!--                color="gradient-secondary"-->
<!--            >-->
<!--              <CIcon name="cil-user" width="24"/>-->
<!--            </CWidgetIcon>-->
<!--            <CWidgetIcon-->
<!--                header="기술이전담당자(뿌리, 대경, 동남, 울산)"-->
<!--                text="이름 : 송세헌 / 메일 : ssh@kitech.re.kr / 전화번호 : 041-589-8062"-->
<!--                color="gradient-secondary"-->
<!--            >-->
<!--              <CIcon name="cil-user" width="24"/>-->
<!--            </CWidgetIcon>-->
          </CForm>
        </CCardBody>
      </CCard>
    </v-card>
  </div>
</template>

<script>
import axios from 'axios'
import moment from 'moment'
export default {
  props: {
    techtrans_data: { type: Object, required: false },
    patent_data: { type: Object, required: false },
  },
  methods: {
    onClose(){
      this.$emit('callBackTechTrans', 'close')
    },
    async onSummit(){
      if (this.dialog.company_name.length == 0){
        this.$session.$emit('modal-alert','회사명을 입력하여 주세요!')
        return
      }
      // if (this.dialog.bussiness_num.length == 0){
      //   this.$session.$emit('modal-alert','사업자번호를 입력하여 주세요!')
      //   return
      // }
      if (this.dialog.request_name.length == 0){
        this.$session.$emit('modal-alert','이름을 입력하여 주세요!')
        return
      }
      if (this.dialog.request_phone.length == 0){
        this.$session.$emit('modal-alert','전화번호를 입력하여 주세요!')
        return
      }
      if (this.dialog.request_email.length == 0){
        this.$session.$emit('modal-alert',' 이메일을 입력하여 주세요!')
        return
      }
      if (this.dialog.request_contents.length == 0){
        this.$session.$emit('modal-alert',' 요청내용을 입력하여 주세요!')
        return
      }
      let params = {}
      params.company_name = this.dialog.company_name;
      params.bussiness_num = '';
      params.request_name = this.dialog.request_name;
      params.request_phone = this.dialog.request_phone;
      params.request_email = this.dialog.request_email;
      params.request_contents = this.dialog.request_contents;
      params.techtrans_type = this.dialog.techtrans_type;
      params.patent_code = this.dialog.patent_code;
      let today = moment().format('YYYY-MM-DD HH:mm:ss')
      if(this.dialog.current_job == 'MODIFY'){
        params.updated_date = today
        params.techtrans_result = this.dialog.techtrans_result;
        await this.$http.patch(`techtrans/${this.dialog.id}`, params)
      }else{
        params.created_date = today
        params.updated_date = today
        await this.$http.post(`techtrans`, params)
      }
      this.$emit('callBackTechTrans', 'add')
    },
    onChangeTransType(selected_trans_type){
      this.dialog.techtrans_type=selected_trans_type
    },
    getButtonName(){
      if(this.dialog.current_job == 'MODIFY'){
        return "수정"
      }
      return "등록"
    },
    onChangeResultType(selected_result_type){
      this.dialog.techtrans_result=selected_result_type
    },
  },
  mounted () {
    this.dialog.selected_trans_type = this.trans_type[0]
    if(this.techtrans_data != null){
      Object.assign(this.dialog,this.techtrans_data)
      this.dialog.selected_trans_type = this.trans_type[this.dialog.techtrans_type]
      this.dialog.selected_result_type = this.result_type[this.dialog.techtrans_result]
      this.dialog.current_job = "MODIFY"
    }
    if(this.patent_data != null){
      // this.dialog.patent_code = this.$makePatentCode(this.patent_data.patent_code)
      this.dialog.patent_code = this.patent_data.patent_code
    }

  },
  data () {
    return {
      dialog:{
        show:false,
        id:'',
        // company_name:'',
        // bussiness_num:'',
        // request_name:'',
        // request_phone:'',
        // request_email:'',
        // techtrans_type:null,
        // request_contents:'',
        // techtrans_result:null,
        patent_code:'',
        company_name:'',
        bussiness_num:'',
        request_name:'',
        request_phone:'',
        request_email:'',
        techtrans_type:null,
        request_contents:'',
        techtrans_result:null,
        canModify:false,
        current_job:'',
        selected_trans_type:null,
        selected_result_type:null,
      },
      trans_type:[
        {text:'통상',value:0},
        {text:'전용',value:1},
        {text:'독점적통상',value:2},
        {text:'매각(유상)',value:3},
        {text:'매각(무상)',value:4},
        {text:'기술출자',value:5},
        {text:'기부채납',value:6},
        {text:'기타(M&A)',value:7},
      ],
      result_type:[
        {text:'미처리',value:0},
        {text:'대기',value:1},
        {text:'처리완료',value:2},
      ],
    }
  }
}
</script>

<style lang="scss" scoped>
.pos-center{
  text-align: center;
}
.left-m{
  margin-left: 10px;
}
</style>