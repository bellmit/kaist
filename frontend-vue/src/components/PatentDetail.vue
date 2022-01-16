<template>
  <div>
    <v-card :loading="loading" :disabled="loading">
      <v-card-text>
      <abl-document class="abl-page"  :key="patent_obj.patent_code" ref="report">
        <div class="abl-doc-title">
          <div class="title-text">한국 생산기술 연구원 특허</div>
        </div>
        <div class="abl-doc-body">
<!--          <table class="abl-table-empty">-->
<!--            <colgroup>-->
<!--              <col style="width:8.33%"/>-->
<!--              <col style="width:8.33%"/>-->
<!--              <col style="width:8.33%"/>-->
<!--              <col style="width:8.33%"/>-->
<!--              <col style="width:8.33%"/>-->
<!--              <col style="width:8.33%"/>-->
<!--              <col style="width:8.33%"/>-->
<!--              <col style="width:8.33%"/>-->
<!--              <col style="width:8.33%"/>-->
<!--              <col style="width:8.33%"/>-->
<!--              <col style="width:8.33%"/>-->
<!--              <col style="width:8.33%"/>-->
<!--            </colgroup>-->
<!--            <tr>-->
<!--              <th class="s-t-blank" colspan="2"><div class="d-flex"><div>1.</div><div class="t1">출원번호</div><div class="pr-3">:</div></div></th>-->
<!--              <td colspan="4"><input type="text" placeholder="출원번호" class="abl-input" v-model="patent_obj.patent_code"></td>-->
<!--              <th class="s-t-blank" colspan="2"><div class="d-flex"><div>2.</div><div class="t1">출원인</div><div class="pr-3">:</div></div></th>-->
<!--              <td colspan="4"><input type="text" placeholder="출원인" class="abl-input" v-model="patent_obj.patent_person"></td>-->
<!--            </tr>-->
<!--            <tr>-->
<!--              <th class="s-t-blank" colspan="2"><div class="d-flex"><div>3.</div><div class="t1">특허제목</div><div class="pr-3">:</div></div></th>-->
<!--              <td colspan="8"><input type="text" placeholder="특허제목" class="abl-input" v-model="patent_obj.patent_title"></td>-->
<!--            </tr>-->
<!--          </table>-->
          <br>
          <table class="abl-table-ts">
            <colgroup>
              <col style="width:20%"/>
              <col style="width:30%"/>
              <col style="width:20%"/>
              <col style="width:30%"/>
            </colgroup>
            <tr>
            <tr>
              <th class="s-t-blank" colspan="1"><div class="d-flex"><div></div><div class="t1">출원번호</div><div class="pr-3">:</div></div></th>
              <td colspan="1"><input type="text" placeholder="출원번호..." class="abl-input" v-model="patent_obj.patent_code"></td>
              <th class="s-t-blank" colspan="1"><div class="d-flex"><div></div><div class="t1">출원인</div><div class="pr-3">:</div></div></th>
              <td colspan="1"><input type="text" placeholder="출원인..." class="abl-input" v-model="patent_obj.patent_person"></td>
            </tr>
            <tr>
              <th class="s-t-blank" colspan="1"><div class="d-flex"><div></div><div class="t1">특허제목</div><div class="pr-3">:</div></div></th>
              <td colspan="3"><input type="text" placeholder="특허제목" class="abl-input" v-model="patent_obj.patent_title"></td>
            </tr>
            <tr>
              <th colspan="1">기술분야</th>
              <td colspan="1" class="image-default-h">
                <v-select solo dense hide-details light
                          v-model="selected_tech_type"
                          :items="$constant.tech_types"
                          item-text="text"
                          item-value=""
                          placeholder="-"
                          class="s-size"
                >
                </v-select>
              </td>
              <th colspan="1">업데이트 일자</th>
              <td colspan="1"><span>{{patent_obj.patent_updated_date | moment('YYYY-MM-DD HH:mm:ss')}}</span></td>
            </tr>
<!--            <tr>-->
<!--              <th colspan="1">업데이트 일자</th>-->
<!--              <td colspan="1" class="image-default-h"><span></span></td>-->
<!--              <th colspan="1">출헌년도</th>-->
<!--              <td colspan="1"><span></span></td>-->
<!--            </tr>-->
          </table>
          <br>
          <table class="abl-table-ts">
            <colgroup>
            </colgroup>
            <tr>
              <th colspan="2">특허요약</th>
            </tr>
            <tr>
              <td colspan="2">
                <abl-textarea v-model="patent_obj.patent_summary" placeholder="특허요약입력..." height="100px" class="ta-align"/>
              </td>
            </tr>
            <tr>
              <th colspan="2">특허문서등록(PDF)</th>
            </tr>
            <tr style="height:40px">
              <td colspan="2">
                <v-row>
                  <v-col cols="12" sm="8">
                    <v-file-input
                        truncate-length="50"
                        v-model="pdf_file_input"
                        color="deep-purple accent-4"
                        :placeholder="patent_obj.patent_pdf_file_path"
                        :disabled="!$session.check_permission()"
                        class="f-size"
                    ></v-file-input>
                  </v-col>
