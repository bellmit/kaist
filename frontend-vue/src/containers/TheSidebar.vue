<template>
  <CSidebar
    fixed
    :minimize="minimize"
    :show="show"
    @update:show="(value) => $store.commit('set', ['sidebarShow', value])"
    class="sidebar-bg"
    width="304"
  >
    <CSidebarBrand class="d-md-down-none" @click="move_first()">
       <div class="kitech-log"> </div>
<!--      <span class="cb-log">-->
<!--        인공지능 특허검색-->
<!--      </span>-->
<!--      <CIcon-->
<!--        class="c-sidebar-brand-full"-->
<!--        name="logo"-->
<!--        size="custom-size"-->
<!--        :height="35"-->
<!--        viewBox="0 0 556 134"-->
<!--      />-->
<!--      <CIcon-->
<!--        class="c-sidebar-brand-minimized"-->
<!--        name="logo"-->
<!--        size="custom-size"-->
<!--        :height="35"-->
<!--        viewBox="0 0 110 134"-->
<!--      />-->
    </CSidebarBrand>
    <CRenderFunction v-if="$session.authorized" flat :content-to-render="$options.nav"/>
    <CRenderFunction v-else flat :content-to-render="$options.nav_anyone"/>
<!--    <CSidebarMinimizer-->
<!--      class="d-md-down-none"-->
<!--      @click.native="$store.commit('set', ['sidebarMinimize', !minimize])"-->
<!--    />-->
  </CSidebar>
</template>

<script>
import nav from './_nav'
import nav_anyone from './_nav_anyone'
import { brandSet as brands } from '@coreui/icons'
export default {
  name: 'TheSidebar',
  nav,
  nav_anyone,
  brands,
  computed: {
    show () {
      return this.$store.state.sidebarShow 
    },
    minimize () {
      return this.$store.state.sidebarMinimize 
    }
  },
  methods:{
    move_first() {
      if(this.$session.check_permission()){
        this.$session.logout()
        this.$router.push('/searchmain').catch(()=>{});
      }else{
        this.$router.push('/searchmain').catch(()=>{});
        location.reload(true)
      }

    }

  }

}
</script>
<style scoped lang="scss">
.cb-log{
  font-size: 20px;
  font-weight: bold;
  margin-left: 10px;
}
.sidebar-bg{
  background-image: url('~@/assets/bg/left-bg.png');
}
.kitech-log{
  background-image: url('~@/assets/bg/kitech-logo.png');
  background-size: 130px;
  position: absolute;
  left: 0.36%;
  right: 0.36%;
  top: 1.27%;
  bottom: 1.26%;
}
</style>
