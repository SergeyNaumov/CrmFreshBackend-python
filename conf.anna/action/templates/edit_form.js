
// Таб с прогнозными бонусами
window.select_bonus_ur_lico=function(ur_lico_id){
    let items=document.querySelectorAll('.prognoz_bonus_item')
    for(let i of items){
        console.log(i.getAttribute('id'),'select_bonus_ur_lico'+ur_lico_id, (i.getAttribute('id')=='select_bonus_ur_lico'+ur_lico_id) )
        if(i.getAttribute('id')=='bonus_ur_lico'+ur_lico_id){
            i.style.display=''
        }
        else{
            i.style.display='none'
        }
        
        
    }
    return false
}
function draw_diagramm(canvas_el){

    //let ctx = document.getElementById('myChart').getContext('2d');
    let ctx = canvas_el.getContext('2d');
    let data=canvas_el.getAttribute('data-values').split(',')
    let labels=canvas_el.getAttribute('data-labels').split('|')
    let description=canvas_el.getAttribute('data-description')
    for(let i in data){
        data[i]=parseInt(data[i])
    }
    console.log(data)
    //let d2=i.querySelector('.diagramm2').innerText
    console.log(labels)
    let myChart = new Chart(ctx, {
    type: 'doughnut',
    data: {
        labels: labels,
        datasets: [{
            data: data,
            backgroundColor: [ '#00e676','#e91e63',],
            borderWidth: 0.5 ,
            borderColor: '#ddd'
        }]
    },
    options: {
        responsive: false,
        title: {
            display: true,
            text: description,
            position: 'top',
            fontSize: 16,
            fontColor: '#111',
            padding: 20
        },
        legend: {
            display: true,
            position: 'bottom',
            labels: {
                boxWidth: 20,
                fontColor: '#111',
                padding: 15
            }
        },
        tooltips: {
            enabled: false
        },
        plugins: {
            datalabels: {
                color: '#111',
                textAlign: 'center',
                font: {
                    lineHeight: 1
                },
                formatter: function(value, ctx) {
                    return ctx.chart.data.labels[ctx.dataIndex] + '\n' + value + '%';
                }
            }
        }
    }
});

}
function draw_all_diagrams(){
  setTimeout(
    ()=>{
      let items=document.querySelectorAll('.prognoz_bonus_item')
      if(items.length){
        console.log('рисуем')
        for(let i of items){
            let canvas_el=i.querySelectorAll('.diagramm')
            for(let c of canvas_el){
                draw_diagramm(c)
            }


        }
      }
      else{
        console.log('пробуем ещё')
        draw_all_diagrams()
      }
    },500)
}


draw_all_diagrams()

// for good categories
function show_plan(plan_id,el){
  
  let e=document.getElementById('plan'+plan_id)
  let d=e.style.display
  let lnk=document.querySelectorAll('.catheader a#toggle'+plan_id)
  
  if(d=='none'){
    e.style.display=''
    //el.innerText('скрыть')
  }
  else{
    e.style.display='none'
    //el.innerText('подробности')
  }
  
  
  return false
}

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
function init_subscribe_links(){

  // инициализация ссылок "подписаться" для юрлица
  for(let a of document.querySelectorAll('a.ur_lico_subscribe_link')){
    a.onclick=()=>{
      let action_id=a.getAttribute('data-action_id')
      let ur_lico_id=a.getAttribute('data-id')


      let url='/anna/subscribe-action/'+action_id+'/ur_lico/'+ur_lico_id
      window.app.$http.get(
          window.BackendBase+url
      ).then(
          r=>{
            let d=r.data
            if(d.success){
                    a.parentNode.insertBefore(
                      ce({t:'span',html:'<span style="color: blue;">запрос отправлен</b></span>'}),
                      a.nextSibling
                    )
                    a.innerHTML=''
                  }
                  else if(d.errors.length){
                    //alert(d.errors[0])

                    let error_div=ce({t:'div',html:'<span style="color: red;">'+d.errors[0]+'</b></span>'})
                    error_div.setAttribute("id",'error-'+u.id)

                    a.parentNode.insertBefore(
                      error_div,
                      a.nextSibling
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
    }
  }

}

function load_categories(){
  setTimeout(
    ()=>{
      
      init_subscribe_links()

      for(let a of document.querySelectorAll('a.popup_vitrina')){
        a.onclick=()=>{
          window.EditForm.popup={
              show:true,
              header:'Витрина',
              body: 'По условиям контракта, товар должен быть выложен на полке'
          }
          return false
        }
      }

      for(let a of document.querySelectorAll('a.popup_bonus')){
        a.onclick=()=>{
          window.EditForm.popup={
              show:true,
              header:'Бонус',
              body: '% бонуса зависит от закупленного товара. Каждый товар имеет свой % бонуса'
          }
          return false
        }
      }

      let catheaders_list=document.querySelectorAll('.catheader a')
      for(let a of catheaders_list){
        
        a.onclick=function(){
          let cat_id=a.getAttribute('data-id')
          show_plan(cat_id,this)
          return false
        }
      }
    },
    300
  )
}
load_categories()



