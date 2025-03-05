
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
          console.log(element)
          return element
        }
        return false
      }
      function get_subscribe_label(v){
        return parseInt(v)?'<span style="color: red;">отписаться</span>':'<span style="color: green;">подписаться</span>'
      }
      function create_button(u,type){ // кнопка "подписаться / отписаться" для юридического лица
        // type==1 -- юрлицо
        // type=2 -- аптека

          let btn
          let v=parseInt(u.v)

          if(v==0){ // если не подписан -- создаём кнопку
            btn=ce({t:'a'})
            btn.innerHTML=get_subscribe_label(u.v)
            btn.setAttribute("href",'#')
            btn.setAttribute("data-id",u.id)
            btn.setAttribute("data-type",u.id)
            btn.setAttribute("data-subscribed",u.v)
            // Нажатие на кнопку "подписаться / отписаться" для юрлица
            btn.onclick=function(){
              console.log('btn:',btn)
              
              let id=element.getAttribute('data-id')
              let subscribed=element.getAttribute('data-subscribed')
              let type=element.getAttribute('data-type')
              subscribed=parseInt(subscribed)?0:1
              if(parseInt(subscribed)){
                subscribed=0
                btn.innerText='подписаться'
              }
              else{
                subscribed=1
                btn.innerText='отписаться'
              }



              return false
            }
          }
          else if(v==1){ // надпись "запрос на подписку"
            btn=ce({t:'div',html:'<span style="color: blue;"><b>запрос на подписку отправлен</b></span>'})
          }
          else if(v==2){
            btn=ce({t:'div',html:'<span style="color: green;">подписка оформлена</span>'})
          }
          






          return btn
      }

      function button_processing(b){
        //console.log('b:',b)
        let [ur_lico_subscribe, apteka_subscribe]=b.innerText.split('|')
        ur_lico_subscribe=ur_lico_subscribe?JSON.parse(ur_lico_subscribe):[]
        apteka_subscribe=apteka_subscribe?JSON.parse(apteka_subscribe):[]



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
            b.appendChild(ce({t:'span',html:`${u.name}: `}))

            let btn=create_button(u,1)
            //let label=document.createElement(`span`)
            //b.innerHTML+=`${u.name}:&nbsp;`
            //b.appendChild(label)
            
            b.appendChild(btn)
            
            if(ur_lico_subscribe.length){ // разделение между юрлицами (если их несколько)
              b.appendChild(ce({t:'br'}))
            }
            

            //b.appendChild(document.createElement('br'))

          }
        }

        
        if(apteka_subscribe.length){
          b.appendChild(ce({t:'hr'}))
          b.appendChild(ce({t:'span',html:'<br><b>Аптеки:</b>'}))
          for(let a of apteka_subscribe){
            b.appendChild(ce({t:'span',html:`<br>${a.name}: `}))
            // кнопка
            b.appendChild(create_button(a,2))
          }

        }
        
        
        
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