<template>
  <div>
    <CCard>
      <v-app class="sr-card-app-title">
        <CCardHeader>
          <CIcon name="cil-justify-center"/>
          <strong> 생산기술연구원 특허문서 검색 </strong>
        </CCardHeader>
        <CCardBody>
          <CNavbar
              expandable="md"
              color="light"
          >
            <CCol sm="2">
              <v-select outlined dense hide-details
                        v-model="selected_tech"
                        :items="tech_types"
                        label="기술분야"
                        item-text="text"
                        item-value="value"
                        @change="onChangeTechTypes()"
                        class="bg-white"
              />
            </CCol>
            <CCol sm="2">
              <v-select outlined dense hide-details
                        v-model="selected_year"
                        :items="years_type"
                        label="출원연도"
                        @change="onChangeYearsTypes()"
                        class="bg-white"
              />
            </CCol>
            <CCol sm="4">
              <v-text-field outlined dense hide-details
                            placeholder="검색어를 입력하세요"
                            append-icon="mdi-magnify"
                            v-model="filter.querystring"
                            @keydown.enter="query()"
                            class="m-right bg-white"
              />
            </CCol>
            <CCol sm="1">
              <v-btn depressed dark big
                     color="light-blue darken-2"
                     @click="query">
                <v-icon small>mdi-magnify</v-icon>
                <div class="ml-1">검색</div>
              </v-btn>
            </CCol>
            <CCol sm="1.5">
              <v-btn depressed dark big
                     color="light-blue darken-2"
                     class="m-right"
                     @click="onPatentAddHandler()">
                <v-icon small>mdi-plus</v-icon>
                <div class="ml-1">특허문서 등록</div>
              </v-btn>
            </CCol>
            <CCol sm="1.5">
              <v-btn depressed dark big
                     color="light-blue darken-2"
                     class="m-right"
                     @click="excel_dowunload()">
                <v-icon small>mdi-cloud-download</v-icon>
                <div class="ml-1">XLS 다운로드</div>
              </v-btn>
            </CCol>
          </CNavbar>
        </CCardBody>
      </v-app>
    </CCard>
    <CCard>
      <v-app class="sr-card-app">
        <v-data-table
            height="calc(100vh-100vh)"
            :headers="table.headers"
            :items="table.data"
            :server-items-length="table.total"
            :loading="table.loading"
            :options.sync="table.options"
            :footer-props="{ 'items-per-page-options': [15, 30, 60] }"
            class="elevation-1"
        >
          <template v-slot:item="row">
            <tr>
              <td>{{ row.item._index }}</td>
              <td class="clickable-row" @click="$pdfDownload(row.item.patent_code)">{{row.item.patent_code}}</td>
              <td class="clickable-row" >{{ row.item.person }}</td>
              <td class="clickable-row" >{{$getPatentTitle(row.item.description)}}</td>
              <td>
                <v-btn depressed dark small
                       color="light-blue"
                       class="m-right"
                       @click="attach_download(row.item.maketting_file_path)"
                       v-if="check_item(row.item.maketting_file_path)"
                  >
                  <v-icon small>mdi-download</v-icon>
                  <div class="ml-1">다운로드</div>
                </v-btn>
              </td>
              <td> {{row.item.updated_date | moment('YYYY-MM-DD HH:mm:ss')}}</td>
              <td v-show="$session.check_permission()" @click.stop> <v-btn outlined x-small rounded color="primary" @click="onPatentDetailHandler(row.item)">수정</v-btn></td>
              <td v-show="$session.check_permission()" @click.stop> <v-btn outlined x-small rounded color="red" @click="delPatent(row)">삭제</v-btn></td>
            </tr>
          </template>
        </v-data-table>
        <v-dialog v-model="patentDetail.show" persistent max-width="840px" :key="patentDetail.data">
          <v-card>
            <div class="school-detail-container">
              <v-btn fab x-small dark depressed color="grey darken-1" class="school-detail-close" @click="patentDetail.show = false">
                <v-icon>mdi-close</v-icon>
              </v-btn>
              <patent-detail @callBackEvent="onEmitEvent" :patent="patentDetail.data" />
            </div>
          </v-card>
        </v-dialog>
        <v-dialog v-model="dialog.del_show" max-width="500px">
          <v-card>
            <v-card-title>선택한 내용을 삭제하시겠습니까?</v-card-title>
            <v-card-actions>
              <v-btn tile depressed class="flex-grow-1" @click="deletePatent(dialog.del_item)">삭제</v-btn>
              <v-btn tile depressed class="flex-grow-1" @click="dialog.del_show = false">취소</v-btn>
            </v-card-actions>
          </v-card>
        </v-dialog>
        <input type="file" ref="fileinput" accept=".pdf" class="f-pos" @change="onFileChangeHandler($event)" onclick="this.value=null"/>
      </v-app>
    </CCard>

  </div>
