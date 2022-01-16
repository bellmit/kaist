<template>
  <div>
    <CCard>
      <v-app class="sr-card-app-title">
        <CCardHeader>
          <CIcon name="cil-justify-center"/>
          <strong> 마케팅자료 관리 </strong>
        </CCardHeader>
        <CCardBody>
          <CNavbar
              expandable="md"
              color="light"
          >
            <CCol sm="8">
              <v-text-field outlined dense hide-details
                            placeholder="검색어를 입력하세요"
                            append-icon="mdi-magnify"
                            v-model="filter.querystring"
                            @keydown.enter="query()"
                            class="m-right"
              />
            </CCol>
            <CCol sm="1">
              <v-btn depressed dark big
                     color="light-blue darken-2"
                     @click="getCommunity()">
                <v-icon small>mdi-magnify</v-icon>
                <div class="ml-1">검색</div>
              </v-btn>
            </CCol>
            <CCol sm="1">
              <v-btn depressed dark big
                     color="light-blue darken-2"
                     class="m-right"
                     @click="onMakeCommunityDialog()">
                <v-icon small>mdi-plus</v-icon>
                <div class="ml-1">공지사항 작성</div>
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
            <tr class="clickable-row" @click="onCommunityModifyHandler(row.item)">
              <td>{{ row.item._index }}</td>
              <td>{{ row.item.user_id }}</td>
              <td>{{ row.item.user_name }}</td>
              <td>{{ row.item.title }}</td>
              <td>{{ row.item.view_cnt}}</td>
              <td>{{ row.item.created_date | moment('YYYY-MM-DD HH:mm:ss') }}</td>
              <td>{{ row.item.updated_date | moment('YYYY-MM-DD HH:mm:ss') }}</td>
              <td @click.stop> <v-btn outlined x-small rounded color="red" @click="delCommunity(row)">삭제</v-btn></td>
            </tr>
          </template>
        </v-data-table>
        <v-dialog v-model="community.dialog.show" persistent max-width="600px" :key="community.dialog.id">
          <v-card :loading="loading" :disabled="loading">
            <v-card-title class="pt-2 pb-1 primary white--text">
              <span class="body-1">공지사항 작성</span>
            </v-card-title>
            <v-divider />
            <v-card-text>
              <v-container :key="community.dialog.id">
                <v-row>
                  <v-col cols="12" sm="6">
                    <v-text-field outlined dense hide-details
                                  label="글쓴이 아이디"
                                  placeholder=""
                                  disabled
                                  v-model="community.dialog.user_id"
                    />
                  </v-col>
                  <v-col cols="12" sm="6">
                    <v-text-field outlined dense hide-details
                                  label="글쓴이 이름"
                                  placeholder=""
                                  disabled
                                  v-model="community.dialog.user_name"
                    />
                  </v-col>
                  <v-col cols="12" sm="12">
                    <v-text-field outlined dense hide-details
                                  label="제목"
                                  placeholder=""
                                  v-model="community.dialog.title"
                                  :disabled="!community.dialog.canModify"
                    />
                  </v-col>
                  <v-col cols="12">
                    <v-textarea
                        outlined
                        name="input-7-4"
                        label="내용입력"
                        value=""
                        v-model="community.dialog.contents"
                        :disabled="!community.dialog.canModify"
                    ></v-textarea>
                  </v-col>
                </v-row>
              </v-container>
            </v-card-text>
            <v-card-actions>
              <v-btn
                  color="light-blue darken-2"
                  class="flex-grow-1"
                  text
                  @click="onCommunityDialogClose()"
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
              <v-btn tile depressed class="flex-grow-1" @click="deleteCommunity(community.dialog.del_item)">삭제</v-btn>
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
    async getCommunity() {
      this.community.loading = true;
      const { page, itemsPerPage,sortBy, sortDesc } = this.community.options;
      let filters_and = [];
      let filters_or = [];
      let order_by = []
      if(this.community.search_text != ''){
        filters_or.push({"name": "user_id", "op": "like", "val": "%"+this.community.search_text+"%"});
        filters_or.push({"name": "user_name", "op": "like", "val": "%"+this.community.search_text+"%"});
        filters_or.push({"name": "title", "op": "like", "val": "%"+this.community.search_text+"%"});
        filters_or.push({"name": "contents", "op": "like", "val": "%"+this.community.search_text+"%"});
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
        let { data } = await this.$http.get("community", { params });
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
    onMakeCommunityDialog(){
      this.community.dialog.id = -1
      this.community.dialog.contents = ''
      this.community.dialog.title = ''
      this.community.dialog.user_id = this.$session.getUserId()
      this.community.dialog.user_name = this.$session.getUserName()
      this.community.dialog.file_path = ''
      this.community.dialog.file_name = ''
      this.community.dialog.file_input = ''
      this.community.dialog.show = true
      this.community.dialog.canModify = true
      this.community.dialog.canFileModify = true
      this.community.dialog.community_type = this.selected_tab_item + 1
      this.community.dialog.current_job = "MAKE"
      this.community.dialog.selected_open = this.community.dialog.open_list[0]
      this.community.dialog.selected_open_range = this.community.dialog.open_range_list[0]
    },
    onCommunityDialogClose() {
      this.getCommunity(this.type_tab_items[this.selected_tab_item])
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
      let params = {}
      params.title = this.community.dialog.title;
      params.contents = this.community.dialog.contents;
      params.user_id = this.$session.getUserId();
      params.user_name = this.$session.getUserName();
      let today = moment().format('YYYY-MM-DD HH:mm:ss')
      params.updated_date = today
      params.open = this.community.dialog.selected_open.code
      if(this.selected_tab_item == 1 && this.community.dialog.current_job == "MAKE") {
        params.community_type = this.selected_tab_item + 1
      }
      else
        params.community_type =this.selected_tab_item + 1

      if(this.community.dialog.file_input != '' && this.community.dialog.file_input != null) {
        const fd = new FormData()
        fd.append('file', this.community.dialog.file_input)
        let {data} = await this.$http.post('upload_file', fd)
        if (!data || !data.result || !data.filename)
          return alert("이미지 저장실패!!")
        params.attatch_file_path = data.filename
        params.attatch_file_name = data.src_filename
      }

      if(this.community.dialog.current_job == "MAKE") {
        params.created_date = today
        await this.$http.post(`community`, params)
      }
      else{
        await this.$http.patch(`community/${this.community.dialog.id}`, params)
      }
      this.getCommunity()
      this.community.dialog.show = false
      this.community.dialog.alert_show = true
    },
    getAttachFileName(attach_file){
      if(attach_file != undefined && attach_file.length > 0){
        return "유"
      }
      return '무'
    },
    async onCommunityModifyHandler(item){
      this.community.dialog.show = true
      this.community.dialog.id = item.id
      this.community.dialog.title = item.title
      this.community.dialog.user_id = item.user_id
      this.community.dialog.user_name = item.user_name
      this.community.dialog.contents = item.contents
      this.community.dialog.file_path = item.attatch_file_path
      this.community.dialog.file_name = item.attatch_file_name
      this.community.dialog.canModifile_namefy = false
      this.community.dialog.community_type = item.community_type
      this.community.dialog.selected_open = this.community.dialog.open_list[item.open]
      this.community.dialog.canModify = false
      this.community.dialog.canFileModify = false
      if(this.$session.getUserId() == item.user_id) {
        this.community.dialog.canModify = true
        this.community.dialog.canFileModify = true
      }
      this.community.dialog.current_job = "MODIFY"
      let params = {}
      params.view_cnt = item.view_cnt + 1;
      await this.$http.patch(`community/${item.id}`, params)
    },
    async deleteCommunity(item) {
      this.community.dialog.del_show = false
      await this.$http.delete(`community/${item.id}`)
      this.$session.$emit('modal-alert', '삭제되었습니다')
      this.getCommunity()
    },
    delCommunity(row) {
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
  },
  mounted() {
    this.getCommunity();
  },
  computed: {
  },
  watch: {
    "table.options": {
      handler() {
        this.getCommunity();
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
          {text: "글쓴이 아이디", value: "user_id", align: 'center',sortable: false},
          {text: "글쓴이 이름", value: "user_name",  align: 'center',sortable: false},
          {text: "제목", value: "title",  align: 'center',sortable: false},
          {text: "조회수", value: "view_cnt",  align: 'center',sortable: false},
          {text: "작성일", value: "created_date",  align: 'center',sortable: false},
          {text: "수정일", value: "updated_date",  align: 'center',sortable: false},
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
          user_id:'',
          user_name:'',
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
          parent_id:-1,
          community_type:0,
          selected_open:null,
          open_list:[
            {name:"비공개",code:0},
            {name:"공개",code:1},
          ],
          selected_open_range:null,
          selected_open_range_code:0,
          open_range_list:[
            {name:'전체',code:0},
            {name:'한국교육시설안전원',code:1},
            {name:'회원 및 학교',code:2},
          ],
          current_job:''
        },
        dialog_response:{
          show:false,
          id:'',
          title:'',
          user_id:'',
          user_name:'',
          contents:'',
          response_contents:'',
          file_input:null,
          file_path:null,
          file_name: '파일을 선택해 주세요',
          del_show:false,
          deleted_show:false,
          del_item:null,
          canModify:false,
          canFileModify:false,
          parent_id:-1,
          community_type:0,
          current_job:''
        }
      },
      popuptwo:{
        show: false,
        del_show: false,
        error: [],
        delItem:null
      },
      member_type:[
        "관리자",
        "기관사용자",
        "일반사용자"
      ],
      loading: false,
      selected_tab_item: null,
      type_tab_items: ['공지','Q & A','자료실'],
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