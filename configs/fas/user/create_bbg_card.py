from lib.send_mes import send_mes

async def create_bbg_card(form):
        db=form.db
        ov=form.ov
    # Пример ссылки на создание: /edit_form/user/106998?action=create_ofp_card
        #action=R['cgi_params']['action']

        #form.pre(ov)
        city_id=0
        data={
            'manager_id':form.manager['id'],
            'user_id':form.id,
        }


        bbg_card_id = await db.save(
          table='user_bbg',
          data=data
        )

        message=f"<p>Только что {form.manager['name']} создал(а) карту ББГ для компании {ov['firm']}( ИНН: {ov['inn']})</p>"+\
          f"<p><a href='{form.s.config['system_url']}edit_form/user_bbg/{bbg_card_id}'>Перейти в карту</a></p>"

        #print('message:',message)

        send_mes(
          from_addr='info@fascrm.ru',
          to='dmn@reg-rf.pro, zer@reg-rf.pro',
          subject=f"Создана новая карта ББГ: {ov['firm']}, ИНН: {ov['inn']}",
          message=message
        )
        redirect_link=f"/edit_form/user_bbg/{bbg_card_id}"
        form.redirect=redirect_link