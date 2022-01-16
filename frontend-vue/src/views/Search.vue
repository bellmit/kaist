<template>
  <div>
    <v-app class="container-bg">
      <v-container fluid>
        <CCard class="search-header">
          <CCardBody>
            <div >
              <v-row   align="center" justify="center">
                <v-col class="search-header-left" cols="12" sm="12" md="2">
                  <v-select outlined dense hide-details
                            v-model="selected_tech"
                            :items="tech_types"
                            label="기술분야"
                            item-text="text"
                            item-value="value"
                            @change="onChangeTechTypes()"
                            class="bg-white"
                  />
                </v-col>
                <v-col cols="12" sm="12" md="2">
                  <v-select outlined dense hide-details
                            v-model="selected_year"
                            :items="years_type"
                            label="출원연도"
                            @change="onChangeYearsTypes()"
                            class="bg-white"
                  />
                </v-col>
                <v-col cols="12" sm="12" md="5">
                  <v-text-field outlined dense hide-details
                                placeholder="검색어를 입력하세요"
                                append-icon="mdi-magnify"
                                v-model="filter.querystring"
                                @keydown.enter="search()"
                                class="m-right bg-white"
                  />
                </v-col>
                <v-col cols="12" sm="12" md="1">
                  <v-btn depressed dark big
                         color="light-blue darken-2"
                         @click="search()"
                         class="m-left"
                          >
                    <v-icon small>mdi-magnify</v-icon>
                    <div class="ml-1">검색</div>
                  </v-btn>
                </v-col>
                <v-col cols="12" sm="12" md="1">
                  <v-btn depressed  dark big
                         color="deep-purple darken-4"
                         @click="openTechTrans(null)"
                         class="m-left"
                  >
                    <v-icon small>mdi-plus</v-icon>
                    <div class="ml-1">기술이전문의등록</div>
                  </v-btn>
                </v-col>
              </v-row>
            </div>
            <div >
              <v-row style="text-align: right">
                <v-col>
                  <span class="sw-label">{{(ai_use == true)? '인공지능(AI) 검색':'키워드 검색'}}</span>
                  <v-switch
                      style="margin-top: -4px"
                      class="float-right"
                      color="info"
                      v-model="ai_use"
                  />
                </v-col>
              </v-row>
            </div>
            <br>
            <br>
            <div>
              <template >
                <div class="search-title-top">
                  <v-chip big  label class="ml-1 v-chip-bg"> *검색에는 약 20초 정도 소요됩니다.</v-chip> <br>
                  <v-chip big  label class="ml-1 v-chip-bg"> *두 단어 이상 입력하면 정확도가 높아집니다.</v-chip> <br>
                </div>
              </template>
            </div>
          </CCardBody>

        </CCard>
        <div style="margin-left: 500px">
          <spinner   :status="table.loading" :color="spinnerColor" :size="100" :depth="10" :clockwise="spinnerClockwise" :speed="spinnerSpeed" />
        </div>
        <div class="d-flex">

          <div class="search-container mt-4">

            <template v-if="table.data.length == 0">
              <div class="search-title-top-2">
                <v-chip big  label class="ml-1 v-chip-bg"> 검색 결과가 없습니다.</v-chip> <br>
              </div>
            </template>
            <template v-else>
              <div class="text-center mt-1" v-if="table.data && table.data.length">

                <v-pagination
                    v-model="page.current"
                    :length="page.total"
                    @input="onPageChangeHandler()"
                    @next="onPageChangeHandler()"
                    @previous="onPageChangeHandler()"
                />
              </div>
              <br>
              <v-card flat tile color="grey lighten-4" class="mb-1" v-for="(item, idx) in table.data" :key="item.patent_code">
                <article>
                  <div class="search_section_title">
                    <div class="stitle">
                      <div class="lank-bg">
                        {{((page.current) * page.limit) + idx + 1 }}
                      </div>
                      <span >{{$getPatentTitle(item.description,60)}}</span>
                      <br>
                      <v-chip small  label class="ml-1 v-chip-bg">출원번호:{{ item.patent_code }}</v-chip>
                      <v-chip small  label class="ml-1 v-chip-bg">출원인:{{item.person}}</v-chip>
                      <v-chip small  label class="ml-1 v-chip-bg">주발명자:{{item.main_person}}</v-chip>
                      <v-chip small label class="ml-1">기술분야:{{$constant.tech_types.find(v=>v.value == item.tech_type).text}}</v-chip>
                      <v-chip small label class="ml-1 v-chip-bg">수정일자:{{item.updated_date}}</v-chip>
                    </div>
                    <div class="buttons-area-1">
                      <div class="btn_doc" v-if="check_item(item.maketting_file_path)">
                        <v-btn depressed dark small
                               color="light-blue darken-2"

                               @click="attach_download(item.maketting_file_path)">
                          <v-icon small>mdi-file-document</v-icon>
                          <div class="ml-1">마케팅자료</div>
                        </v-btn>
                      </div>
                    </div>
                    </div>
                    <div class="buttons-area-2">
                      <div class="btn_doc">
                        <v-btn depressed dark small
                               color="light-blue darken-2"
                               @click="onPdfDownload(item)">
                          <v-icon small>mdi-file-pdf-box</v-icon>
                          <div class="ml-1">PDF</div>
                        </v-btn>
                        <br>
  <!--                      <v-chip small  label class="ml-1 v-chip-bg v-chip-w">관련도:{{'100%'}}</v-chip>-->
                      </div>
                      <div class="btn_doc">
                        <v-btn depressed dark small
                               color="light-blue darken-2"
                               @click="openTechTrans(item)">
                          <v-icon small>mdi-graphql</v-icon>
                          <div class="ml-1">기술이전</div>
                        </v-btn>
                        <br>
                        <!--                      <v-chip small  label class="ml-1 v-chip-bg v-chip-w">관련도:{{'100%'}}</v-chip>-->
                      </div>
                  </div>
                  <div class="search_basic_info">
                    <div class="thumb">
                      <img :src="getThumImg(item)" width="100" height="100" @error="getDefaultThumImg()">
                    </div>
                    <div>
                      <div class="summary-size">
                        {{ $getPatentSummary(item.description,300) }}
                      </div>
                    </div>
                  </div>
                </article>
  <!--              <v-card-title class="pb-0">-->
  <!--                <div class="report-title">-->

  <!--                  <v-avatar color="blue-grey darken-2" size="36"><span class="white&#45;&#45;text">{{((page.current - 1) * page.limit) + idx + 1 }}</span></v-avatar>-->
  <!--                  <div class="ml-3 d-flex report-title-wrap">-->
  <!--                    <div class="report-title-text">-->
  <!--                      <div class="text-subtitle-1 m_focus" @click="onPatentDetailHandler(item)">{{$getPatentTitle(item.description)}}</div>-->
  <!--                      <div class="d-flex justify-space-between">-->
  <!--                        <div class="report-labels">-->

  <!--                          $getPatentNum-->
  <!--                          <v-chip small label>출헌번호:{{item.patent_code}}</v-chip>-->
  <!--                          <v-chip small label>출헌인:{{item.person}}</v-chip>-->
  <!--                          <v-chip small label class="ml-1">마케팅자료:{{item.maketting_file_path}}</v-chip>-->
  <!--                          <v-chip small label class="ml-1">수정일자:{{item.updated_date}}</v-chip>-->
  <!--                        </div>-->
  <!--                      </div>-->
  <!--                    </div>-->
  <!--                  </div>-->
  <!--                </div>-->
  <!--              </v-card-title>-->
  <!--              <v-divider/>-->
  <!--              <v-list-item three-line>-->
  <!--                <v-list-item-avatar tile size="80" color="#eeeeee">-->
  <!--                  <v-img :src="getThumImg('/api/v1/attachment/' + item.patent_code)" v-on:error="onImgError" />-->
  <!--                </v-list-item-avatar>-->
  <!--                <v-list-item-content>-->
  <!--                  <span class="text-body-2 grey&#45;&#45;text text&#45;&#45;darken-2">{{$getPatentSummary(item.description,100)}}</span>-->
  <!--                </v-list-item-content>-->
  <!--              </v-list-item>-->
              </v-card>
            </template>
          </div>
        </div>

        <v-dialog v-model="patentDetail.show" persistent max-width="840px">
          <v-card>
            <div class="school-detail-container">
              <v-btn fab x-small dark depressed color="grey darken-1" class="school-detail-close" @click="patentDetail.show=false">
                <v-icon>mdi-close</v-icon>
              </v-btn>
              <patent-detail @callBackEvent="onEmitEvent" :patent="patentDetail.data" />
            </div>
          </v-card>
        </v-dialog>
        <v-dialog v-model="techTrainsDlg.show" persistent max-width="600px" :key="dialog.refresh_id">
          <tech-trans-dialog :techtrans_data=null :patent_data="techTrainsDlg.patent" @callBackTechTrans="onEmitTechTrans"/>
        </v-dialog>
      </v-container>
    </v-app>
  </div>
