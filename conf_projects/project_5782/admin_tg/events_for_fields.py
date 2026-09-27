async def accepted_before_code(form,field):
  if form.id:
    bot=form.bot
    #if form.id field['value']=='0':
    botname=bot.get('header')
    #form.pre(form.ov)
    bot_link=f'https://t.me/{botname.replace("@","")}?start=accept-admin{form.ov["access_key"]}'
    field['after_html']=f'''
      Для подтверждения данного Telegram-логина, пожалуйста отправьте команду:<br>
      <a href="{bot_link}" target="_blank">/start accept-admin{form.ov["access_key"]}</a><br>
      боту {botname}
    '''
events={
  'accepted':{
    'before_code':accepted_before_code
  }
}