<!--                  <v-col cols="12" sm="3">-->
<!--                    <v-btn-->
<!--                        color="light-blue darken-2"-->
<!--                        class="f-size m-top"-->
<!--                        tile-->
<!--                        dark-->
<!--                        depressed-->
<!--                        @click="pdf_upload_file()"-->
<!--                        v-show="$session.check_permission()"-->
<!--                    >-->
<!--                      특허문서업로드-->
<!--                    </v-btn>-->
<!--                  </v-col>-->
                </v-row>
              </td>
            </tr>
            <tr>
              <th colspan="2">마케팅자료등록</th>
            </tr>
            <tr style="height:40px">
              <td colspan="2">
                <v-row>
                  <v-col cols="12" sm="8">
                    <v-file-input
                        truncate-length="50"
                        v-model="market_file_input"
                        color="deep-purple accent-4"
                        :placeholder="patent_obj.patent_maketting_file_path"
                        :disabled="!$session.check_permission()"
                        class="f-size"
                    ></v-file-input>
                  </v-col>
                </v-row>
              </td>
            </tr>
            <tr>
              <th colspan="2">특허 섭네일 이미지추가</th>
            </tr>
            <tr style="height:40px">
              <td colspan="2">
                <v-row>
                  <v-col cols="12" sm="8">
                    <v-file-input
                        truncate-length="50"
                        v-model="thumb_file_input"
                        color="deep-purple accent-4"
                        :placeholder="patent_obj.patent_thumb_image_path"
                        :disabled="!$session.check_permission()"
                        class="f-size"
                    ></v-file-input>
                  </v-col>
                </v-row>
              </td>
            </tr>
          </table>
          <v-row>
            <v-col class="ta-align-center">
              <v-btn
                  color="light-blue darken-2"
                  class="f-size m-top "
                  tile
                  dark
                  depressed
                  @click="add_patent()"
                  v-show="$session.check_permission()"
              >
                {{(patent == null)? "특허 등록":"특허 수정"}}
              </v-btn>
            </v-col>
          </v-row>
          <br>
        </div>
      </abl-document>
      </v-card-text>
    </v-card>
  </div>
</template>

