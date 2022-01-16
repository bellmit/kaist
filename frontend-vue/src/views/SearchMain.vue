<template>
  <v-app class="back_height">
    <div class="login-main">
<!--        <CButton color="secondary" class="login-btn" @click="$router.push('/login').catch(()=>{})">로그인</CButton>-->
        <CButton color="secondary" class="login-btn" @click="move_page">관리자 로그인</CButton>
        <div class="bg-log">
        </div>
        <div class="bg-title-1">
          기업과 기술을 이어주는
        </div>
        <div class="bg-title-2">
          한국생산기술연구원 <br>
          인공지능 특허정보 검색시스템
        </div>
        <div >
            <v-text-field
                          placeholder="검색어를 입력하세요"
                          @keydown.enter="move_search()"
                          class="search-bar"
                          v-model="search_string"
            />
        </div>
        <div class="search-btn" @click="move_search()"></div>
        <div class="techtrans-btn" @click="dialog.show=true"></div>
        <div class="notice-wrap">
          <div class="notice-header">
            소액기술
          </div>
          <div class="header-line"></div>
          <div class="py-3">
            <div v-for="item in smallpatent_datas" :key="item.id" class="notice-list-item" >
              <div class="notice-list-item-title">{{item.title}}</div>
              <div class="notice-list-item-title t-right">{{item.costcontents}}</div>
              <div class="item-line"></div>
            </div>
          </div>
        </div>
        <div class="popup-zone-area">
          <div class="popup-header">
            팝업존
          </div>
        </div>
        <div class="popup-body" @click="popupzone_move()" :key="popupzone_index">
          <CCard>
            <CCardHeader>
              팝업존이미지
            </CCardHeader>
            <CCardBody>
              <CCarousel
                  arrows
                  indicators
                  animate
                  width="400px"
                  height="250px"
              >
                <CCarouselItem
                    :image="getImageUrl(popupzone_image)"
                />
              </CCarousel>
            </CCardBody>
          </CCard>
        </div>
        <div class="popup-count">{{popupzone_index + 1 + '/' + popupzone_datas.length}}</div>
        <div class="popup-left" @click="popupzone_prev()" ></div>
        <div class="popup-right" @click="popupzone_next()"></div>
        <div class="smallpatent_plus" @click="move_smallpatent()"></div>
        <CContainer>
          <CRow class="justify-content-center">
          </CRow>
        </CContainer>
      <v-dialog v-model="dialog.show" persistent max-width="600px">
        <tech-trans-dialog :techtrans_data="null" @callBackTechTrans="onEmitTechTrans"/>
      </v-dialog>
    </div>
  </v-app>
</template>


