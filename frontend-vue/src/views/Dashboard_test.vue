<template>
  <div>
    <CRow>
      <CCol md="12">
        <CCard>
          <CCardHeader>
            <span class="title text-v1">통합보안 로그파일(스팸메일) 정합성 테스트 결과</span>
          </CCardHeader>
          <CCardBody>
            <CRow>
              <CCol sm="6" lg="6">
                <ul class="horizontal-bars type-2">
                  <div class="progress-group">
                    <div class="progress-group-header">
                      <CIcon name="cil-globe-alt" class="progress-group-icon"/>
                      <span class="title text-v">Mail_log.txt 파일 검증 결과</span>
                      <span class="ml-auto font-weight-bold text-v">
                        2,000,000건 <span class="text-muted small text-v">(100%)</span>
                      </span>
                    </div>
                    <div class="progress-group-bars">
                      <CProgress
                          class="progress-xs"
                          :value="100"
                          color="success"
                      />
                    </div>
                  </div>
                  <br>
                  <div class="progress-group">
                    <div class="progress-group-header">
                      <CIcon name="cil-globe-alt" class="progress-group-icon"/>
                      <span class="title text-v">Documents.tsv 파일 검증 결과</span>
                      <span class="ml-auto font-weight-bold text-v">
                        500,000건 <span class="text-muted small text-v">(99%)</span>
                      </span>
                    </div>
                    <div class="progress-group-bars">
                      <CProgress
                          class="progress-xs"
                          :value="99"
                          color="success"
                      />
                    </div>
                  </div>
                  <br>
                  <div class="progress-group">
                    <div class="progress-group-header">
                      <CIcon name="cil-globe-alt" class="progress-group-icon"/>
                      <span class="title text-v">Querys.tsv 파일 검증 결과</span>
                      <span class="ml-auto font-weight-bold text-v">
                        68건 <span class="text-muted small text-v">(98%)</span>
                      </span>
                    </div>
                    <div class="progress-group-bars">
                      <CProgress
                        class="progress-xs"
                        :value="98"
                        color="success"
                      />
                    </div>
                  </div>
                  <br>
                  <div class="progress-group">
                    <div class="progress-group-header">
                      <CIcon name="cil-globe-alt" class="progress-group-icon"/>
                      <span class="title text-v text-v">Qrels.tsv 파일 검증 결과</span>
                      <span class="ml-auto font-weight-bold text-v">
                        12,987건 <span class="text-muted small text-v">(99%)</span>
                      </span>
                    </div>
                    <div class="progress-group-bars">
                      <CProgress
                        class="progress-xs"
                        :value="99"
                        color="success"
                      />
                    </div>
                  </div>
                  <br>
                  <div class="progress-group">
                    <div class="progress-group-header">
                      <CIcon name="cil-globe-alt" class="progress-group-icon"/>
                      <span class="title text-v text-v">MRR 스코어</span>
                      <span class="ml-auto font-weight-bold text-v">
                        0.2634 <span class="text-muted small text-v"></span>
                      </span>
                    </div>
                    <div class="progress-group-bars">
                      <CProgress
                        class="progress-xs"
                        :value="26"
                        color="success"
                      />
                    </div>
                  </div>
                </ul>
              </CCol>
            </CRow>
            <br/>
          </CCardBody>
        </CCard>
      </CCol>
    </CRow>
    <CRow>
      <CCol md="12">
        <CCard>
          <CCardBody>
            <CCard>
              <CRow>
                <CCol sm="6" lg="3">
                  <CCardHeader>mail_log.txt</CCardHeader>
                  <CCardBody><CChartPieExample3/></CCardBody>
                </CCol>
                <CCol sm="6" lg="3">
                  <CCardHeader>documents.tsv</CCardHeader>
                  <CCardBody><CChartPieExample/></CCardBody>
                </CCol>
                <CCol sm="6" lg="3">
                  <CCardHeader>querys.tsv</CCardHeader>
                  <CCardBody><CChartPieExample2/></CCardBody>
                </CCol>
                <CCol sm="6" lg="3">
                  <CCardHeader>qrels.tsv</CCardHeader>
                  <CCardBody><CChartPieExample/></CCardBody>
                </CCol>
              </CRow>
            </CCard>
          </CCardBody>
        </CCard>
      </CCol>
    </CRow>
  </div>
