def accepted_before_code(form,field):
  #form.pre(form.s.shop)
  shop=form.s.shop
  #if form.id field['value']=='0':
  bot_link=f'https://t.me/{shop["botname"].replace("@","")}?accept-admin-telegram'
  field['after_html']=f'''
    Для подтверждения данного Telegram-логина, пожалуйста отправьте команду:<br>
    <a href="{bot_link}" target="_blank">/accept-admin-telegram</a><br>
    боту {shop["botname"]}
  '''
events={
  'accepted':{
    'before_code':accepted_before_code
  }
}