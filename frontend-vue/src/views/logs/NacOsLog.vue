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

      let { data } = await this.$http.get("log_nac_os", { params });
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
          { text: "ID", value: "id", sortable: false, width: 40 },
          { text: "IP 주소", value: "ipaddress", sortable: false },
          { text: "MAC 주소", value: "mac", sortable: false },
          { text: "인증사용자", value: "auth_user_name", sortable: false },
          { text: "부서", value: "dept_name", sortable: false },
          { text: "운영체제명", value: "os_name", sortable: false },
          { text: "버전", value: "os_version", sortable: false },
          { text: "서비스팩", value: "os_service_pack", sortable: false },
          { text: "IE버전", value: "ie_version", sortable: false }
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
