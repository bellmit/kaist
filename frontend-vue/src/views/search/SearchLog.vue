<template>
  <div>
    <CCard>
      <v-app class="sr-card-app-title">
        <CCardHeader>
          <CIcon name="cil-justify-center"/>
          <strong> 통합보안 로그 검색 / 지능형 보안검색</strong>
        </CCardHeader>
        <CCardBody>
          <CNavbar
              expandable="md"
              color="light"
          >
            <CToggler inNavbar @click="show=!show"/>
            <CCol sm="11">
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
        <v-card flat tile color="grey lighten-4" class="mb-1" v-for="(item,index) in table.data">
          <v-card-title class="pb-1">
            <div class="report-title">
              <v-avatar color="blue-grey darken-2" size="36"><span class="white--text">{{index + 1}}</span></v-avatar>
              <div class="ml-3 d-flex report-title-wrap">
                <div class="report-title-text">
                  <div class="text-subtitle-1">{{item.detect_object.desc}}</div>
                  <div class="d-flex justify-space-between">
                    <div class="report-labels">
                      <v-chip small label class="v-chip-m">이름:{{item.account_info.name}}</v-chip>
                      <v-chip small label class="v-chip-m">아이디:{{item.account_info.id}}</v-chip>
                      <v-chip small label class="v-chip-m">부서:{{item.account_info.dept_name}}</v-chip>
                      <v-chip small label class="v-chip-m">IP:{{item.src_ip}}</v-chip>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </v-card-title>
          <v-divider/>
          <v-list-item three-line>
            <v-list-item-content>
              <span class="text-body-2 grey--text text--darken-2">{{item}}</span>
            </v-list-item-content>
          </v-list-item>
        </v-card>
<!--        <v-data-table-->
<!--            height="calc(100vh-50vh)"-->
<!--            hide-default-header-->
<!--            :items="table.data"-->
<!--            :server-items-length="table.total"-->
<!--            :loading="table.loading"-->
<!--            :options.sync="table.options"-->
<!--            :footer-props="{ 'items-per-page-options': [20, 40, 60] }"-->
<!--            class="elevation-1"-->
<!--            @click:row="clickRowHandler"-->
<!--        >-->
<!--          -->
<!--          <template v-slot:item="row">-->
<!--&lt;!&ndash;            <tr>&ndash;&gt;-->
<!--&lt;!&ndash;              <td>&ndash;&gt;-->
<!--&lt;!&ndash;                <span class="h5">{{ row.item.action_name}}</span>&ndash;&gt;-->
<!--&lt;!&ndash;               <div class="d-bar"></div>&ndash;&gt;-->
<!--&lt;!&ndash;              </td>&ndash;&gt;-->
<!--&lt;!&ndash;            </tr>&ndash;&gt;-->
<!--          </template>-->
<!--        </v-data-table>-->
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

      if (this.filter.querystring) {
        filters_and.push({name: 'log_msg', op: 'like', val: "%"+this.filter.querystring+"%"})
      }


      let q = {
        filters: [{and: filters_and}],
        order_by: [{field: 'id', direction: 'asc'}]
      };

      let params = {
        q: JSON.stringify(q),
        page: page,
        results_per_page: itemsPerPage,
      };

      let { data } = await this.$http.get("logdata", { params });
      this.table.total = data.num_results;
      this.table.loading = false;

      this.table.data = data.objects.map((v, i) => {
        v._index = data.num_results - i - (page - 1) * itemsPerPage;
        return JSON.parse(v.log_msg);
      });

    },
  },
  mounted() {
    this.query();
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
  height:150px;
}
.sr-card-app-title{
  height:160px;
}

td {
  padding: 1px 1px;
  font-size: 14px;
  height: 48px;
  line-height: 80px;
}
.d-bar{
  height:2px;
  background-color: lightgray;
}
.report-title {
  width: 100%;
  display: flex;
  .report-title-wrap {
    position: relative;
    flex: 1 1 auto;
  }
  .report-title-text {
    flex: 1 0 100%;
    width: 100%;
  }
  .report-actions {
    // position: absolute;
    // right: 0; top: 0;
    // width: 220px;
    // text-align: right;
    // display: flex;
    //text-align: right !important;
  }
}
.v-chip-m{
  margin-left: 2px;
}
</style>