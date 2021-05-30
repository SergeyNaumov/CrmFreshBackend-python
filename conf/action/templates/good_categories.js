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


function load_categories(){
  setTimeout(
    ()=>{
      
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
