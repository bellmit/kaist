import _ from 'lodash'
// import numeral from 'numeral'

const regx_end_session = /^Ended\sdesktop\ssession\s"(.*)"\sfrom\s(.*)\sto\s(.*),\s(\d+)\s(.*)$/
const regx_start_remote = /^Started\sremote\sdesktop\swithout\snotification\s\((.*)\)$/
const regx_start_session = /^Started\sdesktop\ssession\s"(.*)"\sfrom\s(.*)\sto\s(.*)$/

export default {
  install(Vue) {
    // Vue.filter('format', (value, option) => {
    //   if (!option) option = '0,0'
    //   return numeral(value).format(option)
    // })
    // Vue.prototype.$numeral = numeral

    Vue.prototype.$getPatentNum = (description) => {
      return description.split('","')[0].replace('"','')
    }

    Vue.prototype.$getPatentTitle= (description,limit=null) => {
      if(limit != null && description.split('","')[1].length > limit-3)
        return description.split('","')[1].split('(')[0].substring(0,limit) + "..."
      return description.split('","')[1].split('(')[0]
    }

    Vue.prototype.$getPatentSummary= (description,limit=null) => {
      if(limit != null)
        return description.split('","')[2].substring(0,limit) + "..."
      return description.split('","')[2]
    }
    Vue.prototype.$makePatentCode= (obj) => {
      var data1 = obj.substr(0,2)
      var data2 = ''
      if(data1 == "10")
        data2 = "KR" + obj.substr(2,obj.length-2) + "A"
      else if(data1 == "20")
        data2 = "KR" + obj.substr(2,obj.length-2) + "U"
      return data2
    }

    Vue.prototype.$getLevel = (cost) => {
      var cost_array = [10000000,20000000,50000000,100000000]
      if(cost < cost_array[0])
        return 1
      else if (cost >= cost_array[0] && cost <= cost_array[1])
        return 2
      else if (cost >= cost_array[1] && cost <= cost_array[2])
        return 3
      else if (cost >= cost_array[2] && cost < cost_array[3])
        return 4
      else
       return 5
    }
    Vue.prototype.$getCostColor = (cost) => {
      var cost_array = [10000000,20000000,50000000,100000000]
      if(cost < cost_array[0])
        return 'cost_color_1'
      else if (cost >= cost_array[0] && cost <= cost_array[1])
        return 'cost_color_2'
      else if (cost >= cost_array[1] && cost <= cost_array[2])
        return 'cost_color_3'
      else if (cost >= cost_array[2] && cost < cost_array[3])
        return 'cost_color_4'
      else
        return 'cost_color_5'
    }

    Vue.prototype.$getCostRange = (cost) => {
      var cost_array = [10000000,20000000,50000000,100000000]
      if(cost < cost_array[0])
        return '1천만원 미만'
      else if (cost >= cost_array[0] && cost <= cost_array[1])
        return '1천만원 ~ 2천만원'
      else if (cost >= cost_array[1] && cost <= cost_array[2])
        return '3천만원 ~ 5천만원'
      else if (cost >= cost_array[2] && cost < cost_array[3])
        return '5천만원 ~ 1억원'
      else
        return '1억원이상'
    }

    Vue.prototype.$getTextColor = (cost) => {
      var cost_array = [10000000,20000000,50000000,100000000]
      if(cost < cost_array[0])
        return 'blue--text'
      else if (cost >= cost_array[0] && cost <= cost_array[1])
        return 'amber--text'
      else if (cost >= cost_array[1] && cost <= cost_array[2])
        return 'yellow--text'
      else if (cost >= cost_array[2] && cost < cost_array[3])
        return 'deep-orange--text'
      else
        return 'red--text'
    }
    Vue.prototype.$getWebURL = () => {
      //return 'http://localhost:8080'
      return 'http://101.101.215.87:443'
    }
    Vue.prototype.$pdfDownload = (patent_code) => {
      var df_url = Vue.prototype.$getWebURL() + '/api/v1/pdf/' + patent_code + '.pdf'
      window.open(df_url, "_blank", "toolbar=yes,scrollbars=yes,resizable=yes,top=200,left=200,width=1200,height=800")

    }
    Vue.prototype.$convertPatentToRaw= (kr_patent_code) => {
      var patent_code = ''
      var last_idx = kr_patent_code.length-1
      if(kr_patent_code.substring(last_idx,kr_patent_code.length) == "U")
        patent_code = '20' + kr_patent_code.substring(2,kr_patent_code.length-1)
      else
        patent_code = '10' + kr_patent_code.substring(2,kr_patent_code.length-1)
      return patent_code
    }
    Vue.filter('transit', (value) => {
      let matched = regx_end_session.exec(value)
      if (matched) {
        let unit = ''
        if (_.startsWith(matched[5], 'sec')) unit = '초'
        else if (_.startsWith(matched[5], 'min')) unit = '분'
        else if (_.startsWith(matched[5], 'hour')) unit = '시간'
        return `"${matched[1]}" 세션이 종료되었습니다(${matched[2]} > ${matched[3]}, ${matched[4]} ${unit})`
      }

      matched = regx_start_remote.exec(value)
      if (matched) {
        return `원격제어를 시작합니다(${matched[1]})`
      }

      matched = regx_start_session.exec(value)
      if (matched) {
        return `원격 세션이 연결되었습니다(${matched[1]} > ${matched[2]})`
      }

      return value
    })
  }
}
