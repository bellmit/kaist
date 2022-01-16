<template>
      <div class="main-panel">
        <v-card-title>특허통계</v-card-title>
        <v-card-text>
          <v-row>
            <v-col cols="4">
              <v-card light color="blue-grey lighten-4">
                <v-card-title class="body-1 font-weight-bold py-2">최근 5년간 특허보유현황</v-card-title>
                <v-divider/>
                <v-card-text>
                  <highcharts constructor-type="chart" :options="pie1Option" />
                </v-card-text>
              </v-card>
            </v-col>
            <v-col cols="4">
              <v-card light color="blue-grey lighten-4">
                <v-card-title class="body-1 font-weight-bold py-2">기술분야별 특허보유현황</v-card-title>
                <v-divider/>
                <v-card-text>
                  <highcharts constructor-type="chart" :options="pie2Option" />
                </v-card-text>
              </v-card>
            </v-col>
            <v-col cols="4">
              <v-card light color="blue-grey lighten-4">
                <v-card-title class="body-1 font-weight-bold py-2">특허소유자별 특허보유현황(Top5)</v-card-title>
                <v-divider/>
                <v-card-text>
                  <highcharts constructor-type="chart" :options="pie3Option" />
                </v-card-text>
              </v-card>
            </v-col>
          </v-row>
          <v-row>
            <v-col cols="12">
              <v-card light color="blue-grey lighten-4">
                <v-card-title class="body-1 font-weight-bold py-2">기간별 특허 검색 조회건수</v-card-title>
                <v-divider/>
                <v-card-text>
                  <highcharts
                      constructor-type="chart"
                      :options="line1Option"
                  />
                </v-card-text>
              </v-card>
            </v-col>
          </v-row>
          <v-row>
            <v-col cols="12">
              <v-card light color="blue-grey lighten-4">
                <v-card-title class="body-1 font-weight-bold py-2">Top 10 검색어</v-card-title>
                <v-divider/>
                <v-card-text>
                  <highcharts
                      constructor-type="chart"
                      :options="chart1Option"
                  />
                </v-card-text>
              </v-card>
            </v-col>
          </v-row>
        </v-card-text>
      </div>
</template>

<script>
import _ from 'lodash'

const chartOptions = {
  chart: {backgroundColor: 'transparent', type: 'column', height: 200},
  title: {text: null},
  credits: {enabled: false},
  legend: {enabled: false},
  xAxis: {
    categories: []
  },
  yAxis: {title:{enabled: false}},
  series: [{
    data: [],
    name: 'data',
    maxPointWidth: 10
  }]
}

const lineOptions = {
  chart: {backgroundColor: 'transparent', type: 'area', height: 200},
  title: {text: null},
  credits: {enabled: false},
  legend: {enabled: false},
  xAxis: {
    categories: []
  },
  yAxis: {title:{enabled: false}},
  series: [{
    data: [],
    name: 'data',
    maxPointWidth: 10
  }]
}

const pieOptions = {
  chart: {backgroundColor: 'transparent', type: 'pie', height: 280},
  title: {text: null},
  credits: {enabled: false},
//   legend: {enabled: false},
  legend: {layout: 'horizontal'},
  plotOptions: {
    pie: {
      allowPointSelect: true,
      cursor: 'pointer',
      dataLabels: {
        enabled: true
      },
      showInLegend: true
    }
  },
  series: [{
    data: [],
    name: '점수비율(%)',
    colorByPoint: true
  }]
}

