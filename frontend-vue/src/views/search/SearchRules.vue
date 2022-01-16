<template>
  <div>
    <CCard>
      <v-app class="sr-card-app-title">
        <CCardHeader>
          <CIcon name="cil-justify-center"/>
          <strong> 시나리오별 탐지 검색 </strong>
        </CCardHeader>
        <CCardBody>
          <CNavbar
              expandable="md"
              color="light"
          >
            <CToggler inNavbar @click="show=!show"/>
            <CCol sm="2">
              <v-select outlined dense hide-details
                        v-model="selected_rule"
                        :items="rules_array"
                        label="보안 룰"
                        item-text="rule_name"
                        item-value=""
                        @change="changeRules"
              />
            </CCol>
            <CCol sm="2">
              <v-select outlined dense hide-details
                        v-model="selected_rule_data"
                        :items="rules_datas"
                        label="탐지 내용"
                        item-text="desc"
                        item-value=""
              />
            </CCol>
            <CCol sm="6">
              <v-text-field outlined dense hide-details
                            placeholder="검색어를 입력하세요"
                            append-icon="mdi-magnify"
                            v-model="filter.querystring"
                            @keydown.enter="query()"
                            class="m-right"
              />
            </CCol>
            <CCol sm="2">
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
            height="calc(100vh-50vh)"
            :headers="table.headers"
            :items="table.data"
            :server-items-length="table.total"
            :loading="table.loading"
            :options.sync="table.options"
            :footer-props="{ 'items-per-page-options': [5,20, 40, 60] }"
            class="elevation-1"
            @click:row="clickRowHandler"
        >
          <template v-slot:[`item.id`]="{ item }">
            {{ item._index }}
          </template>
        </v-data-table>
      </v-app>
    </CCard>
    <CCard>
      <v-app class="sr-card-app">
        <v-data-table
            height="calc(100vh-120vh)"
            :headers="table_detail.headers"
            :items="table_detail.data"
            :server-items-length="table_detail.total"
            :loading="table_detail.loading"
            :options.sync="table_detail.options"
            :footer-props="{ 'items-per-page-options': [5,20, 40, 60] }"
            class="elevation-1"
        >
          <template v-slot:[`item.id`]="{ item }">
            {{ item._index }}
          </template>
          <template v-slot:[`item.created_date`]="{ item }">
            {{ JSON.parse(item.log_msg).created_date[0] }}
          </template>
          <template v-slot:[`item.user_id`]="{ item }">
            {{ JSON.parse(item.log_msg).account_info.id }}
          </template>
          <template v-slot:[`item.user_name`]="{ item }">
            {{ JSON.parse(item.log_msg).account_info.name }}
          </template>
          <template v-slot:[`item.dept_name`]="{ item }">
            {{ JSON.parse(item.log_msg).account_info.dept_name }}
          </template>
          <template v-slot:[`item.src_ip`]="{ item }">
            {{ JSON.parse(item.log_msg).src_ip }}
          </template>
          <template v-slot:[`item.src_port`]="{ item }">
            {{ JSON.parse(item.log_msg).src_port }}
          </template>
          <template v-slot:[`item.detect_object`]="{ item }">
            {{ JSON.parse(item.log_msg).detect_object.desc }}
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

      if(this.selected_rule.rule_name != '전체') {
        filters_and.push({name: 'fk_rule_id', op: 'eq', val: this.selected_rule.rule_id})
      }

      let q = {
        filters: [{and: filters_and}],
        order_by: [{field: 'id', direction: 'asc'}]
      };

      if (this.filter.querystring) {
        filters_and.push({name: 'detect_logs_data', op: 'like', val: "%"+this.selected_rule.rule_id+"%"})
      }

      let params = {
        q: JSON.stringify(q),
        page: page,
        results_per_page: itemsPerPage,
      };

      let { data } = await this.$http.get("detectedruledata", { params });
      this.table.total = data.num_results;
      this.table.loading = false;

      this.table.data = data.objects.map((v, i) => {
        v._index = data.num_results - i - (page - 1) * itemsPerPage;
        return v;
      });
    },
    async clickRowHandler(item){
      const { page, itemsPerPage } = this.table_detail.options;
      this.table_detail.loading = true;
      let filters = []
      let id_list = JSON.parse(item.detect_logs_data)
      // alert(id_list)
      id_list.map(v=>filters.push({name: 'id', op: 'eq', val: v}))
      let q = {
        filters: [{or: filters}]
      }
      let params = {
        q: q,
        results_per_page: 20,
        page: 1,
      };
      let { data } = await this.$http.get("logdata", { params });
      this.table_detail.total = data.num_results;
      this.table_detail.loading = false;

      this.table_detail.data = data.objects.map((v, i) => {
        v._index = data.num_results - i - (page - 1) * itemsPerPage;
        return v;
      });
    },
    changeRules(){
      this.rules_datas = this.rules_array.find(v=>v.rule_name == this.selected_rule).rule_data
      this.selected_rule = this.rules_array.find(v=>v.rule_name == this.selected_rule)
      this.query();
    }
  },
  mounted() {
    this.selected_rule = this.rules_array[0]
    this.rules_datas = this.rules_array[0].rule_data
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
          { text: "시나리오 이름", value: "security_rules.rule_name", sortable: false},
          { text: "위반 사항", value: "rule_sub_desc", sortable: false,
            align: "center" },
          { text: "점검일시", value: "created_date", sortable: false,
            align: "center" },
        ],
        loading: false,
        total: 0,
        options: {},
        data: [],
      },
      table_detail: {
        headers: [
          { text: "No.", value: "id", sortable: false, width: 40 },
          { text: "생성일", value: "created_date", sortable: false},
          { text: "아이디", value: "user_id", sortable: false,align: "center" },
          { text: "이름", value: "user_name", sortable: false,align: "center" },
          { text: "부서", value: "dept_name", sortable: false,align: "center" },
          { text: "IP", value: "src_ip", sortable: false,align: "center" },
          { text: "port", value: "src_port", sortable: false,align: "center" },
          { text: "탐지내용", value: "detect_object", sortable: false,align: "center" },
        ],
        loading: false,
        total: 0,
        options: {},
        data: [],
      },
      selected_rule:null,
      selected_rule_data:null,
      rules_datas:null,
      rules_array : [
        {"rule_name":"전체","rule_id":0,"rule_data":[{"code":"A000","desc":"전체"}]},
        {"rule_name":"인증(Identification)","rule_id":1,"rule_use":1,"rule_data":[
            {"code":"R000","desc":"전체"},
            {"code":"R001","desc":"IP별 부서정보 일치?"},
            {"code":"R002","desc":"LDAP 서버 존재?"},
            {"code":"R003","desc":"IP별 이름이 일치?"},
            {"code":"R004","desc":"보안시스템과 LDAP 연동 가능?"},
          ]},
        {"rule_name":"IP / MAC Violation","rule_id":2,"rule_use":1,"rule_data":[
            {"code":"R100","desc":"전체"},
            {"code":"R101","desc":"고정 IP 할당?"},
            {"code":"R102","desc":"IP는 동일 MAC 다름?"},
            {"code":"R103","desc":"NAC 인증 성공/실패 확인"},
            {"code":"R104","desc":"NAC SW 설치 정보"},
            {"code":"R105","desc":"NAC OS 설치 정보"},
            {"code":"R106","desc":"NAC IE 설치 정보"},
            {"code":"R107","desc":"PMS 백신 설지/점검 정보"},
            {"code":"R108","desc":"매체제어 매체 사용 확인"},
            {"code":"R109","desc":"보안감사 사용자 활동 이력 점검"},
            {"code":"R110","desc":"IP는 다르지만 MAC은 동일"},
          ]},
        {"rule_name":"NAC violation","rule_id":3,"rule_use":1,"rule_data":[
            {"code":"R200","desc":"전체"},
            {"code":"R201","desc":"NAC 인증실패?(특정기간 횟수 초과)"},
            {"code":"R202","desc":"NAC ID별 IP 변경 이력 존재?(특정기간 횟수 초과)"},
            {"code":"R203","desc":"IP별 OS/IE 버전 일치"},
            {"code":"R204","desc":"할당 IP별 Mac 변경 이력 존재?(특정기간 횟수 초과)"},
            {"code":"R205","desc":"사용자 변경 여부 확인"},
            {"code":"R206","desc":"Pc 변경 여부 확인"},
            {"code":"R207","desc":"매체제어 : 매체 사용 확인"},
            {"code":"R208","desc":"보안usb 사용 내역 확인"},
            {"code":"R209","desc":"보안usb 사용 내역 확인"},
          ]},
        {"rule_name":"Safety USB used violation","rule_id":4,"rule_use":1,"rule_data":[
            {"code":"R300","desc":"전체"},
            {"code":"R301","desc":"Usb 인증 실패?(특정기간 횟수 초과)"},
            {"code":"R302","desc":"사용자 변경 여부 확인"},
            {"code":"R303","desc":"보안usb 분실 여부 확인"},
            {"code":"R304","desc":"보안usb별 내외부 접속 여부 확인"},
            {"code":"R305","desc":"보안USB별 내부 IP/MAC 정보 확인"},
          ]},
        {"rule_name":"Media used violation","rule_id":5,"rule_use":1,"rule_data":[
            {"code":"R400","desc":"전체"},
            {"code":"R401","desc":"비허가 매체 반복 사용?(특정기간내 횟수 또는 종류)"},
            {"code":"R402","desc":"사용자 정보 확인"},
            {"code":"R403","desc":"매체 사용 권한 확인(RO/RW 등)"},
            {"code":"R404","desc":"파일경로/파일크기 확인"},
            {"code":"R405","desc":"보안usb 사용 내역 확인"},
            {"code":"R406","desc":"Nac violation 이력 : pc 변경, 로그인 실패 "},
            {"code":"R407","desc":"감사로그 : 로그인 실패 횟수, 권한 변경"},
          ]},
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