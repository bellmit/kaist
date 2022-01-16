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

      let { data } = await this.$http.get("log_safepc", { params });
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
          { text: "구분", value: "menu_name", sortable: false,
            align: "center" },
          { text: "조치사항", value: "action_name", sortable: false,
            align: "center" },
          { text: "조치결과", value: "action_result", sortable: false,
            align: "center" },
          { text: "아이디", value: "user_id", sortable: false,
            align: "center" },
          { text: "사용자명", value: "user_name", sortable: false,
            align: "center" },
          { text: "접속 주소", value: "ipaddress", sortable: false,
            align: "center" },
          { text: "처리일자", value: "action_date", sortable: false,
            align: "center" },
          { text: "처리내용", value: "action_contents_han", sortable: false,
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