const pieOptions_tech_types = {
  colors: ['#003f5c', '#58508d','#bc5090', '#ff6361', '#ffa600','#aa3f5c', '#aa508d','#aa5090', '#aa6361', '#aaa600'],
  chart: {
    plotBackgroundColor: null,
    plotBorderWidth: null,
    plotShadow: false,
    type: 'pie',
    height: 280
  },
  title: {
    text: ''
  },
  tooltip: {
    pointFormat: '<b>{point.name}</b>: {point.y} 건'
  },
  accessibility: {
    point: {
      valueSuffix: '%'
    }
  },
  plotOptions: {
    pie: {
      allowPointSelect: true,
      cursor: 'pointer',
      dataLabels: {
        enabled: true,
        format: '<b>{point.name}</b>: {point.y} 건 '
      },
      showInLegend: true
    }
  },
  series: [{
    name: 'Brands',
    colorByPoint: true,
    data: []
  }],
}
export default {
  computed: {
    chart1Option () {
      let obj = _.cloneDeep(chartOptions)
      obj.xAxis.categories = this.data.search_rank_objs.map(v => v.search_string)
      obj.series[0].data = this.data.search_rank_objs.map(v => parseInt(v.count, 10))
      obj.series[0].name = '검색횟수'
      return obj
    },
    chart2Option () {
      let obj = _.cloneDeep(chartOptions)
      // obj.xAxis.categories = this.data.us.map(v => v.value)
      // obj.series[0].data = this.data.us.map(v => parseInt(v.value, 10))
      // obj.series[0].name = '검색횟수'
      return obj
    },
    pie1Option () {
      let obj = _.cloneDeep(pieOptions_tech_types)
      obj.series[0].data = this.data.apply_date_objs.map(v => ({name:v.apply_date,y:parseInt(v.count)}))
      obj.series[0].name = '연도별'
      return obj
    },
    pie2Option () {
      let obj = _.cloneDeep(pieOptions_tech_types)
      obj.series[0].data = this.data.tech_types_objs.map(v => ({name:this.$constant.tech_types.find(v2=>v2.value == v.tech_type).text,y:parseInt(v.count)}))
      obj.series[0].name = '기술분류'
      return obj
    },
    pie3Option () {
      let obj = _.cloneDeep(pieOptions_tech_types)
      obj.series[0].data = this.data.person_objs.map(v => ({name:v.person,y:parseInt(v.count)}))
      obj.series[0].name = '특허소유자'
      return obj
    },
    line1Option () {
      let obj = _.cloneDeep(lineOptions)
      obj.xAxis.categories = this.data.user_action_months_objs.map(v => v.month)
      obj.series[0].data = this.data.user_action_months_objs.map(v => parseInt(v.count))
      obj.series[0].name = '월별조회건수'
      return obj
    },
    line2Option () {
      let obj = _.cloneDeep(chartOptions)
      return obj
    }
  },
  mounted() {
    this.getStaticsReport()
  },
  methods : {
    async getStaticsReport () {
      console.log("getStaticsReport start")
      let { data } = await this.$http.get("statics_report", {});
      this.data.tech_types_objs = data['tech_types_objs']
      this.data.person_objs = data['person_objs']
      this.data.apply_date_objs = data['apply_date_objs']
      this.data.user_action_months_objs = data['user_action_months_objs']
      this.data.search_rank_objs = data['search_rank_objs']

      // this.data.tech_types_objs = data['tech_types_objs']
      // this.data.dept_objs = data['dept_objs']
      // this.data.check_items_objs = data['check_items_objs']
      // data['months_objs'].forEach((v) => {
      //   this.data.months_objs.push({
      //     key:v.key,
      //     value:v.value
      //   })
      // })
      // data['user_objs'].forEach((v) => {
      //   this.data.user_objs.push({
      //     key:v.key,
      //     value:v.value
      //   })
      // })
    }
  },
  data () {
    return {
      data: {
        lables:{
          align: 'right',
          rotation: 45,
          shape: null
        },
        tech_types_objs:[],
        person_objs:[],
        apply_date_objs:[],
        months_objs:[],
        user_action_months_objs:[],
        search_rank_objs:[],
      }
    }
  }
}
</script>

<style lang="scss" scoped>
.data-table-container {
  overflow-y: auto;
  height: calc(100vh - 105px);
}
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