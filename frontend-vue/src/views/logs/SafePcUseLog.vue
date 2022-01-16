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

      let { data } = await this.$http.get("log_safepc_uselog", { params });
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
          { text: "그룹", value: "group_name", sortable: false,
            align: "center" },
          { text: "아이디", value: "person_id", sortable: false,
            align: "center" },
          { text: "사용자명", value: "name", sortable: false,
            align: "center" },
          { text: "IP", value: "ipaddress", sortable: false,
            align: "center" },
          { text: "파일명", value: "hwdata", sortable: false,
            align: "center" },
          { text: "Agent 상태", value: "agent_status", sortable: false,
            align: "center" },
          { text: "매체명", value: "hw_name", sortable: false,
            align: "center" },
          { text: "파일크기", value: "file_size", sortable: false,
            align: "center" },
          { text: "구분", value: "use_result", sortable: false,
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
