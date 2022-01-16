<template>
  <CChartPie
    :datasets="defaultDatasets"
    :labels="['검증결과[ 100%]']"
  />
</template>

<script>
import { CChartPie } from '@coreui/vue-chartjs'

export default {
  name: 'CChartPieExample3',
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
          data: [100]
        }
      ]
    }
  }
}
</script>
