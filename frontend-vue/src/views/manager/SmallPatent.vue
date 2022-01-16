<template>
  <div>
    <CCard>
      <v-app class="sr-card-app-title">
        <CCardHeader>
          <CIcon name="cil-justify-center"/>
          <strong> 소액기술관리 </strong>
        </CCardHeader>
        <CCardBody>
          <CNavbar
              expandable="md"
              color="light"
          >
            <CCol sm="10">
              <v-text-field outlined dense hide-details
                            placeholder="검색어를 입력하세요"
                            v-model="filter.querystring"
                            @keydown.enter="getSmallPatent()"
                            class="m-right bg-white"
              />
            </CCol>
            <CCol sm="1">
              <v-btn depressed dark big
                     color="light-blue darken-2"
                     @click="getSmallPatent()">
                <v-icon small>mdi-magnify</v-icon>
                <div class="ml-1">검색</div>
              </v-btn>
            </CCol>
            <CCol sm="1" v-show="$session.check_permission()">
              <v-btn depressed dark big
                     color="light-blue darken-2"
                     class="m-right"
                     @click="onMakeSamllPatentDialog()">
                <v-icon small>mdi-plus</v-icon>
                <div class="ml-1">등록</div>
              </v-btn>
            </CCol>
          </CNavbar>
        </CCardBody>
      </v-app>
    </CCard>
    <CCard>
      <v-app class="sr-card-app">
        <v-data-table
            :headers="getHeader()"
            :items="community.data"
            :loading="community.loading"
            :options.sync="community.options"
            :server-items-length="community.total"
            :items-per-page="10"
            :footer-props="{'items-per-page-options': [5, 10, 15,20,25,30,-1]}"
            class="elevation-1 mt-4 "
        >
          <template v-slot:item="row">
            <tr class="clickable-row" >
              <td>{{ row.item._index }}</td>
              <td @click="$pdfDownload($convertPatentToRaw(row.item.patent_code))">{{ row.item.patent_code }}</td>
              <td @click="onSmallPatentModifyHandler(row.item,'VIEW')">{{ row.item.title }}</td>
              <td>{{ row.item.view_cnt}}</td>
              <td>{{ row.item.costcontents}}</td>
              <td v-show="$session.check_permission()" @click.stop> <v-btn outlined x-small rounded color="primary" @click="onSmallPatentModifyHandler(row.item,'MODIFY')">수정</v-btn></td>
              <td v-show="$session.check_permission()" @click.stop> <v-btn outlined x-small rounded color="red" @click="delSmallPatent(row)">삭제</v-btn></td>
            </tr>
          </template>
        </v-data-table>
        <v-dialog v-model="community.dialog.show" persistent max-width="600px" :key="community.dialog.id">
          <v-card :loading="loading" :disabled="loading">
            <v-card-title class="pt-2 pb-1 primary white--text">
              <span class="body-1">소액기술작성</span>
            </v-card-title>
            <v-divider />
            <v-card-text>
              <v-container :key="community.dialog.id">
                <v-row>
                  <v-col cols="12" sm="12">
                    <v-text-field outlined dense hide-details
                                  label="출원번호"
                                  placeholder=""
                                  v-model="community.dialog.patent_code"
                    />
                  </v-col>
                  <v-col cols="12" sm="12">
                    <v-text-field outlined dense hide-details
                                  label="제목"
                                  placeholder=""
                                  v-model="community.dialog.title"
                    />
                  </v-col>
                  <v-col cols="12">
                    <v-textarea
                        outlined
                        name="input-7-4"
                        label="내용입력"
                        value=""
                        v-model="community.dialog.contents"
                    ></v-textarea>
                  </v-col>
                  <v-col cols="12" sm="12">
                    <v-text-field outlined dense hide-details
                                  label="이전금액"
                                  placeholder=""
                                  v-model="community.dialog.costcontents"
                    />
                  </v-col>
                </v-row>
              </v-container>
            </v-card-text>
            <v-card-actions>
              <v-btn
                  color="light-blue darken-2"
                  class="flex-grow-1"
                  text
                  @click="onSmallPatentDialogClose()"
              >
                닫기
              </v-btn>
              <v-btn
                  color="primary"
                  class="flex-grow-1"
                  tile
                  :disabled="!community.dialog.canModify"
                  depressed
                  @click="submitHandler"
              >
                작성
              </v-btn>
            </v-card-actions>
          </v-card>
        </v-dialog>
        <v-dialog v-model="community.dialog.del_show" max-width="500px">
          <v-card>
            <v-card-title>선택한 내용을 삭제하시겠습니까?</v-card-title>
            <v-card-actions>
              <v-btn tile depressed class="flex-grow-1" @click="deleteSmallPatent(community.dialog.del_item)">삭제</v-btn>
              <v-btn tile depressed class="flex-grow-1" @click="community.dialog.del_show = false">취소</v-btn>
            </v-card-actions>
          </v-card>
        </v-dialog>
      </v-app>
    </CCard>

  </div>
