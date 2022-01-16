<template>
  <div>
    <CRow>
      <CCol  md="6">
        <CCard>
          <CCardHeader>
            <CIcon name="cil-justify-center"/>
            <strong> {{rules.ident.rule_name}}</strong>
            <small>(위반건수 : 100건)</small>
          </CCardHeader>
          <CCardBody>
            <CListGroup>
              <CListGroupItem v-for="(item, index) in JSON.parse(rules.ident.rule_data)"
                  class="d-flex justify-content-between align-items-center"
              >
                {{item.desc}}
                <CBadge color="primary" shape="pill">{{ getRandomData() }}</CBadge>
              </CListGroupItem>
            </CListGroup>
          </CCardBody>
        </CCard>
      </CCol>
      <CCol md="6">
        <CCard>
          <CCardHeader>
            <CIcon name="cil-justify-center"/>
            <strong> {{rules.usb.rule_name}}</strong>
            <small>(위반건수 : 100건)</small>
          </CCardHeader>
          <CCardBody>
            <CListGroup>
              <CListGroupItem v-for="(item, index) in JSON.parse(rules.usb.rule_data)"
                              class="d-flex justify-content-between align-items-center"
              >
                {{item.desc}}
                <CBadge color="primary" shape="pill">{{ getRandomData() }}</CBadge>
              </CListGroupItem>
            </CListGroup>
          </CCardBody>
        </CCard>
      </CCol>
      <CCol md="6">
        <CCard>
          <CCardHeader>
            <CIcon name="cil-justify-center"/>
            <strong> {{rules.ipmac.rule_name}}</strong>
            <small>(위반건수 : 100건)</small>
          </CCardHeader>
          <CCardBody>
            <CListGroup>
              <CListGroupItem v-for="(item, index) in JSON.parse(rules.ipmac.rule_data)"
                              class="d-flex justify-content-between align-items-center"
              >
                {{item.desc}}
                <CBadge color="primary" shape="pill">{{ getRandomData() }}</CBadge>
              </CListGroupItem>
            </CListGroup>
          </CCardBody>
        </CCard>
      </CCol>

      <CCol md="6">
        <CCard>
          <CCardHeader>
            <CIcon name="cil-justify-center"/>
            <strong> {{rules.nac.rule_name}}</strong>
            <small>(위반건수 : 100건)</small>
          </CCardHeader>
          <CCardBody>
            <CListGroup>
              <CListGroupItem v-for="(item, index) in JSON.parse(rules.nac.rule_data)"
                              class="d-flex justify-content-between align-items-center"
              >
                {{item.desc}}
                <CBadge color="primary" shape="pill">{{ getRandomData() }}</CBadge>
              </CListGroupItem>
            </CListGroup>
          </CCardBody>
        </CCard>
      </CCol>

      <CCol md="6">
        <CCard>
          <CCardHeader>
            <CIcon name="cil-justify-center"/>
            <strong> {{rules.mediause.rule_name}}</strong>
            <small>(위반건수 : 100건)</small>
          </CCardHeader>
          <CCardBody>
            <CListGroup>
              <CListGroupItem v-for="(item, index) in JSON.parse(rules.mediause.rule_data)"
                              class="d-flex justify-content-between align-items-center"
              >
                {{item.desc}}
                <CBadge color="primary" shape="pill">{{ getRandomData() }}</CBadge>
              </CListGroupItem>
            </CListGroup>
          </CCardBody>
        </CCard>
      </CCol>
    </CRow>
  </div>
</template>

<script>

export default {
  name: 'SecureRules',
  methods :{
    async getSecureRules(){
      let params = {
        page: 1,
        results_per_page: 20,
      }

      let { data } = await this.$http.get("securerules", { params })
      this.rules.ident = data.objects[0]
      this.rules.ipmac = data.objects[1]
      this.rules.nac = data.objects[2]
      this.rules.usb = data.objects[3]
      this.rules.mediause = data.objects[4]
    },
    getRandomData(){
      return Math.round(Math.random() * (100 - 20) + 20);
    }
  },
  mounted() {
    this.getSecureRules();

  },
  data: function () {
    return {
      show: true,
      isCollapsed: true,
      rules : {
        ident:null,
        ipmac:null,
        nac:null,
        usb:null,
        mediause:null
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
