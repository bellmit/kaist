<template>
  <div>
    <CRow>
      <CCol sm="6" lg="3">
        <CWidgetProgress footer="데이터 수집건수 : 20,1000건">
          <div class="h4 m-0">백신 DB 수집 에이전트</div>
          <div class="card-header-actions">
            <CSwitch
                class="float-right"
                size="sm"
                shape="pill"
                color="info"
                data-on="On"
                data-off="Off"
                :checked="true"
            />
          </div>
          <div>데이터 수집중...</div>
          <br>
          <CProgress class="mb-3">
            <CProgressBar color="success" :value="70" animated show-percentage/>
          </CProgress>
        </CWidgetProgress>
      </CCol>

      <CCol sm="6" lg="3">
        <CWidgetProgress footer="데이터 수집건수 : 120,1000건">
          <div class="h4 m-0">매체제어 서버 로그 수집 에이전트</div>
          <div class="card-header-actions">
            <CSwitch
                class="float-right"
                size="sm"
                shape="pill"
                color="info"
                data-on="On"
                data-off="Off"
                :checked="true"
            />
          </div>
          <div>데이터 수집중...</div>
          <br>
          <CProgress class="mb-3">
            <CProgressBar color="success" :value="30" animated show-percentage/>
          </CProgress>
        </CWidgetProgress>
      </CCol>
      <CCol sm="6" lg="3">
        <CWidgetProgress footer="데이터 수집건수 : 50,1000건">
          <div class="h4 m-0">인증서버 로그데이터 수집 에이전트</div>
          <div class="card-header-actions">
            <CSwitch
                class="float-right"
                size="sm"
                shape="pill"
                color="info"
                data-on="On"
                data-off="Off"
                :checked="true"
            />
          </div>
          <div>데이터 수집중...</div>
          <br>
          <CProgress class="mb-3">
            <CProgressBar color="success" :value="80" animated show-percentage/>
          </CProgress>
        </CWidgetProgress>
      </CCol>
    </CRow>

    <CRow>
      <CCol sm="6" lg="3">
        <CWidgetProgress footer="데이터 수집건수 : 40,1000건">
          <div class="h4 m-0">방화벽 syslog 데이터 수집 에이전트</div>
          <div class="card-header-actions">
            <CSwitch
                class="float-right"
                size="sm"
                shape="pill"
                color="info"
                data-on="On"
                data-off="Off"
                :checked="true"
            />
          </div>
          <div>데이터 수집중...</div>
          <br>
          <CProgress class="mb-3">
            <CProgressBar color="success" :value="30" animated show-percentage/>
          </CProgress>
        </CWidgetProgress>
      </CCol>

      <CCol sm="6" lg="3">
        <CWidgetProgress footer="데이터 수집건수 : 10,1000건">
          <div class="h4 m-0">NAC DB 로그 데이터 수집 에이전트</div>
          <div class="card-header-actions">
            <CSwitch
                class="float-right"
                size="sm"
                shape="pill"
                color="info"
                data-on="On"
                data-off="Off"
                :checked="true"
            />
          </div>
          <div>데이터 수집중...</div>
          <br>
          <CProgress class="mb-3">
            <CProgressBar color="success" :value="70" animated show-percentage/>
          </CProgress>
        </CWidgetProgress>
      </CCol>
      <CCol sm="6" lg="3">
        <CWidgetProgress footer="데이터 수집건수 : 70,1000건">
          <div class="h4 m-0">USB 관리서버 데이터 수집 에이전트</div>
          <div class="card-header-actions">
            <CSwitch
                class="float-right"
                size="sm"
                shape="pill"
                color="info"
                data-on="On"
                data-off="Off"
                :checked="true"
            />
          </div>
          <div>데이터 수집중...</div>
<!--          <CProgress-->
<!--              color="gradient-success"-->
<!--              :value="45"-->
<!--              class="progress-xs my-5 mb-0"-->
<!--              animated-->
<!--          />-->
          <br>
          <CProgress class="mb-3">
            <CProgressBar color="success" :value="50" animated show-percentage/>
          </CProgress>
        </CWidgetProgress>
      </CCol>
    </CRow>
  </div>
</template>
<script>

export default {
  name: 'Servers',
  methods :{
    async getServers(){
      let params = {
        page: 1,
        results_per_page: 20,
      }

      let { data } = await this.$http.get("servers", { params })
      this.servers.fw = data.objects[1]
      this.servers.nac = data.objects[13]
      this.servers.dlp = data.objects[14]
      this.servers.pms = data.objects[15]
      this.servers.vms = data.objects[12]
    }
  },
  mounted() {
    this.getServers();
  },
  data: function () {
    return {
      show: true,
      isCollapsed: true,
      loremIpsum: 'Lorem ipsum dolor sit amet, consectetuer adipiscing elit, sed diam nonummy nibh euismod tincidunt ut laoreet dolore magna aliquam erat volutpat. Ut wisi enim ad minim veniam, quis nostrud exerci tation ullamcorper suscipit lobortis nisl ut aliquip ex ea commodo consequat.',
      servers : {
        fw:null,
        vms:null,
        nac:null,
        dlp:null,
        pms:null
      },
      server_types:[
        "접근통재",
        "위협탐지",
        "PC보안",
        "인프라장비",
      ]
    }
  }
}
</script>
