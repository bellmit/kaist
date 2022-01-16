<template>
  <div>
    <CRow>
      <CCol sm="6" md="4">
        <CCard>
          <CCardHeader>
            {{ servers.fw.server_name }}
            <CSwitch
                class="float-right"
                size="sm"
                shape="pill"
                color="info"
                data-on="On"
                data-off="Off"
                :checked="true"
            />
          </CCardHeader>
          <CCardBody>
            <CInput
                label="서버 IP : "
                value="Username"
                v-model="servers.fw.server_ip"
                horizontal
                disabled
                size="sm"
            />
            <CInput
                label="접속 계정 : "
                value="아이디"
                v-model="servers.fw.admin_id"
                horizontal
                disabled
                size="sm"
            />
            <CSelect
                label="서버유형"
                size="sm"
                horizontal
                :options="server_types"
                placeholder="Please select"
                custom
                v-model="server_types[servers.fw.server_type]"
                disabled
            />
          </CCardBody>
        </CCard>
      </CCol>
      <CCol sm="6" md="4">
        <CCard>
          <CCardHeader>
            {{ servers.nac.server_name }}
            <CSwitch
                class="float-right"
                size="sm"
                shape="pill"
                color="info"
                data-on="On"
                data-off="Off"
                :checked="true"
            />
          </CCardHeader>
          <CCardBody>
            <CInput
                label="서버 IP : "
                value="Username"
                v-model="servers.nac.server_ip"
                horizontal
                disabled
                size="sm"
            />
            <CInput
                label="접속 계정 : "
                value="아이디"
                v-model="servers.nac.admin_id"
                horizontal
                disabled
                size="sm"
            />
            <CSelect
                label="서버유형"
                size="sm"
                horizontal
                :options="server_types"
                placeholder="Please select"
                custom
                v-model="server_types[servers.nac.server_type]"
                disabled
            />
          </CCardBody>
        </CCard>
      </CCol>
      <CCol sm="6" md="4">
        <CCard>
          <CCardHeader>
            {{ servers.dlp.server_name }}
            <CSwitch
                class="float-right"
                size="sm"
                shape="pill"
                color="info"
                data-on="On"
                data-off="Off"
                :checked="true"
            />
          </CCardHeader>
          <CCardBody>
            <CInput
                label="서버 IP : "
                value="Username"
                v-model="servers.dlp.server_ip"
                horizontal
                disabled
                size="sm"
            />
            <CInput
                label="접속 계정 : "
                value="아이디"
                v-model="servers.dlp.admin_id"
                horizontal
                disabled
                size="sm"
            />
            <CSelect
                label="서버유형"
                size="sm"
                horizontal
                :options="server_types"
                placeholder="Please select"
                custom
                v-model="server_types[servers.dlp.server_type]"
                disabled
            />
          </CCardBody>
        </CCard>
      </CCol>
      <CCol sm="6" md="4">
        <CCard>
          <CCardHeader>
            {{ servers.pms.server_name }}
            <CSwitch
                class="float-right"
                size="sm"
                shape="pill"
                color="info"
                data-on="On"
                data-off="Off"
                :checked="true"
            />
          </CCardHeader>
          <CCardBody>
            <CInput
                label="서버 IP : "
                value="Username"
                v-model="servers.pms.server_ip"
                horizontal
                disabled
                size="sm"
            />
            <CInput
                label="접속 계정 : "
                value="아이디"
                v-model="servers.pms.admin_id"
                horizontal
                disabled
                size="sm"
            />
            <CSelect
                label="서버유형"
                size="sm"
                horizontal
                :options="server_types"
                placeholder="Please select"
                custom
                v-model="server_types[servers.pms.server_type]"
                disabled
            />
          </CCardBody>
        </CCard>
      </CCol>
      <CCol sm="6" md="4">
        <CCard>
          <CCardHeader>
            {{ servers.vms.server_name }}
            <CSwitch
                class="float-right"
                size="sm"
                shape="pill"
                color="info"
                data-on="On"
                data-off="Off"
                :checked="true"
            />
          </CCardHeader>
          <CCardBody>
            <CInput
                label="서버 IP : "
                value="Username"
                v-model="servers.vms.server_ip"
                horizontal
                disabled
                size="sm"
            />
            <CInput
                label="접속 계정 : "
                value="아이디"
                v-model="servers.vms.admin_id"
                horizontal
                disabled
                size="sm"
            />
            <CSelect
                label="서버유형"
                size="sm"
                horizontal
                :options="server_types"
                placeholder="Please select"
                custom
                v-model="server_types[servers.vms.server_type]"
                disabled
            />
          </CCardBody>
        </CCard>
      </CCol>
      <CCol sm="6" md="4">
        <div style="min-height: 200px;inline-size: 400px;margin-top: 100px;margin-left: 200px">
          <v-icon x-large @click="dialog.show=true"> mdi-plus</v-icon>
        </div>

      </CCol>

    </CRow>
    <v-app>
      <v-dialog v-model="dialog.show" persistent max-width="600px">
        <v-card>
          <v-card-title class="pt-2 pb-1 primary white--text">
            <span class="body-1">수집 서버 추가</span>
          </v-card-title>
          <v-divider />
          <v-card-text>
            <v-container>
              <v-row>
                <v-col cols="12" sm="6">
                  <v-text-field outlined dense hide-details
                                label="수집서버 이름"
                                placeholder="이름"
                                onKeyup="this.value=this.value.replace(/[^0-9]/g,'');"
                  />
                </v-col>
                <v-col cols="12" sm="6">
                  <v-text-field outlined dense hide-details
                                label="수집서버 IP"
                                placeholder="0.0.0.0"
                                onKeyup="this.value=this.value.replace(/[^0-9]/g,'');"
                  />
                </v-col>
                <v-col cols="12" sm="6">
                  <v-text-field outlined dense hide-details
                                label="접속계정"
                                placeholder="admin"
                  />
                </v-col>
                <v-col cols="12" sm="6">
                  <v-text-field outlined dense hide-details
                                label="계정암호"
                                placeholder="*********"
                  />
                </v-col>
                <v-col cols="12" sm="12">
                  <CSelect
                      label="서버유형"
                      size="sm"
                      horizontal
                      :options="server_types"
                      placeholder="Please select"
                      custom
                  />
                </v-col>
              </v-row>
            </v-container>
          </v-card-text>
          <v-card-actions>
            <v-btn
                color="light-blue darken-2"
                class="flex-grow-1"
                text
                @click="dialog.show=false"
            >
              닫기
            </v-btn>
            <v-btn
                color="light-blue darken-2"
                class="flex-grow-1"
                tile
                dark
                depressed
                @click="dialog.show=false"
            >
              추가
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
    </v-app>
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
      ],
      dialog:{
        show:false
      }
    }
  }
}
</script>
