<template>
  <div class="c-app flex-row align-items-center login-main">
    <CContainer>
      <CRow class="justify-content-center">
        <CCol md="8">
          <CCardGroup>
            <CCard class="p-4">
              <CCardBody>
                <CForm>
                  <h1>한국 생산기술 연구원 <br>인공지능 특허검색</h1>
                  <p class="text-muted"></p>
                  <CInput
                    placeholder="사용자 아이디"
                    autocomplete="username email"
                    v-model="form.username"
                  >
                    <template #prepend-content><CIcon name="cil-user"/></template>
                  </CInput>
                  <CInput
                    placeholder="패스워드"
                    type="password"
                    autocomplete="curent-password"
                    v-model="form.password"
                    @keypress.enter="requestGetToken"
                  >
                    <template #prepend-content><CIcon name="cil-lock-locked"/></template>
                  </CInput>
                  <CRow>
                    <CCol col="6" class="text-left">
                      <CButton color="secondary" class="px-4" @click="requestGetToken" >로그인</CButton>
                    </CCol>
<!--                    <CCol col="6" class="text-right">-->
<!--                      <CButton color="link" class="px-0">패스워드 분실</CButton>-->
<!--                      <CButton color="link" class="d-lg-none">회원가입</CButton>-->
<!--                    </CCol>-->
                  </CRow>
                </CForm>
              </CCardBody>
            </CCard>
            <CCard
              color="primary"
              text-color="white"
              class="text-center py-5 d-md-down-none"
              body-wrapper
            >
              <CCardBody>
                <h2>공지사항</h2>
<!--                <p>10월은 보안 점검 기간입니다. 개인 보안에 각별히 주의해 주세요!!</p>-->
              </CCardBody>
            </CCard>
          </CCardGroup>
        </CCol>
      </CRow>
    </CContainer>
  </div>
</template>

<script>
export default {
  name: 'Login',
  methods: {
    async requestGetToken () {
      this.error = null
      if (!this.form.username || !this.form.password)
        return (this.error = '아이디와 패스워드를 입력해 주세요.')

      this.loading = true
      try {
        let {data} = await this.$http.post('login', this.form)
        // alert(JSON.stringify(data))
        // if(this.form.password != 'kitech!@'){
        //   alert("패스워드 오류!!")
        //   location.reload(true)
        //   return data
        // }
        if (data.status) this.$session.setToken(data.user)
        else this.error = this.CONSTANT.LOGIN_ERR[data.reason] || `로그인 실패 [${data.reason}]`
        this.$session.authorized = true
        this.$router.push('/search')
        return data
      }
      catch (err) {
        this.error = err.message
      }
      finally {
        this.loading = false
      }

    },
    move_first(){
      location.reload(true)
    },
    // signUpDialogShow () {
    //   this.signup.show = true
    // },
    // signUpSubmit () {
    //   let msg = []
    //   if (!this.signup.form.userid) msg.push('아이디를 입력해 주세요.')
    //   else if (!/^[a-zA-Z0-9]+$/.test(this.signup.form.userid)) msg.push('아이디는 영문, 숫자만 사용 가능합니다.')
    //
    //   if (!this.signup.form.userpw) msg.push('비밀번호를 입력해 주세요.')
    //   else {
    //     if (this.signup.form.userpw.length < 8 || this.signup.form.userpw.length > 15) msg.push('비밀번호는 8-15자 길이여야 합니다.')
    //     if (!/^[a-zA-Z0-9]+$/.test(this.signup.form.userpw)) msg.push('비밀번호는 영문, 숫자를 포함해야 합니다.')
    //     if (this.signup.form.userpw !== this.signup.form.userpwc) msg.push('비밀번호 확인과 일치하지 않습니다.')
    //   }
    //
    //   // validation 추가
    //
    //   if (msg.length) {
    //     this.signup.errors = msg
    //     return;
    //   }
    //   else this.signUpDialogClose()
    // },
    // signUpDialogClose () {
    //   this.signup.show = false
    //   this.signup.errors = []
    //   this.signup.form = {
    //     userid: '',
    //     userpw: '',
    //     userpwc: '',
    //     company: '',
    //     username: '',
    //     email: '',
    //     phone: ''
    //   }
    // }
    beforeDestroy () {
      // document.removeEventListener("backbutton", this.move_first());
    }
  },
  mounted() {
    window.onpopstate = function() {
      location.reload(true)
    };
  },
  data () {
    return {
      loading: false,
      form: {
        username: '',
        password: ''
      },
      error: null,
    }
  }
}
</script>
<style lang="scss" scoped>
.login-main {
  background-color: #E6EEFF !important;
  background-image: url('~@/assets/bg/bg-2.jpg');
  background-size: cover;
  background-position: center center;
}
</style>