</template>

<script>
import PatentDetail from '@/components/PatentDetail'
import axios from 'axios'
import moment from 'moment'
export default {
  components: {PatentDetail,moment},
  methods: {
    async query() {
      this.table.loading = true;
      const { page, itemsPerPage } = this.table.options;
      let filters_and = []
      let filters_or = []

      if(this.selected_tech != -1){
        filters_and.push({name: 'tech_type', op: 'eq', val: this.selected_tech})
      }
      if(this.selected_year != '전체'){
        filters_and.push({name: 'apply_date', op: 'eq', val: this.selected_year})
      }
      if (this.filter.querystring) {
        filters_or.push({name: 'person', op: 'like', val: "%"+this.filter.querystring+"%"})
        filters_or.push({name: 'patent_code', op: 'like', val: "%"+this.filter.querystring+"%"})
        filters_or.push({name: 'description', op: 'like', val: "%"+this.filter.querystring+"%"})
      }

      let q = {
        filters: [{or:filters_or},{and:filters_and}],
        // order_by: [{field: 'apply_date', direction: 'desc'}]
        order_by: [{field: 'id', direction: 'desc'}]
      };

      let params = {
        q: JSON.stringify(q),
        page: page,
        results_per_page: itemsPerPage,
      };
      let { data } = await this.$http.get("sources", { params });
      this.table.total = data.num_results;
      this.table.loading = false;

      this.table.data = data.objects.map((v, i) => {
        v._index = data.num_results - i - (page - 1) * itemsPerPage;
        return v;
      });
    },

    changeOption(){
      this.selected_option = this.options_array.find(v=>v.option_name == this.selected_option)
      this.query();
    },
    onPatentDetailHandler (patentData) {
      this.dialog.refresh_id += 1
      this.patentDetail.data = patentData
      this.patentDetail.show = true
    },
    onPatentAddHandler () {
      this.patentDetail.data = null
      this.patentDetail.show = true
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
        this.query();
      }else if(type == "add"){
        this.query();
      }
      this.patentDetail.show = false
    },
    async deletePatent(item) {
      this.dialog.del_show = false
      await this.$http.delete(`sources/${item.id}`)
      this.$session.$emit('modal-alert', '삭제되었습니다')
      this.query();
    },
    delPatent(row) {
      this.dialog.del_show = true
      this.dialog.del_item = row.item
    },
    async onFileChangeHandler (evt) {
      if (evt.target && evt.target.files && evt.target.files[0]) {
        this.file_post_upload(evt.target.files[0],true)
      }
      else return null
    },
    async file_post_upload(pdf_file) {
      const fd = new FormData()
      fd.append('file', pdf_file)
      let {data} = await this.$http.post('pdf_upload', fd)
      console.log("data.filename :" + JSON.stringify(data.filename))
      if (!data || !data.result || !data.filename)
        return alert("저장실패!!")

    },
    async excel_dowunload() {
      // this.$session.$emit('modal-alert', '준비중입니다...')
      this.download_file_index += 1
      let params = {
        tech_type:this.selected_tech,
        years:this.selected_year,
        search_string:this.filter.querystring,
      }
      let {data} = await this.$http.get("patent_manage_download",{params});
      var url = this.$getWebURL() + '/api/v1/download/' + data.filename
      axios({
        method: 'get',
        url:url,
        // url: 'search_result.xlsx',
        responseType: 'blob'
      })
          .then(response => {
            const url = window.URL.createObjectURL(new Blob([response.data], {
              type: 'application/vnd.ms-excel'
            }))
            const link = document.createElement('a')
            link.href = url
            var download_file_name = '한국생산기술연구원_특허문서리스트_' + this.download_file_index + ".xlsx"
            link.setAttribute('download', download_file_name) // or any other extension
            document.body.appendChild(link)
            link.click()
          })
          .catch(() => console.log('error occured'))
    },
  },
  mounted() {
    if(!this.$session.authorized){
      location.reload(true)
      return
    }
    this.years_type.push('전체')
    this.tech_types.push({text:'전체',value:-1})
    this.tech_types = this.tech_types.concat(this.$constant.tech_types)
    this.years_type = this.years_type.concat(this.years)
    this.selected_tech = this.tech_types[0].value
    this.selected_year = this.years_type[0]
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
        this.query();
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
          { text: "수정일자", value: "updated_date", sortable: false,align: "center" },
          {text: "수정", value: "",  align: 'center',sortable: false, width: 40},
          {text: "삭제", value: "",  align: 'center',sortable: false, width: 40}
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
        data: null,
      },
      dialog: {
        refresh_id :1,
        show: false,
        form: null,
        del_show:false,
        deleted_show:false,
        del_item:null,
      },
      years_type:[],
      tech_types:[],
      selected_year:null,
      selected_tech:null,
      download_file_index:0
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
</style>