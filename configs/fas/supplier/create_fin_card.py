from lib.send_mes import send_mes

async def create_fin_card(form):
        db=form.db ; ov=form.ov
        city_id=0
        data={
          'user_id':form.id,
          #'underwriter':8311, # Деженков
          'manager_id':form.manager['id'],
          'group_id':443,
          'manager_fin':12057 
        }

        #if ov['city']:
        #  city_id = await db.query(
        #    query='select city_id from city where name=%s',
        #    values=[ov['city']],
        #    onevalue=1
        #  )
        #  if city_id: data['city_id']=city_id

        fin_card_id = await db.save(
          table='user_fin',
          data=data
        )
        send_mes(
          from_addr='info@fascrm.ru',
          to='svs@reg-rf.pro',
          subject="Создана новая карта фин. услуг",
          message=f"<p>Только что {form.manager['name']} создал(а) карту Фин. услуг для компании: <b>{ov['firm']}</b>( ИНН: {ov['inn']})</p>"+\
                  f"<p><a href='{form.s.config['system_url']}edit_form/user_fin/{fin_card_id}'>Перейти в карту</a></p>"
        )
        #message=f"<p>Только что {form.manager['name']} создал(а) карту Фин. услуг для компании {ov['firm']}( ИНН: {ov['inn']})</p>"+\
        #  f"<p><a href='{form.s.config['system_url']}edit_form/teamwork_ofp/{fin_card_id}'>Перейти в карту</a></p>"

        redirect_link=f"/edit_form/user_fin/{fin_card_id}"
        #form.pre(f"<a href='{redirect_link}'>{redirect_link}</a>")
        form.redirect=redirect_link