<template>
  <div>
    <CCard>
      <v-app class="sr-card-app-title">
        <CCardHeader>
          <CIcon name="cil-justify-center"/>
          <strong> 기술이전관리 </strong>
        </CCardHeader>
        <CCardBody>
          <CNavbar
              expandable="md"
              color="light"
          >
            <v-col sm="2" md="2">
              <v-select outlined dense hide-details
                        v-model="selected_search_result_type"
                        :items="search_result_type"
                        label="처리결과"
                        class="bg-white"
                        @change="onSearchResultType()"
              />
            </v-col>
            <CCol sm="8">
              <v-text-field outlined dense hide-details
                            placeholder="검색어를 입력하세요"
                            v-model="filter.querystring"
                            @keydown.enter="getTechTrans()"
                            class="m-right bg-white"
              />
            </CCol>
            <CCol sm="1">
              <v-btn depressed dark big
                     color="light-blue darken-2"
                     @click="getTechTrans()">
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
            :headers="community.headers"
            :items="community.data"
            :loading="community.loading"
            :options.sync="community.options"
            :server-items-length="community.total"
            :items-per-page="10"
            :footer-props="{'items-per-page-options': [5, 10, 15,20,25,30,-1]}"
            class="elevation-1 mt-4 "
        >
          <template v-slot:item="row">
            <tr class="clickable-row" @click="onTechTransModifyHandler(row.item,'VIEW')">
              <td>{{ row.item._index }}</td>
              <td>{{ row.item.company_name }}</td>
              <td>{{ row.item.request_name }}</td>
              <td>{{ row.item.request_phone }}</td>
              <td>{{ getTransType(row.item.techtrans_type) }}</td>
              <td>{{ getResultType(row.item.techtrans_result) }}</td>
              <td>{{ row.item.created_date }}</td>
              <td @click.stop> <v-btn outlined x-small rounded color="primary" @click="onTechTransModifyHandler(row.item,'MODIFY')">수정</v-btn></td>
              <td @click.stop> <v-btn outlined x-small rounded color="red" @click="delTechTrans(row)">삭제</v-btn></td>
            </tr>
          </template>
        </v-data-table>
        <v-dialog v-model="community.dialog.show" persistent max-width="600px" :key="community.dialog.id">
          <TechTransDialog :techtrans_data="selected_techtrans" @callBackTechTrans="onEmitTechTrans"/>
        </v-dialog>
        <v-dialog v-model="community.dialog.del_show" max-width="500px">
          <v-card>
            <v-card-title>선택한 내용을 삭제하시겠습니까?</v-card-title>
            <v-card-actions>
              <v-btn tile depressed class="flex-grow-1" @click="deleteTechTrans(community.dialog.del_item)">삭제</v-btn>
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
import TechTransDialog from '@/components/TechTransDialog'
export default {
  components: {TechTransDialog},
  methods: {
    async getTechTrans() {
      this.community.loading = true;
      const { page, itemsPerPage,sortBy, sortDesc } = this.community.options;
      let filters_and = [];
      let filters_or = [];
      let order_by = []
      if(this.selected_search_result_type != -1){
        filters_and.push({name: 'techtrans_result', op: 'eq', val: this.selected_search_result_type})
      }
      if(this.filter.querystring != ''){
        filters_or.push({"name": "company_name", "op": "like", "val": "%"+this.filter.querystring+"%"});
        filters_or.push({"name": "request_name", "op": "like", "val": "%"+this.filter.querystring+"%"});
        filters_or.push({"name": "request_contents", "op": "like", "val": "%"+this.filter.querystring+"%"});
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
        let { data } = await this.$http.get("techtrans", { params });
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
    async deleteTechTrans(item) {
      this.community.dialog.del_show = false
      await this.$http.delete(`techtrans/${item.id}`)
      this.$session.$emit('modal-alert', '삭제되었습니다')
      this.getTechTrans()
    },
    delTechTrans(row) {
      this.community.dialog.del_show = true
      this.community.dialog.del_item = row.item
    },
    onEmitTechTrans(){
      this.community.dialog.show = false
      this.getTechTrans()
    },
    async onTechTransModifyHandler(item,job){
      this.selected_techtrans = item
      this.community.dialog.show = true
      this.community.dialog.id = item.id
    },
    getTransType(trans_type){
      return this.trans_type.find(v=>v.value==trans_type).text
    },
    getResultType(techtrans_result){
      return this.result_type.find(v=>v.value == techtrans_result).text
    },
    onSearchResultType(){
      this.getTechTrans()
    }
  },
  mounted() {
    if(!this.$session.authorized){
      location.reload(true)
      return
    }
    this.selected_search_result_type = this.search_result_type[0].value
    this.getTechTrans()
  },
  computed: {
  },
  watch: {
    "table.options": {
      handler() {
        this.getTechTrans();
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
          {text: "회사명", value: "company_name", align: 'center',sortable: false},
          {text: "이름", value: "request_name",  align: 'center',sortable: false},
          {text: "전화번호", value: "request_phone",  align: 'center',sortable: false},
          {text: "실시유형", value: "techtrans_type",  align: 'center',sortable: false},
          {text: "처리결과", value: "techtrans_result",  align: 'center',sortable: false},
          {text: "등록일자", value: "created_date",  align: 'center',sortable: false},
          {text: "수정", value: "",  align: 'center',sortable: false, width: 40},
          {text: "삭제", value: "",  align: 'center',sortable: false, width: 40}
        ],
        search_text: '',
        data: [],
        options: {"page":1,"itemsPerPage":10,"sortBy":[],"sortDesc":[],"groupBy":[],"groupDesc":[],"mustSort":false,"multiSort":false},
        loading: false,
        dialog:{
          show:false,
          del_item:null,
          del_show:false
        },
      },
      loading: false,
      selected_techtrans : null,
      trans_type:[
        {text:'실시유형1',value:0},
        {text:'실시유형2',value:1},
        {text:'실시유형3',value:2},
        {text:'실시유형4',value:3},
      ],
      result_type:[
        {text:'미처리',value:0},
        {text:'대기',value:1},
        {text:'처리완료',value:2},
      ],
      search_result_type: [
        {text:'전체',value:-1},
        {text:'미처리',value:0},
        {text:'대기',value:1},
        {text:'처리완료',value:2},
      ],
      selected_search_result_type:null,
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