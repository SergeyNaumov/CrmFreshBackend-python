async def regnumber(form,v):
  v['regnumber']
  return_hash={}

  if ('regnumber' in v):
    regnumber=v['regnumber']
    after_html=''
    
    if regnumber.isnumeric():
      if len(regnumber)>12:
        link=f'https://zakupki.gov.ru/epz/order/notice/zk44/view/common-info.html?regNumber={regnumber}'
        
        
        
      else:
        link=f'https://zakupki.gov.ru/223/purchase/public/purchase/info/common-info.html?regNumber={regnumber}'
      
      after_html=f'<a href="{link}" target="_blank">{link}</a>'
      return_hash={'after_html':after_html}
        
  return ['regnumber',return_hash]
      

  #print('ajax regnumber:',v)

async def product(form,v):
  firm=v['firm']
  product=v['product']
  bgcolor=''
  
  jscode=''
  if product in ('9','14','15'):
    bgcolor='#fdffc4'
    
  
  if product=='8':
    bgcolor='#ddffc4'
  
  if product=='11':
    bgcolor='#c3c6ff'

  if bgcolor:
    #jscode=f"document.querySelector('form .v-card').style['background-color']='{bgcolor}'"
    
    # подменяем заголовок
    #jscode=f"""document.querySelector('h1').innerHTML=`
    #    <div style="display: inline-block; width: 50px; height: 50px; background-color: {bgcolor}; border: 1px solid gray;"></div>
    #    <div style="display: inline-block; vertical-align: top;">{firm}</div>`"""

    
    #jscode=f"document.querySelector('form .layout .v-card').style.background='{bgcolor}'"
    jscode=f"document.querySelector('#EditForm').style.background='{bgcolor}'"
    

  
  return ['product',{'jscode':jscode}]

ajax={
  'regnumber':regnumber,
  'product':product
}