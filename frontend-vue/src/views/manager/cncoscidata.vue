<template>
  <div>
    <CCard>
      <v-app class="sr-card-app-title">
        <CCardHeader>
          <CIcon name="cil-justify-center"/>
          <strong> KAIST CNC 진동 데이터 </strong>
        </CCardHeader>
        <CCardBody>
          <CNavbar
              expandable="md"
              color="light"
          >
            <CCol sm="2">
              <v-text-field outlined dense hide-details readonly
                            label="시작일"
                            v-model="search.dialog.form.acci_start_date"
                            @click="setSearchDatetime(search.dialog.form,'acci_start_date')"
              />
            </CCol>
            ~
            <CCol sm="2">
              <v-text-field outlined dense hide-details readonly
                            label="종료일"
                            v-model="search.dialog.form.acci_end_date"
                            @click="setSearchDatetime(search.dialog.form,'acci_end_date')"
              />
            </CCol>
            <CCol sm="6">
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
              <td class="clickable-row" >{{ row.item.file_names }}</td>
              <td class="clickable-row" >{{ row.item.sensor_num }}</td>
              <td> {{row.item.created_date | moment('YYYY-MM-DD HH:mm:ss')}}</td>
              <td> <v-btn outlined x-small rounded color="primary" @click="onSensorDetailHandler(row.item)">그래프</v-btn></td>
              <td> <v-btn outlined x-small rounded color="primary" @click="onSensorDetailHandler(row.item)">다운로드</v-btn></td>
              <td> <v-btn outlined x-small rounded color="primary" @click="onSensorDetailHandler(row.item)">상세보기</v-btn></td>
            </tr>
          </template>
        </v-data-table>
        <v-dialog v-model="sensorDetail.show" persistent max-width="840px" >
          <v-card>
            <div class="sensor-detail-container">
              <v-btn fab x-small dark depressed color="grey darken-1" class="sensor-detail-close" @click="sensorDetail.show = false">
                <v-icon>mdi-close</v-icon>
              </v-btn>
              <cncosci-detail @callBackEvent="onEmitEvent" :cncosci_data="sensorDetail.data" />
            </div>
          </v-card>
        </v-dialog>
        <v-dialog v-model="search.datetime.show" width="300" overlay-opacity="0.9">
          <div class="white">
            <div class="d-flex white">
              <v-date-picker no-title v-model="search.datetime.date" />
            </div>
            <div class="d-flex pa-2">
              <v-btn class="flex-grow-1" tile depressed @click="search.datetime.show=false">취소</v-btn>
              <v-btn
                  class="flex-grow-1 ml-2"
                  tile
                  depressed
                  color="primary"
                  @click="saveSearchDatetime">
                선택
              </v-btn>
            </div>
          </div>
        </v-dialog>
      </v-app>
    </CCard>

  </div>
</template>

<script>
import CncosciDetail from '@/components/CncosciDetail'
import axios from 'axios'
import moment from 'moment'
export default {
  components: {CncosciDetail,moment},
  methods: {
    async query() {
      this.table.loading = true;
      const { page, itemsPerPage } = this.table.options;
      let filters_and = []
      let filters_or = []
      filters_and.push({name: 'sensor_type', op: 'eq', val: 'CNCOSCI'})
      // if(this.selected_tech != -1){
      //   filters_and.push({name: 'tech_type', op: 'eq', val: this.selected_tech})
      // }
      // if(this.selected_year != '전체'){
      //   filters_and.push({name: 'apply_date', op: 'eq', val: this.selected_year})
      // }
      // if (this.filter.querystring) {
      //   filters_or.push({name: 'person', op: 'like', val: "%"+this.filter.querystring+"%"})
      //   filters_or.push({name: 'patent_code', op: 'like', val: "%"+this.filter.querystring+"%"})
      //   filters_or.push({name: 'description', op: 'like', val: "%"+this.filter.querystring+"%"})
      // }

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
      let { data } = await this.$http.get("sensorfiles", { params });
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
    onSensorDetailHandler (sensorData) {
      this.dialog.refresh_id += 1
      this.sensorDetail.data = sensorData
      this.sensorDetail.show = true
    },
    onPatentAddHandler () {
      this.sensorDetail.data = null
      this.sensorDetail.show = true
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
    setSearchDatetime(form, datakey) {
      let dt = form[datakey].split(/\s+/);
      this.search.datetime.form = form;
      this.search.datetime.datakey = datakey;
      this.search.datetime.date = dt[0];
      this.search.datetime.show = true;
    },
    saveSearchDatetime() {
      this.search.datetime.form[this.search.datetime.datakey] = this.search.datetime.date;
      this.search.datetime.show = false;
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
          { text: "파일명", value: "file_names", sortable: false, width: 100 },
          { text: "채널번호", value: "sensor_num", sortable: false,align: "center", width: 100 },
          { text: "생성일자", value: "created_date", sortable: false,align: "center", width: 100 },
          {text: "그래프", value: "",  sortable: false, align: "center", width: 100 },
          {text: "다운로드", value: "", sortable: false, align: "center", width: 100 },
          {text: "상세", value: "",  sortable: false, align: "center", width: 100 },
        ],

        loading: false,
        total: 0,
        options: {},
        data: [],
      },
      selected_option:null,
      options_array : [
      ],
      sensorDetail: {
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
      download_file_index:0,
      search: {
        dialog: {
          show: false,
          form: {
            acci_start_date: moment().format("YYYY-MM-DD"),
            acci_end_date: moment().format("YYYY-MM-DD"),
          },
          selected_search_type:null,
          selected_search_type_code:0,
        },
        datetime: {
          show: false,
          date: "",
          time: "",
        },
      },
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
.sensor-detail-container {
  position: relative;
}
.sensor-detail-close {
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