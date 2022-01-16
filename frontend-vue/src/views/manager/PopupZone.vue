<template>
  <div>
    <CCard>
      <v-app class="sr-card-app-title">
        <CCardHeader>
          <CIcon name="cil-justify-center"/>
          <strong> 팝업존관리 </strong>
        </CCardHeader>
        <CCardBody>
          <CNavbar
              expandable="md"
              color="light"
          >
            <CCol sm="8">
              <v-text-field outlined dense hide-details
                            placeholder="검색어를 입력하세요"
                            v-model="filter.querystring"
                            @keydown.enter="getPopupZone()"
                            class="m-right bg-white"
              />
            </CCol>
            <CCol sm="1">
              <v-btn depressed dark big
                     color="light-blue darken-2"
                     @click="getPopupZone()">
                <v-icon small>mdi-magnify</v-icon>
                <div class="ml-1">검색</div>
              </v-btn>
            </CCol>
            <CCol sm="1">
              <v-btn depressed dark big
                     color="light-blue darken-2"
                     class="m-right"
                     @click="onMakeSamllPatentDialog()">
                <v-icon small>mdi-plus</v-icon>
                <div class="ml-1">팝업존 등록</div>
              </v-btn>
            </CCol>
          </CNavbar>
        </CCardBody>
      </v-app>
    </CCard>
    <CCard>
      <v-app class="sr-card-app">
        <v-data-table
            :headers="community.headers_notice"
            :items="community.data"
            :loading="community.loading"
            :options.sync="community.options"
            :server-items-length="community.total"
            :items-per-page="10"
            :footer-props="{'items-per-page-options': [5, 10, 15,20,25,30,-1]}"
            class="elevation-1 mt-4 "
        >
          <template v-slot:item="row">
            <tr class="clickable-row" @click="onPopupZoneModifyHandler(row.item,'VIEW')">
              <td>{{ row.item._index }}</td>
              <td style="height:100px"><img :src="getImageUrl(row.item.contents)"  width="100px" height="100px" /></td>
              <td>{{ row.item.title }}</td>
              <td>{{ row.item.view_cnt}}</td>
              <td @click.stop> <v-btn outlined x-small rounded color="primary" @click="onPopupZoneModifyHandler(row.item,'MODIFY')">수정</v-btn></td>
              <td @click.stop> <v-btn outlined x-small rounded color="red" @click="delPopupZone(row)">삭제</v-btn></td>
            </tr>
          </template>
        </v-data-table>
        <v-dialog v-model="community.dialog.show" persistent max-width="600px" :key="community.dialog.id">
          <v-card :loading="loading" :disabled="loading">
            <v-card-title class="pt-2 pb-1 primary white--text">
              <span class="body-1">팝업존작성</span>
            </v-card-title>
            <v-divider />
            <v-card-text>
              <v-container :key="community.dialog.id">
                <v-row>
                  <v-col cols="12" sm="12">
                    <v-text-field outlined dense hide-details
                                  label="팝업존 주소(URL)- http:// 문구 필수 입력"
                                  placeholder=""
                                  v-model="community.dialog.title"
                    />
                  </v-col>
                  <v-col cols="12">
                    <CCard>
                      <CCardHeader>
                        팝업존이미지
                      </CCardHeader>
                      <CCardBody>
                        <CCarousel
                            arrows
                            indicators
                            animate
                            height="300px"
                            v-show="(community.dialog.contents.length > 0)"
                        >
                          <CCarouselItem
                              :image="getImageUrl(community.dialog.contents)"
                          />
                        </CCarousel>