</template>

<script>
import PatentDetail from '@/components/PatentDetail'
import TechTransDialog from '@/components/TechTransDialog'
import axios from 'axios'
import moment from 'moment'
import Spinner from 'vue-spinner-component/src/Spinner.vue'
export default {
  components: {PatentDetail,moment,TechTransDialog,Spinner},
  methods: {
    search(){

      if(this.filter.querystring.length < 1){
        this.$session.$emit('modal-alert','검색어를 입력해 주세요!')
        return true
      }
      this.page.current = 0
      this.search_query(this.filter.querystring)
    },
    async search_query(search_string) {
      // alert(JSON.stringify(this.selected_tech))
      // alert(JSON.stringify(this.selected_year))
      this.table.loading = true;

      let filters_and = []
      let filters_or = []

      if(this.selected_tech != -1){
        filters_and.push({name: 'tech_type', op: 'like', val: "%"+search_string+"%"})
      }
      if(this.selected_year != '전체'){
        filters_and.push({name: 'apply_date', op: 'like', val: "%"+search_string+"%"})
      }
      if (this.filter.querystring) {
        this.table.data = []
        filters_or.push({name: 'person', op: 'like', val: "%"+search_string+"%"})
        filters_or.push({name: 'patent_code', op: 'like', val: "%"+search_string+"%"})
        filters_or.push({name: 'description', op: 'like', val: "%"+search_string+"%"})
      }

      // let q = {
      //   filters: [{or:filters_or},{and:filters_and}],
      //   order_by: [{field: 'id', direction: 'asc'}]
      // };
      let params = {
        querystring:search_string,
        limit: this.page.limit,
        offset: this.page.current * this.page.limit,
        ai_use:(this.ai_use == true)? 1 :0,
        tech_type:this.selected_tech,
        apply_date:this.selected_year,
      };
      let { data } = await this.$http.get("kitech_ai_search", { params });
      this.table.loading = false;
      this.page.total = data.num_results/20
      if(this.page.total > 10)
        this.page.total = 10

      this.table.data = data.objects.map((v, i) => {
        v._index = data.num_results - i - (this.page.current - 1) * this.page.limit;
        return v;
      });
      // if(this.ai_use == true){
      //   let params = {
      //     querystring:search_string,
      //     limit: this.page.limit,
      //     offset: this.page.current * this.page.limit,
      //   };
      //   let { data } = await this.$http.get("kitech_ai_search", { params });
      //   this.page.total = data.num_results/20
      //   if(this.page.total > 10)
      //     this.page.total = 10
      //   this.table.loading = false;
      //   this.table.data = data.objects.map((v, i) => {
      //     v._index = data.num_results - i - (this.page.current - 1) * this.page.limit;
      //     return v;
      //   });
      // }else{
      //   let params = {
      //     q: JSON.stringify(q),
      //     page: this.page.current,
      //     results_per_page: this.page.limit,
      //   };
      //   let { data } = await this.$http.get("sources", { params });
      //   this.page.total = data.num_results/20
      //   if(this.page.total > 10)
      //     this.page.total = 10
      //   this.table.loading = false;
      //   this.table.data = data.objects.map((v, i) => {
      //     v._index = data.num_results - i - (this.page.current - 1) * this.page.limit;
      //     return v;
      //   });
      // }
    },
    onChangeTechTypes(){
    },
    onChangeYearsTypes(){
    },
    check_item(file_name){
      if(file_name != undefined && file_name != '' && file_name.length > 3)
        return true
      return false
    },
    async attach_download(attach_filename) {
      var url = '/api/v1/upload_file/' + attach_filename
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
    onEmitEvent(type){
      if(type == "upload"){
        this.search();
      }
    },
    getThumImg: function(item) {
      return this.$getWebURL() + '/api/v1/thumbnail/' + item.patent_code + '.jpg'
    },
    getDefaultThumImg: function() {
      return this.$getWebURL() + '/api/v1/thumbnail/default.png'
    },

    onImgError: function() {
      this.failed_image = false;
    },
    onPatentDetailHandler (item) {
      this.dialog.refresh_id += 1
      this.patentDetail.data = item
      this.patentDetail.show = true
    },
    openTechTrans(patent){
      this.dialog.refresh_id += 1
      this.techTrainsDlg.patent = patent
      this.techTrainsDlg.show = true
    },
    onEmitTechTrans(type){
      if(type == "add")
        this.$session.$emit('modal-alert','기술이전 등록 요청하였습니다.')
      this.techTrainsDlg.show = false
    },
    onPageChangeHandler () {
      this.search_query(this.filter.querystring)
    },
    async onPdfDownload(item){
      this.$pdfDownload(item.patent_code)
      let params = {}
      params.patent_code = item.patent_code
      params.rank = item._index
      params.search_string = this.filter.querystring
      params.user_id = 'admin'
      params.action_type = 1
      params.fk_users = 1
      params.create_date = moment().format('YYYY-MM-DD HH:mm:ss')
      await this.$http.post(`user_action`, params)
    }
  },
  mounted() {

    this.years_type.push('전체')
    this.tech_types.push({text:'전체',value:-1})
    this.tech_types = this.tech_types.concat(this.$constant.tech_types)
    this.years_type = this.years_type.concat(this.years)
    this.selected_tech = this.tech_types[0].value
    this.selected_year = this.years_type[0]
    this.filter.querystring = this.$session.getSearchString()
    if(this.filter.querystring.length >0){
      this.search()
    }
  },
  computed: {
    years () {
      const year = new Date().getFullYear()
      return Array.from({length: year - 1989}, (value, index) => year - index)
    }
  },
  watch: {
    "table.options": {
      handler() {
        this.search();
      },
      deep: true,
    },
  },
  data() {
    return {
      filter: {
        querystring: "",
      },
      table: {
        headers: [
          { text: "No.", value: "id", sortable: false, width: 40 },
          { text: "출원번호", value: "patent_code", sortable: false, width: 100 },
          { text: "출원인", value: "person", sortable: false,align: "center", width: 200 },
          { text: "제목", value: "patent_title", sortable: false,align: "center", width: 500 },
          { text: "마케팅자료", value: "maketting_file_path", sortable: false,align: "center" },
          { text: "수정일자", value: "updated_date", sortable: false,align: "center" }
        ],

        loading: false,
        total: 0,
        options: {},
        data: [],
      },
      selected_option:null,
      options_array : [
        {"option_name":"출원인","option_id":1},
        {"option_name":"출원번호","option_id":2},
        {"option_name":"요약내용","option_id":3},
      ],
      patentDetail: {
        show: false,
        data: null
      },
      dialog: {
        refresh_id :1,
        show: false,
        form: null
      },
      failed_image:false,
      page: {
        current: 0,
        limit: 20,
        total: 1
      },
      pdf_url:null,
      years_type:[],
      tech_types:[],
      selected_year:null,
      selected_tech:null,
      techTrainsDlg:{
        show:false,
        patent:null
      },
      ai_use:true,
    };
  },
};
</script>
<style scoped lang="scss">
.sr-card-app{
  height:350px;
}
.sr-card-app-title{
  height:160px;
}
.school-detail-container {
  position: relative;
}
.school-detail-close {
  position: absolute;
  top: 20px; right: 10px;
  z-index: 10;
}
.m-right{margin-right: 20px;}
.text-center{
  text-align: center;
}
td {
  text-align: center;
}
.m-left{margin-left: 10px;}
.container {
  max-width: 1200px;
  margin: 0 auto;
}
.bg-white{
  background-color: white;
}

.search_section_title {
  float:left;
  //clear: both;
  //margin-bottom: 0px;
  //padding: 0px 0 4px;
  //border-bottom: dotted 1px #d5d5d5;
  //letter-spacing: -1px;
  //line-height: 1.4;
  //overflow: hidden;
  //background: #dddddd;
  max-height: 70px;
  width:100%;
}
.search_section_title span.blue_box_small {/* 상태 box */
  color: #fff;
  font-size: 0.75em;
  font-weight: normal;
}
.stitle {
  //width: 625px;
  float:left;
  margin-left: 5px;
  color: #304c9b;
  font-size: 18px;
  line-height: 1.2;
  font-weight: bold;
  margin-top: 10px;
  width:70%;
  height: 50px;
  //border: 1px solid blue;
}
.stitle a {
  color: #304c9b;
}
.btn_doc {
  float:left;
  /*width: 75px;*/
  display: block;
  font-size: 0.9em;
  letter-spacing: -1px;
  font-family: '돋움', Dotum, sans-serif;
  //background-color: #0d47a1;
  width:30%;
  margin-top: 0px;
  margin-left: 10px;
}
.search_section_title .btn_doc span {
  display: block;
}

/* 썸네일, 검색식 영역 STYLE */
.search_basic_info {
  clear: both;
  display: inline-block;
  width: 100%;
  padding-bottom: 8px;
  border-bottom: solid 1px #e2e2e2;
  background-color: #eeeeee;
}
.search_basic_info:after {
  clear: both;
  display: block;
  width: 100%;
  content: "" ;
}
/* 썸네일 */
.thumb {
  float: left;
  width: 100px;
  height: 100px;
  margin-right: 10px;
  border: solid 1px #898989;
}
.thumb img {
  width: 100%;
  height: 100%;
}
/* 검색식 */
.search_info_list {
  display: inline-block;
  width: 635px;
  overflow: hidden;
}
.search_info_list li {
  float: left;
  height: 19px;
  margin: 0;
  padding: 0;
  border: none;
  color: #000;
  overflow: hidden;
  /* 글자가 넘어갈 경우 "..." 처리 By J.H.S 20130711*/
  text-overflow: ellipsis;
  white-space: nowrap;
}
.search_info_list li.left_width {
  width: 200px;
  margin-right: 10px;
  overflow: hidden;
}
.search_info_list li.right_width {
  width: 425px;
  overflow: hidden;
}
.search_info_list li.letter1 {
  letter-spacing: -1px;
}
ul {
  list-style-type: none;
  padding: 0;
}

li {
  display: inline-block;
  margin: 0 10px;
}

a {
  color: #42b983;
}
.pdf-btn-width{
  width:80px;
}
.v-chip-bg{
  background-color: #0d47a1;
  border-bottom: 1px solid #aaaaaa;
}
.lank-bg{
  float:left;
  background-color: #304c9b;
  color:white;
  width:30px;
  text-align: center;
  margin-right: 5px;
}

/* 썸네일, 검색식 영역 STYLE */
.search_section .search_basic_info {
  clear: both;
  display: inline-block;
  width: 100%;
  padding-bottom: 8px;
  border-bottom: solid 1px #e2e2e2;
}
.search_section .search_basic_info:after {
  clear: both;
  display: block;
  width: 100%;
  content: "" ;
}
/* 썸네일 */
.search_section .thumb {
  float: left;
  width: 100px;
  height: 100px;
  margin-right: 10px;
  border: solid 1px #898989;
}
.search_section .thumb img {
  width: 100%;
  height: 100%;
}
.cursor-title{
  cursor: pointer;
}
.summary-size{
  font-size: 14px;
}
.v-chip-w{
  width:80px;
  margin-left: -3px !important;
}
.btn-blue{
  color:#3E1F99;
}
.container-bg{
  background-color: #eeeeee;
  width: 1600px;
  position: center;
}
.search-title-top{
  font-size: 20px;
  margin-top: -80px;
}
.search-title-top-2{
  font-size: 20px;
}
.search-header{
  background-color: #E0E0E0;
  width: 100%;
}
.search-header-left {
  margin-left: -70px!important;
}

.search-btn {
  background-color: #9CCC14;
}
.v-btn::before {
  background-color: #9CCC14;
}
.sw-label{
  font-size: 18px;
  margin-top: 20px;
  margin-right: 10px;
  font-weight: bold;
}
.m-left{
  margin-left: -40px;
}
.buttons-area-1{
  float:left;
  //border: 1px solid blue;
  width: 12%;
  height: 50px;
  margin-top: 10px;
}
.buttons-area-2{
  float:right;
  //border: 1px solid blue;
  width: 19%;
  height: 50px;
  margin-top: -50px;
}
</style>