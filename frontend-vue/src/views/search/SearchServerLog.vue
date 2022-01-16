<template>
  <div>
    <CCard>
      <v-app class="sr-card-app-title">
        <CCardHeader>
          <CIcon name="cil-justify-center"/>
          <strong> 수집 서버 로그 검색 </strong>
        </CCardHeader>
        <CCardBody>
          <CNavbar
              expandable="md"
              color="light"
          >
            <CToggler inNavbar @click="show=!show"/>
            <CCol sm="2">
              <v-select outlined dense hide-details
                        v-model="selected_server"
                        :items="servers_array"
                        label="서버"
                        item-text="server_name"
                        item-value=""
                        @change="changeServer"
              />
            </CCol>
            <CCol sm="9">
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
            :headers="getHeader()"
            :items="table.data"
            :server-items-length="table.total"
            :loading="table.loading"
            :options.sync="table.options"
            :footer-props="{ 'items-per-page-options': [10, 20, 40] }"
            class="elevation-1"
        >
          <template v-slot:[`item.id`]="{ item }">
            {{ item._index }}
          </template>
        </v-data-table>
      </v-app>
    </CCard>

  </div>
</template>

<script>
export default {
  methods: {
    async query() {
      this.table.loading = true;
      const { page, itemsPerPage } = this.table.options;
      let filters_and = []


      let q = {
        filters: [{and: filters_and}],
        order_by: [{field: 'id', direction: 'asc'}]
      };

      if (this.filter.querystring) {
        filters_and.push({name: 'user_name', op: 'like', val: "%"+this.filter.querystring+"%"})
      }

      let params = {
        q: JSON.stringify(q),
        page: page,
        results_per_page: itemsPerPage,
      };

      var api_name = "logs_safepc"
      if(this.selected_server.server_id == 2){
        api_name = "logs_safepc_usb"
      }else if(this.selected_server.server_id == 3){
        api_name = "logs_safepc_uselog"
      }
      let { data } = await this.$http.get(api_name, { params });
      this.table.total = data.num_results;
      this.table.loading = false;

      this.table.data = data.objects.map((v, i) => {
        v._index = data.num_results - i - (page - 1) * itemsPerPage;
        return v;
      });
    },

    changeServer(){
      this.selected_server = this.servers_array.find(v=>v.server_name == this.selected_server)
      this.query();
    },
    getHeader(){
      if(this.selected_server.server_id == 1){
        return this.table.headers
      }else if(this.selected_server.server_id == 2){
        return this.table.headers_usb
      }else if(this.selected_server.server_id == 3){
        return this.table.headers_uselog
      }
      return this.table.headers
    }
  },
  mounted() {
    this.selected_server = this.servers_array[0]
  },
  computed: {
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
          { text: "매뉴명", value: "menu_name", sortable: false},
          { text: "활동명", value: "action_name", sortable: false,align: "center" },
          { text: "활동결과", value: "action_result", sortable: false,align: "center" },
          { text: "아이디", value: "user_id", sortable: false,align: "center" },
          { text: "이름", value: "user_name", sortable: false,align: "center" },
          { text: "IP", value: "ipaddress", sortable: false,align: "center" },
          { text: "활동일자", value: "action_date", sortable: false,align: "center" },
        ],
        headers_usb: [
          { text: "No.", value: "id", sortable: false, width: 40 },
          { text: "디바이스번호", value: "device_no", sortable: false},
          { text: "시리얼번호", value: "serial_no", sortable: false,align: "center" },
          { text: "아이디", value: "user_id", sortable: false,align: "center" },
          { text: "이름", value: "user_name", sortable: false,align: "center" },
          { text: "IP", value: "ipaddress", sortable: false,align: "center" },
          { text: "MAC", value: "mac", sortable: false,align: "center" },
          { text: "구분", value: "inout_type", sortable: false,align: "center" },
          { text: "결과", value: "result", sortable: false,align: "center" },
          { text: "발생일자", value: "logdt", sortable: false,align: "center" },
        ],
        headers_uselog: [
          { text: "No.", value: "id", sortable: false, width: 40 },
          { text: "부서명", value: "dept_name", sortable: false},
          { text: "아이디", value: "user_id", sortable: false,align: "center" },
          { text: "이름", value: "user_name", sortable: false,align: "center" },
          { text: "IP", value: "ipaddress", sortable: false,align: "center" },
          { text: "파일명", value: "hwdata", sortable: false,align: "center" },
          { text: "구분", value: "agent_status", sortable: false,align: "center" },
          { text: "매체명", value: "hw_name", sortable: false,align: "center" },
          { text: "파일크기", value: "file_size", sortable: false,align: "center" },
          { text: "사용결과", value: "use_result", sortable: false,align: "center" },
          { text: "사용일시", value: "logtime", sortable: false,align: "center" },
        ],
        loading: false,
        total: 0,
        options: {},
        data: [],
      },
      selected_server:null,
      servers_array : [
        {"server_name":"PC보안서버","server_id":1},
        {"server_name":"USB관리서버","server_id":2},
        {"server_name":"매체제어서버","server_id":3},
      ]
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
</style>