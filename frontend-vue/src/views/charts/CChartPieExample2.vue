<template>
  <CChartPie
    :datasets="defaultDatasets"
    :labels="['검증결과[ 98%]']"
  />
</template>

<script>
import { CChartPie } from '@coreui/vue-chartjs'

export default {
  name: 'CChartPieExample2',
  components: { CChartPie },
  computed: {
    defaultDatasets () {
      return [
        {
          backgroundColor: [
            '#FF00FF',
            '#E46651',
            '#00D8FF',
            '#DD1B16',
            '#FF00FF'
          ],
          data: [98]
        }
      ]
    }
  }
}
</script>
