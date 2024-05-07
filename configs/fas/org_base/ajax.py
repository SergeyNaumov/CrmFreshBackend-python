async def brand_id(form,v):
  brand_id=v['brand_id']
  after_html=''
  if brand_id:
    brand=await form.db.query(
      query='SELECT * from brand where id=%s',
      values=[brand_id],
      onerow=1,
    )
    if brand:
      after_html=f"<img src='/files/logo/{brand['logo']}'>"
    

  
  return ['brand_id',{'after_html':after_html}]

ajax={
  'brand_id':brand_id,
  
}
