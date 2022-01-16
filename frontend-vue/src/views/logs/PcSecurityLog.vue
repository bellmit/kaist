<template>
  <v-app>
    <div>
      <v-data-table
          height="calc(100vh-120vh)"
          :headers="table.headers"
          :items="table.data"
          :server-items-length="table.total"
          :loading="table.loading"
          :options.sync="table.options"
          :footer-props="{ 'items-per-page-options': [5,20, 40, 60] }"
          class="elevation-1"
      >
        <template v-slot:[`item.id`]="{ item }">
          {{ item._index }}
        </template>
      </v-data-table>
    </div>
  </v-app>

</template>

<script>
export default {
  methods: {
    async query() {
      this.table.loading = true;
      const { page, itemsPerPage } = this.table.options;

      let q = {
        filters: [
          {
            or: [
            ],
          },
        ],
        order_by: [{field: 'id', direction: 'asc'}]
      };

      if (this.filter.querystring) {
        q.filters.push({
          or: [
            {
              name: "user_name",
              op: "like",
              val: `%${this.filter.querystring}%`
            }
          ],
        });
      }

      let params = {
        q: JSON.stringify(q),
        page: page,
        results_per_page: itemsPerPage,
      };

      let { data } = await this.$http.get("log_asm", { params });
      this.table.total = data.num_results;
      this.table.loading = false;

      this.table.data = data.objects.map((v, i) => {
        v._index = data.num_results - i - (page - 1) * itemsPerPage;
        return v;
      });
    },
    shuffleArray (array) {
      for (let i = array.length - 1; i > 0; i--) {
        let j = Math.floor(Math.random() * (i + 1))
        let temp = array[i]
        array[i] = array[j]
        array[j] = temp
      }
      return array
    },
  },
  mounted() {
    this.query();
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
          { text: "이름", value: "user_name", sortable: false, width: 75 },
          { text: "컴퓨터 이름", value: "pc_name", sortable: false,
            align: "center" },
          { text: "IP", value: "ipaddress", sortable: false,
            align: "center" },
          { text: "부서명", value: "full_path", sortable: false,
            align: "center", width: 180 },
          { text: "점검일시", value: "update_date", sortable: false,
            align: "center" },
          { text: "점수", value: "score", sortable: false,
            align: "center" },
          { text: "백신설치", value: "check_vir_install", sortable: false,
            align: "center" },
          { text: "백신보안", value: "check_vir_secure", sortable: false,
            align: "center" },
          { text: "암호안전성", value: "check_pass_valid", sortable: false,
            align: "center" },
          { text: "암호변경", value: "check_pass_change", sortable: false,
            align: "center" },
          { text: "화면보호기", value: "check_screen", sortable: false,
            align: "center" },
          { text: "공유폴더", value: "check_share_dir", sortable: false,
            align: "center" },
          { text: "USB", value: "check_usb_autorun", sortable: false,
            align: "center" },
          { text: "ActiveX", value: "check_activex", sortable: false,
            align: "center" },
          { text: "비인가 프로그램", value: "check_invalid_program", sortable: false,
            align: "center" }
        ],
        loading: false,
        total: 0,
        options: {},
        data: [],
      },
    };
  },
};
</script>

<style lang="scss" scoped>
.main-panel {
  padding: 10px;
  height: calc(100vh - 100px);
  overflow-y: auto;
}
.search-action {
  flex: 0 0 120px;
  margin-left: 10px;
  display: flex;
  align-items: center;
}
.h-ext{
  height:600px;
}
</style>