<script>
import TechTransDialog from '@/components/TechTransDialog'
import AblTextarea from '@/components/AblTextarea'
export default {
  name: 'SearchMain',
  components: {AblTextarea,TechTransDialog},
  created() {
    this.$router.push('/')

  },
  mounted() {
    this.getSmallPatent();
    this.getPopupZone();
  },
  methods: {
    async getSmallPatent () {
      let filters_and = [];
      let param = {"and":filters_and};
      try {
        let q = JSON.stringify({
          filters: [param],
          order_by: [{field: 'created_date', direction: 'desc'}]
        })
        let params = {
          q: q,
          results_per_page: 5,
          page: 1,
        };

        let {data} = await this.$http.get('smallpatent', {params})
        this.smallpatent_datas = data.objects
      } catch (err) {
        console.error(err);
      } finally {
      }
    },
    async getPopupZone () {
      let filters_and = [];
      let param = {"and":filters_and};
      try {
        let q = JSON.stringify({
          filters: [param],
          order_by: [{field: 'created_date', direction: 'desc'}]
        })
        let params = {
          q: q,
          results_per_page: 5,
          page: 1,
        };

        let {data} = await this.$http.get('popupzone', {params})
        this.popupzone_datas = data.objects
        this.popupzone_image = this.popupzone_datas[0].contents
        this.popupzone_index = 0
      } catch (err) {
        console.error(err);
      } finally {
      }
    },
    popupzone_prev() {
      if(this.popupzone_index > 0) {
        this.popupzone_index -= 1
        this.popupzone_image = this.popupzone_datas[this.popupzone_index].contents
      }
    },
    popupzone_next() {
      if(this.popupzone_index < (this.popupzone_datas.length-1)) {
        this.popupzone_index += 1
        this.popupzone_image = this.popupzone_datas[this.popupzone_index].contents
      }
    },
    popupzone_move(){
      var win = window.open(this.popupzone_datas[this.popupzone_index].title, "_blank", "toolbar=yes,scrollbars=yes,resizable=yes,top=200,left=200,width=500,height=800")
    },
    onEmitTechTrans(type){
      if(type == "add")
        this.$session.$emit('modal-alert','기술이전 등록 요청하였습니다.')
      this.dialog.show = false
    },
    move_search(){

      if(this.search_string === ''){
        this.$session.$emit('modal-alert','검색어를 입력해 주세요!')
        return
      }
      this.$session.anyone_authorized = true
      this.$session.setSearchString(this.search_string)
      this.$router.push('search').catch(()=>{});
    },
    move_page(){
      this.$session.login_check = true
      this.$router.push('login').catch(()=>{});
    },
    move_smallpatent(){
      this.$session.anyone_authorized = true
      this.$router.push('manager/smallpatent').catch(()=>{});
    },
    getImageUrl(image_path){
      return this.$getWebURL() + '/api/v1/attachment/' + image_path
    }
  },
  data () {
    return {
      search_string:'',
      loading: false,
      form: {
        username: '',
        password: ''
      },
      error: null,
      smallpatent_datas:[],
      popupzone_datas:[],
      popupzone_index:-1,
      popupzone_image:'',
      dialog:{
        show:false
      },
      options:['유형A','유형B','유형C'],
    }
  }
}
</script>
<style lang="scss" scoped>
.login-main {
  background-image: url('~@/assets/bg/searchmain_back.png');
  background-size: cover;
  position: absolute;
  width: 1920px;
  height: 700px;
  left: 0px;
  top: 0px;
}
.bg-log{
  background-image: url('~@/assets/bg/kitech-logo-wh 1.png');
  background-size: cover;
  position: absolute;
  width: 200.05px;
  height: 60px;
  left: 52px;
  top: 24px;
  //border: 1px solid white;
}
.bg-title-1{
  position: absolute;
  width: 306px;
  height: 32px;
  left: 807px;
  top: 208px;

  font-family: Elice DigitalBaeum;
  font-style: normal;
  font-weight: normal;
  font-size: 26px;
  line-height: 26px;
  /* identical to box height, or 100% */

  text-align: center;

  color: #FFFFFF;
}
.bg-title-2{
  position: absolute;
  width: 700px;
  height: 56px;
  left: 637px;
  top: 248px;

  font-family: Elice DigitalBaeum;
  font-style: normal;
  font-weight: bold;
  font-size: 46px;
  line-height: 46px;
  /* identical to box height, or 100% */

  text-align: center;
  letter-spacing: -0.04em;

  color: #FFFFFF;
}
.search-bar{
  position: absolute;
  width: 560px;
  height: 56px;
  left: 530px;
  top: 352px;
  padding-bottom: 0px;
  padding-left: 20px;
  padding-right: 20px;
  background: #FFFFFF;
  border-radius: 16px;

}
.search-input{
  font-family: Noto Sans KR;
  font-style: normal;
  font-weight: 500;
  font-size: 16px;
  line-height: 23px;
  color: #808080;
}
.search-btn{
  background-image: url('~@/assets/bg/btn-search.png');
  position: absolute;
  width: 120px;
  height: 56px;
  left: 1106px;
  top: 355px;
  border-radius: 16px;
  cursor: pointer;
}
.techtrans-btn{
  background-image: url('~@/assets/bg/btn-add.png');
  position: absolute;
  width: 201px;
  height: 56px;
  left: 1234px;
  top: 356px;
  cursor: pointer;
}
.notice-area{
  position: absolute;
  width: 752px;
  height: 348px;
  left: 360px;
  top: 732px;
  background-color: #00ffe8;
}
.login-btn{
  position: absolute;
  width: 120px;
  height: 32px;
  left: 1696px;
  top: 24px;
  background: #3E1F99;
  border-radius: 6px;
  color :white;
}
.back_height{
  height: 1280px;
  background-color: white;
}
.notice-wrap {
  position: absolute;
  width: 752px;
  height: 348px;
  left: 360px;
  top: 732px;
  background: #FFFFFF;
}
.notice-header {
  font-family: 'Noto Sans KR';
  font-style: normal;
  font-size: 16px;
  line-height: 23px;
  letter-spacing: -0.04em;

  border-bottom: 1px solid white;
  margin-bottom: 10px;
  font-weight: bold;
  text-align: left;
  color: #000000;

}
.notice-list-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin: 4px 0;
  padding-left: 12px;

  font-size: 12px;
  color: #404040;

  //cursor: pointer;
  position: relative;
}
.notice-list-item-title {
  &:before {
    position: absolute;
    content: "•";
    font-size: 18px;
    top: 9px; left: 0px;
    line-height: 0;
  }
  width: 100%;
  height: 40px;
  font-family: Noto Sans KR;
  font-weight: bold;
  font-size: 14px;
  line-height: 20px;
  color: #333333;
}
.notice-list-item-date {
  font-size: 11px;
}
.header-line{
  position: absolute;
  width: 752px;
  height: 1px;
  background: #0055BB;
}
.item-line{
  position: absolute;
  width: 752px;
  height: 1px;
  background: #CCCCCC;
}
.t-right{
  text-align: right;
}
.smallpatent_plus{
  background-image: url('~@/assets/bg/smallpatent_plus.png');
  position: absolute;
  width: 43px;
  height: 17px;
  left: 1061px;
  top: 748px;

  font-family: Noto Sans KR;
  font-style: normal;
  font-weight: 300;
  font-size: 12px;
  line-height: 17px;
  text-align: right;

  color: #000000;
  cursor: pointer;
}
.popup-zone-area{
  position: absolute;
  width: 400px;
  height: 348px;
  left: 1160px;
  top: 742px;
  font-weight: bold;
  font-size: 16px;
  line-height: 20px;
  color: #333333;
}
.popup-body{
  position: absolute;
  width: 400px;
  height: 300px;
  left: 1160px;
  top: 780px;
  cursor: pointer;
}
.popup-count{
  position: absolute;
  width: 26px;
  height: 19px;
  left: 1452px;
  top: 747px;

  font-family: Noto Sans KR;
  font-style: normal;
  font-weight: 500;
  font-size: 13px;
  line-height: 19px;
  /* identical to box height */

  text-align: right;

  color: #000000;
}
.popup-left{
  background-image: url('~@/assets/bg/btn-prev.png');
  position: absolute;
  width: 18px;
  height: 18px;
  left: 1490px;
  top: 747px;
  cursor: pointer;
}
.popup-right{
  background-image: url('~@/assets/bg/btn-next.png');
  position: absolute;
  width: 18px;
  height: 18px;
  left: 1512px;
  top: 747px;
  cursor: pointer;
}
.pos-center{
  text-align: center;
}
.left-m{
  margin-left: 10px;
}
</style>