<script>
import AblDocument from '@/components/AblDocument'
import AblTextarea from '@/components/AblTextarea'
import axios from 'axios'
import moment from 'moment'
export default {
  props: {
    patent: { type: Object, required: true }
  },
  components: {AblDocument, AblTextarea},
  methods: {
    async attach_download(attach_filename) {
      var url = '/api/monitor/v1/upload_file/' + attach_filename
      axios({
        method: 'get',
        url: url,
        // url: 'search_result.xlsx',
        responseType: 'blob'
      })
          .then(response => {
            const url = window.URL.createObjectURL(new Blob([response.data], {
              type: 'application/vnd.ms-excel'
            }))
            const link = document.createElement('a')
            link.href = url
            link.setAttribute('download', attach_filename) // or any other extension
            document.body.appendChild(link)
            link.click()
          })
          .catch(() => console.log('error occured'))
    },
    // async upload_file(){
    //   if(this.file_input != '' && this.file_input != null) {
    //     let params = {}
    //     const fd = new FormData()
    //     fd.append('file', this.file_input)
    //     let {data} = await this.$http.post('upload_file', fd)
    //     if (!data || !data.result || !data.filename)
    //       return alert("자료 업로드 실패!!")
    //     let today = moment().format('YYYY-MM-DD HH:mm:ss')
    //     params.maketting_file_path = data.filename
    //     params.updated_date = today
    //     await this.$http.patch(`sources/${this.patent.id}`, params)
    //     this.$session.$emit('modal-alert', '자료가 업로드 되었습니다.')
    //     this.$emit('callBackEvent', 'upload')
    //   }
    // },

    async upload_file(file_input,api_msg){
      if(file_input != '' && file_input != null) {
        const fd = new FormData()
        fd.append('file', file_input)
        let {data} = await this.$http.post(api_msg, fd)
        if (!data || !data.result || !data.filename)
          return alert("자료 업로드 실패!!")
        return data.filename
      }
    },
    makePagentDesc(obj){
      var data1 = obj.patent_code.substr(0,2)
      var data2 = ''
      if(data1 == "10")
        data2 = "KR" + obj.patent_code.substr(2,obj.patent_code.length-2) + "A"
      else if(data1 == "20")
        data2 = "KR" + obj.patent_code.substr(2,obj.patent_code.length-2) + "U"
      var data3 = '"' + data2 +'","' + obj.patent_title + '","' + obj.patent_summary + '"'
      return data3
    },
    async add_patent(){

      if (this.patent_obj.patent_code == 0){
        this.$session.$emit('modal-alert','출원번호를 입력하여 주세요!')
        return
      }
      if (this.patent_obj.patent_person == 0){
        this.$session.$emit('modal-alert','출원인를 입력하여 주세요!')
        return
      }
      if (this.patent_obj.patent_title == 0){
        this.$session.$emit('modal-alert','특허제목 입력하여 주세요!')
        return
      }
      if (this.patent_obj.patent_summary == 0){
        this.$session.$emit('modal-alert','특허요약을 입력하여 주세요!')
        return
      }
      if(this.pdf_file_input != null)
        await this.upload_file(this.pdf_file_input,"pdf_upload")
      if(this.thumb_file_input != null)
        await this.upload_file(this.thumb_file_input,"thumb_upload")
      if(this.market_file_input != null) {
        this.patent_obj.patent_maketting_file_path = await this.upload_file(this.market_file_input, "upload_file")
      }
      let params = {}

      params.person = this.patent_obj.patent_person;
      params.description = this.makePagentDesc(this.patent_obj);
      params.tech_type = this.$constant.tech_types.find(v=>v.text == this.selected_tech_type).value;
      params.apply_date = this.patent_obj.patent_code.substr(2,4);
      params.maketting_file_path = this.patent_obj.patent_maketting_file_path;
      let today = moment().format('YYYY-MM-DD HH:mm:ss')
      params.updated_date = today
      if(this.patent == null){
        params.patent_code = this.patent_obj.patent_code;
        await this.$http.post(`sources`, params)
      }else{
        // alert(JSON.stringify(params))
        await this.$http.patch(`sources/${this.patent_obj.patent_id}`, params)
      }
      this.$emit('callBackEvent', 'add')
    },
    async get_patent_data(id){
      let {data} = await this.$http.get(`sources/${id}`)
      this.patent_obj.patent_id = id
      this.patent_obj.patent_code = data.patent_code
      this.patent_obj.patent_title = this.$getPatentTitle(data.description)
      this.patent_obj.patent_summary = this.$getPatentSummary(data.description)
      this.patent_obj.patent_person = data.person
      this.patent_obj.patent_updated_date = data.updated_date
      this.patent_obj.patent_maketting_file_path = data.patent_maketting_file_path
      this.patent_obj.patent_thumb_image_path = data.patent_thumb_image_path
      this.patent_obj.patent_pdf_file_path = data.patent_pdf_file_path
      this.patent_obj.apply_date = data.apply_date
      this.patent_obj.tech_type = data.tech_type
      this.selected_tech_type = this.$constant.tech_types.find(v=>v.value == data.tech_type).text
    },
    // onChangeTechType(selected_tech_type){
    //   this.selected_tech_type = this.$constant.tech_types[selected_tech_type]
    // }

  },
  mounted () {
    this.selected_tech_type = this.$constant.tech_types[5].value
    if(this.patent != null ){
      this.get_patent_data(this.patent.id)
    }
  },
  data () {
    return {
      preview: null,
      loading: false, 
      school: {},
      refresh_id:0,
      s3_data_json:null,
      deleteDialog:{
        show: false,
        delItem:''
      },
      market_file_input:null,
      file_path:null,
      file_name: '파일을 선택해 주세요',
      pdf_file_input:null,
      pdf_file_path:null,
      pdf_file_name: '파일을 선택해 주세요',
      thumb_file_input:null,
      thumb_file_path:null,
      thumb_file_name: '파일을 선택해 주세요',
      selected_tech_type:null,
      previews:[],
      pdf_save_flag:false,
      pdfDialog:{
        show:false
      },
      member_area_type:[
        {text:'서울강원',value:'R001',code:'A002'},
        {text:'경기인천',value:'R002',code:'A003'},
        {text:'대전충청',value:'R003',code:'A004'},
        {text:'대구경북',value:'R004',code:'A005'},
        {text:'부산경남',value:'R005',code:'A006'},
        {text:'호남제주',value:'R006',code:'A007'},
      ],
      patent_obj:{
        patent_id:-1,
        patent_code:'',
        patent_title:'',
        patent_summary:'',
        patent_updated_date:'',
        patent_thumb_image_path:'',
        patent_name:'',
        patent_maketting_file_path:'',
        patent_tech_type:null,
        patent_person:'',
        patent_pdf_file_path:''
      }
    }
  }
}
</script>

<style lang="scss" scoped>
.t1 {
  text-align: justify;
  text-align-last: justify;
  flex: 1 0 auto;
  padding: 0 10px;
}
.abl-page {
  padding: 15px 30px;
}
.school-file-upload {
  position: relative;
  top: 0px; left: 10px;
  z-index: 10;
}
.school-save {
  position: relative;
  top: -10px; left:15px;
  z-index: 10;
}
.report-download {
  position: relative;
  top: -10px; left:780px;
  z-index: 10;
}
.image-left-m{
  overflow: hidden;
  text-align: center;
  display: block;
  margin-left: auto;
  margin-right: auto;
}
.td-bold{
  background-color: #e7e7e7;
}
.image-default-h{
  height:26px !important;
  text-align: center;
}
.f-pos{
  position: fixed;
  top: -1000px; left: 0;
}
.abl-doc-body{
  width: 740px;
}
.abl-page{
  width: 800px;
}
th {
  text-align: center;
}
.s-size{
  margin: 5px 5px;
  font-size: 12px;
}
.f-size {
  font-size: 12px;
}
.m-top{
  margin-top: 20px;
}
.ta-align{
  text-align: left;
  font-size: 12px;
}
.ta-align-center{
  text-align: center;
}

</style>