</template>

<script>
import MainChartExample from './charts/MainChartExample'
import WidgetsDropdown from './widgets/WidgetsDropdown'
import WidgetsBrand from './widgets/WidgetsBrand'
import CChartPieExample from './charts/CChartPieExample'
import CChartPieExample2 from './charts/CChartPieExample2'
import CChartPieExample3 from './charts/CChartPieExample3'
export default {
  name: 'Dashboard',
  components: {
    MainChartExample,
    WidgetsDropdown,
    WidgetsBrand,
    CChartPieExample,
    CChartPieExample2,
    CChartPieExample3
  },
  data () {
    return {
      selected: 'Month',
      tableItems: [
        {
          avatar: { url: 'img/avatars/1.jpg', status: 'success' },
          user: { name: 'Yiorgos Avraamu', new: true, registered: 'Jan 1, 2015' },
          country: { name: 'USA', flag: 'cif-us' },
          usage: { value: 50, period: 'Jun 11, 2015 - Jul 10, 2015' },
          payment: { name: 'Mastercard', icon: 'cib-cc-mastercard' },
          activity: '10 sec ago'
        },
        {
          avatar: { url: 'img/avatars/2.jpg', status: 'danger' },
          user: { name: 'Avram Tarasios', new: false, registered: 'Jan 1, 2015' },
          country: { name: 'Brazil', flag: 'cif-br' },
          usage: { value: 22, period: 'Jun 11, 2015 - Jul 10, 2015' },
          payment: { name: 'Visa', icon: 'cib-cc-visa' },
          activity: '5 minutes ago'
        },
        {
          avatar: { url: 'img/avatars/3.jpg', status: 'warning' },
          user: { name: 'Quintin Ed', new: true, registered: 'Jan 1, 2015' },
          country: { name: 'India', flag: 'cif-in' },
          usage: { value: 74, period: 'Jun 11, 2015 - Jul 10, 2015' },
          payment: { name: 'Stripe', icon: 'cib-stripe' },
          activity: '1 hour ago'
        },
        {
          avatar: { url: 'img/avatars/4.jpg', status: '' },
          user: { name: 'Enéas Kwadwo', new: true, registered: 'Jan 1, 2015' },
          country: { name: 'France', flag: 'cif-fr' },
          usage: { value: 98, period: 'Jun 11, 2015 - Jul 10, 2015' },
          payment: { name: 'PayPal', icon: 'cib-paypal' },
          activity: 'Last month'
        },
        {
          avatar: { url: 'img/avatars/5.jpg', status: 'success' },
          user: { name: 'Agapetus Tadeáš', new: true, registered: 'Jan 1, 2015' },
          country: { name: 'Spain', flag: 'cif-es' },
          usage: { value: 22, period: 'Jun 11, 2015 - Jul 10, 2015' },
          payment: { name: 'Google Wallet', icon: 'cib-google-pay' },
          activity: 'Last week'
        },
        {
          avatar: { url: 'img/avatars/6.jpg', status: 'danger' },
          user: { name: 'Friderik Dávid', new: true, registered: 'Jan 1, 2015' },
          country: { name: 'Poland', flag: 'cif-pl' },
          usage: { value: 43, period: 'Jun 11, 2015 - Jul 10, 2015' },
          payment: { name: 'Amex', icon: 'cib-cc-amex' },
          activity: 'Last week'
        }
      ],
      tableFields: [
        { key: 'avatar', label: '', _classes: 'text-center' },
        { key: 'user' },
        { key: 'country', _classes: 'text-center' },
        { key: 'usage' },
        { key: 'payment', label: 'Payment method', _classes: 'text-center' },
        { key: 'activity' },
      ]
    }
  },
  methods: {
    color (value) {
      let $color
      if (value <= 25) {
        $color = 'info'
      } else if (value > 25 && value <= 50) {
        $color = 'success'
      } else if (value > 50 && value <= 75) {
        $color = 'warning'
      } else if (value > 75 && value <= 100) {
        $color = 'danger'
      }
      return $color
    }
  }
}
</script>
<style scoped lang="scss">
.text-v{
  font-size: 20px;
  font-weight: bold;
}
.text-v1{
  font-size: 30px;
  font-weight: bold;
}
</style>