</template>

<script>
import moment from 'moment'
export default {
  methods: {
    async getSmallPatent() {
      this.community.loading = true;
      const { page, itemsPerPage,sortBy, sortDesc } = this.community.options;
      let filters_and = [];
      let filters_or = [];
      let order_by = []
      if(this.filter.querystring != ''){
        filters_or.push({"name": "patent_code", "op": "like", "val": "%"+this.filter.querystring+"%"});
        filters_or.push({"name": "title", "op": "like", "val": "%"+this.filter.querystring+"%"});
        filters_or.push({"name": "contents", "op": "like", "val": "%"+this.filter.querystringt+"%"});
      }
      if (sortBy.length) {
        for (let i=0; i<sortBy.length; i++) {
          order_by.push({field: sortBy[i], direction: sortDesc[i] ? 'desc' : 'asc'})
        }
      }
      else order_by.push({field: 'id', direction: 'desc'})

      let q = {
        filters: [{or:filters_or},{and:filters_and}],
        order_by
      }
      let params = {q: JSON.stringify(q), results_per_page: itemsPerPage, page: page}

      try {
        let { data } = await this.$http.get("smallpatent", { params });
        this.community.total = data.num_results;
        this.community.data = data.objects.map((v, i) => {
          v._index = i + (page - 1) * itemsPerPage + 1;
          return v;
        });
      } catch (err) {
        console.error(err);
      } finally {
        this.community.loading = false;
      }
    },
    onMakeSamllPatentDialog(){
      this.community.dialog.id = -1
      this.community.dialog.patent_code = ''
      this.community.dialog.contents = ''
      this.community.dialog.title = ''
      this.community.dialog.file_path = ''
      this.community.dialog.file_name = ''
      this.community.dialog.file_input = ''
      this.community.dialog.costcontents = ''
      this.community.dialog.show = true
      this.community.dialog.canModify = true
      this.community.dialog.canFileModify = true
      this.community.dialog.current_job = "MAKE"
    },
    onSmallPatentDialogClose() {
      this.community.dialog.show = false
    },
    async submitHandler(){
      let msg = [];
      if (this.community.dialog.title.length == 0){
        this.$session.$emit('modal-alert','제목을 입력하여 주세요!')
        return
      }
      if (this.community.dialog.contents.length == 0){
        this.$session.$emit('modal-alert', '내용을 입력하여 주세요!')
        return
      }
      if (this.community.dialog.patent_code.length == 0){
        this.$session.$emit('modal-alert','출원번호를 입력하여 주세요!')
        return
      }

      let params = {}
      params.title = this.community.dialog.title;
      params.contents = this.community.dialog.contents;
      params.patent_code= this.community.dialog.patent_code;
      params.costcontents= this.community.dialog.costcontents;
      let today = moment().format('YYYY-MM-DD HH:mm:ss')
      params.updated_date = today
      params.created_date = today

      if(this.community.dialog.current_job == 'MODIFY'){
        await this.$http.patch(`smallpatent/${this.community.dialog.id}`, params)
      }else{
        await this.$http.post(`smallpatent`, params)
      }

      this.getSmallPatent()
      this.community.dialog.show = false
      this.community.dialog.alert_show = true
    },
    getAttachFileName(attach_file){
      if(attach_file != undefined && attach_file.length > 0){
        return "유"
      }
      return '무'
    },
    async onSmallPatentModifyHandler(item,job){
      this.community.dialog.show = true
      this.community.dialog.id = item.id
      this.community.dialog.title = item.title
      this.community.dialog.patent_code = item.patent_code
      this.community.dialog.contents = item.contents
      this.community.dialog.file_path = item.attatch_file_path
      this.community.dialog.file_name = item.attatch_file_name
      this.community.dialog.costcontents = item.costcontents
      if(job == 'MODIFY')
        this.community.dialog.canModify = true
      else
        this.community.dialog.canModify = false
      this.community.dialog.current_job = job
      let params = {}
      params.view_cnt = item.view_cnt + 1;
      await this.$http.patch(`smallpatent/${item.id}`, params)
    },

    async deleteSmallPatent(item) {
      this.community.dialog.del_show = false
      await this.$http.delete(`smallpatent/${item.id}`)
      this.$session.$emit('modal-alert', '삭제되었습니다')
      this.getSmallPatent()
    },
    delSmallPatent(row) {
      this.community.dialog.del_show = true
      this.community.dialog.del_item = row.item
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
    check_file(filepath){
      if(filepath != undefined && filepath.length > 0)
        return false
      return true
    },
    getHeader(){
      if(this.$session.check_permission()){
        return this.community.headers
      }
      return this.community.headers_anyone
    }
  },
  mounted() {
    this.getSmallPatent();
  },
  computed: {
  },
  watch: {
    "table.options": {
      handler() {
        this.getSmallPatent();
      },
      deep: true,
    },
  },
  data() {
    return {
      filter: {
        querystring: "",
      },
      community: {
        headers: [
          {text: 'No.', value: 'id', sortable: false, align: 'center', width: 40},
          {text: "출원번호", value: "patent_code", align: 'center',sortable: false},
          {text: "제목", value: "title",  align: 'center',sortable: false},
          {text: "조회수", value: "view_cnt",  align: 'center',sortable: false},
          {text: "이전금액", value: "costcontents",  align: 'center',sortable: false},
          {text: "수정", value: "",  align: 'center',sortable: false, width: 40},
          {text: "삭제", value: "",  align: 'center',sortable: false, width: 40}
        ],
        headers_anyone: [
          {text: 'No.', value: 'id', sortable: false, align: 'center', width: 40},
          {text: "출원번호", value: "patent_code", align: 'center',sortable: false},
          {text: "제목", value: "title",  align: 'center',sortable: false},
          {text: "조회수", value: "view_cnt",  align: 'center',sortable: false},
          {text: "이전금액", value: "costcontents",  align: 'center',sortable: false},
        ],
        search_text: '',
        data: [],
        options: {"page":1,"itemsPerPage":10,"sortBy":[],"sortDesc":[],"groupBy":[],"groupDesc":[],"mustSort":false,"multiSort":false},
        loading: false,
        dialog:{
          show:false,
          id:'',
          title:'',
          contents:'',
          file_input:null,
          file_path:null,
          file_name: '파일을 선택해 주세요',
          del_show:false,
          deleted_show:false,
          alert_show:false,
          del_item:null,
          canModify:false,
          canFileModify:false,
          patent_code:'',
          costcontents:'',
          current_job:''
        },
      },
      loading: false,
      selected_tab_item: null,
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