<!--                        <abl-textarea class="abl-text-bg" @callBackImage="emitCallbackImage" v-model="community.dialog.contents"  width="400px" height="250px" />-->

                      </CCardBody>
                    </CCard>
                  </v-col>
                </v-row>
                <v-row>
                  <v-col cols="12">

                    <CCard>
                      <CCardHeader>
                        팝업존이미지 추가
                      </CCardHeader>
                      <CCardBody>
                        <v-file-input
                            truncate-length="50"
                            v-model="community.dialog.file_input"
                            color="deep-purple accent-4"
                            :placeholder="community.dialog.contents"
                            class="f-size"
                            @change="onUploadChange()"
                        ></v-file-input>
                      </CCardBody>
                    </CCard>
                  </v-col>
                </v-row>
              </v-container>
            </v-card-text>
            <v-card-actions>
              <v-btn
                  color="light-blue darken-2"
                  class="flex-grow-1"
                  text
                  @click="onPopupZoneDialogClose()"
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
              <v-btn tile depressed class="flex-grow-1" @click="deletePopupZone(community.dialog.del_item)">삭제</v-btn>
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
import AblTextarea from '@/components/AblTextarea'
export default {
  components: {AblTextarea},
  methods: {
    async getPopupZone() {
      this.community.loading = true;
      const { page, itemsPerPage,sortBy, sortDesc } = this.community.options;
      let filters_and = [];
      let filters_or = [];
      let order_by = []
      if(this.filter.querystring != ''){
        filters_or.push({"name": "title", "op": "like", "val": "%"+this.filter.querystring+"%"});
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
        let { data } = await this.$http.get("popupzone", { params });
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
      this.community.dialog.title = ''
      this.community.dialog.file_path = ''
      this.community.dialog.file_name = ''
      this.community.dialog.file_input = ''
      this.community.dialog.show = true
      this.community.dialog.canModify = true
      this.community.dialog.canFileModify = true
      this.community.dialog.current_job = "MAKE"
      this.community.dialog.contents = ""
    },
    onPopupZoneDialogClose() {
      this.community.dialog.show = false
    },
    async submitHandler(){
      let msg = [];
      if (this.community.dialog.title.length == 0){
        this.$session.$emit('modal-alert','팝업존 주소(URL)을 입력하여 주세요!')
        return
      }
      if (this.community.dialog.contents.length == 0){
        this.$session.$emit('modal-alert', '팝어존이미지를 입력하여 주세요!')
        return
      }

      let params = {}
      params.title = this.community.dialog.title;
      params.contents = this.community.dialog.contents;
      let today = moment().format('YYYY-MM-DD HH:mm:ss')
      params.updated_date = today
      params.created_date = today

      if(this.community.dialog.current_job == 'MODIFY'){
        await this.$http.patch(`popupzone/${this.community.dialog.id}`, params)
      }else{
        await this.$http.post(`popupzone`, params)
      }

      this.getPopupZone()
      this.community.dialog.show = false
      this.community.dialog.alert_show = true
    },
    getAttachFileName(attach_file){
      if(attach_file != undefined && attach_file.length > 0){
        return "유"
      }
      return '무'
    },
    async onPopupZoneModifyHandler(item,job){
      this.community.dialog.show = true
      this.community.dialog.id = item.id
      this.community.dialog.title = item.title
      this.community.dialog.contents = item.contents
      this.community.dialog.file_path = item.attatch_file_path
      this.community.dialog.file_name = item.attatch_file_name
      if(job == 'MODIFY')
        this.community.dialog.canModify = true
      else
        this.community.dialog.canModify = false
      this.community.dialog.current_job = job
      let params = {}
      params.view_cnt = item.view_cnt + 1;
      await this.$http.patch(`popupzone/${item.id}`, params)
    },

    async deletePopupZone(item) {
      this.community.dialog.del_show = false
      await this.$http.delete(`popupzone/${item.id}`)
      this.$session.$emit('modal-alert', '삭제되었습니다')
      this.getPopupZone()
    },
    delPopupZone(row) {
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
    async emitCallbackImage(image_data){
      this.file_post_upload(image_data,true)
    },
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
    async file_post_upload(image_file,bInsertToUi=true) {
      const fd = new FormData()
      fd.append('file', image_file)
      let {data} = await this.$http.post('attachment', fd)
      console.log("data.filename :" + JSON.stringify(data.filename))
      if (!data || !data.result || !data.filename)
        return alert("이미지 저장실패!!")
      this.insertImage(`/api/v1/attachment/${data.filename}`)
    },
    insertImage (path) {
      console.log("path : " + path)
      document.execCommand('InsertHtml', false, `
                <div style="width: 400px; height:250px;">
                    <img src="${path}"  style="width: 400px; height:250px;">
                </div>
            `)
      this.refresh_id += 1
    },
    async onUploadChange(){
      if(this.community.dialog.file_input != null) {
        this.community.dialog.contents = await this.upload_file(this.community.dialog.file_input, "attachment")
      }
    },
    getImageUrl(image_path){
      return this.$getWebURL() + '/api/v1/attachment/' + image_path
    }
  },
  mounted() {
    this.getPopupZone();
  },
  computed: {
  },
  watch: {
    "table.options": {
      handler() {
        this.getPopupZone();
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
        headers_notice: [
          {text: 'No.', value: 'id', sortable: false, align: 'center', width: 40},
          {text: "팝업존이미지", value: "contents", align: 'center',sortable: false},
          {text: "팝업존 주소(URL)", value: "title",  align: 'center',sortable: false},
          {text: "조회수", value: "view_cnt",  align: 'center',sortable: false},
          {text: "수정", value: "",  align: 'center',sortable: false, width: 40},
          {text: "삭제", value: "",  align: 'center',sortable: false, width: 40}
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