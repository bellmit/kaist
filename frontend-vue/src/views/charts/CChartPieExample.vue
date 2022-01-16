<template>
  <CChartPie
    :datasets="defaultDatasets"
    :labels="['검증결과[ 99%]']"
  />
</template>

<script>
import { CChartPie } from '@coreui/vue-chartjs'

export default {
  name: 'CChartPieExample',
  components: { CChartPie },
  computed: {
    defaultDatasets () {
      return [
        {
          backgroundColor: [
            '#00D8FF',
            '#E46651',
            '#00D8FF',
            '#DD1B16',
            '#FF00FF'
          ],
          data: [99]
        }
      ]
    }
  }
}
</script>
