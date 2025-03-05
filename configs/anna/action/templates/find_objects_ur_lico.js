
if( 1 || !('bind_subscribe_buttons'  in window) ){

  window.bind_subscribe_buttons={
    // click_ul_subscribe:function(btn){ // Нажатие на кнопку "подписаться / отписаться" для юрлица
    //     console.log(btn)
    //     return false
    // },

    run: ()=>{
      function ce(o){ // simple create element
        if('t' in o)
          o.tag=o.t

        if(o.tag){
          let element=document.createElement(o.tag)
          if(o.html)
            element.innerHTML=o.html

          if(o.text)
            element.innerText=o.text
          if(o.attr_list){
            for(let a of o.attr_list){
              element.setAttribute(a[0],a[1])
            }
          }
          //console.log(element)
          return element
        }
        return false
      }

      function create_button(u,type){ // кнопка "подписаться / отписаться" для юридического лица
        // type==1 -- юрлицо
        // type=2 -- аптека

          let btn
          let v=parseInt(u.v)

          if(v==0){ // если не подписан -- создаём кнопку
            btn=ce({t:'a'})
            btn.innerHTML='<span style="color: red;">подписаться</span>'
            btn.setAttribute("href",'#')
            btn.setAttribute("data-action_id",u.action_id)
            btn.setAttribute("data-id",u.id)
            btn.setAttribute("data-type",u.id)
            btn.setAttribute("data-subscribed",u.v)
            // Нажатие на кнопку "подписаться / отписаться" для юрлица
            btn.onclick=function(){
              
              url=(type==1)?'/anna/subscribe-action/'+u.action_id+'/ur_lico/'+u.id:'/anna/subscribe-action/'+u.action_id+'/ur_lico/'+u.id

              window.app.$http.get(
                window.BackendBase+url
              ).then(
                r=>{
                  let d=r.data
                  if(d.success){
                    btn.parentNode.insertBefore(
                      ce({t:'span',html:'<span style="color: blue;">запрос отправлен</b></span>'}),
                      btn.nextSibling
                    )
                    btn.innerHTML=''
                  }
                  else if(d.errors.length){
                    //alert(d.errors[0])

                    let error_div=ce({t:'div',html:'<span style="color: red;">'+d.errors[0]+'</b></span>'})
                    error_div.setAttribute("id",'error-'+u.id)

                    btn.parentNode.insertBefore(
                      error_div,
                      btn.nextSibling
                    )
                    setTimeout(
                      ()=>{
                        error_div.parentElement.removeChild(error_div)
                      },
                      500
                    )
                    
                  }
                }
              ).catch(
                ()=>{}
              )
              
              



              return false
            }
          }
          else if(v==1){ // надпись "запрос на подписку"
            btn=ce({t:'span',html:'<span style="color: blue;">запрос отправлен</b></span>'})
          }
          else if(v==2){
            btn=ce({t:'span',html:'<span style="color: green;"><b>подписка оформлена</b></span>'})
          }
          







          return btn
      }

      function button_processing(b){
        let action_id=b.getAttribute('id').replace(/^[^0-9]+/,'')
        
        button_processing
        let [ur_lico_subscribe, apteka_subscribe]=b.innerText.split('|')
        ur_lico_subscribe=ur_lico_subscribe?JSON.parse(ur_lico_subscribe):[]
        //console.log('ur_lico_subscribe:',ur_lico_subscribe)
        apteka_subscribe=apteka_subscribe?apteka_subscribe:'0' // кол-во подписанных аптек



        //console.log([ur_lico_subscribe, apteka_subscribe])
        // получаем id для акции

        /*
        b.innerText=`
          <button data-ul-id="" onclick="return click_ul_subscribe(this)"></button> <hr/>
        `*/

        let buttons_ul=[], buttons_apteka=[]
        // Рендер кнопок для юрлица
        b.innerHTML=''

        // Если есть юрлица
        if(ur_lico_subscribe.length){
          for(let u of ur_lico_subscribe){
            u.action_id=action_id
            b.appendChild(ce({t:'span',html:`${u.name}<small>(${u.apt_cnt})</small>: `}))

            let btn=create_button(u,1)
            //let label=document.createElement(`span`)
            //b.innerHTML+=`${u.name}:&nbsp;`
            //b.appendChild(label)
            
            b.appendChild(btn)
            //console.log('u:',u)
            //b.appendChild(ce({t:'small',html:``}))
            if(ur_lico_subscribe.length){ // разделение между юрлицами (если их несколько)
              b.appendChild(ce({t:'br'}))
            }
            

            //b.appendChild(document.createElement('br'))

          }
        }
        /* "пожписано аптек" убираем (вместо этого сделали подписи для каждого юрлица)
        b.appendChild( ce({t:'div',html:`<hr><b>Подписано аптек: </b> ${apteka_subscribe}<br>`}) )
        */

        
        
        
      }


      let buttons_data=document.querySelectorAll('.subscibe_buttons')
      for(let b of buttons_data){ // цикл по данным для кнопок
        button_processing(b) // рисуем кнопки для акции
      }




    },

    // button_processing -- отрисовывает кнопки



  }


}
else{
  console.log('больше не объявляем')
}




window.bind_subscribe_buttons.run()