from lib.send_mes import send_mes

def create_ofp_card(form):
        db=form.db
        ov=form.ov
    # Пример ссылки на создание: /edit_form/user/106998?action=create_ofp_card
        #action=R['cgi_params']['action']

        #form.pre(ov)
        city_id=0
        data={
            #'firm':ov['firm'],
            'city':ov['city'],
            #'inn':ov['inn'],
            'user_id':form.id,
            # По умолчанию проставлялся Бородин, но решили проставлять того, кто создал
            'manager_from':form.manager['id'], 
        }

        if ov['city']:
          city_id=db.query(
            query='select city_id from city where name=%s',
            values=[ov['city']],
            onevalue=1
          )
          if city_id: data['city_id']=city_id

        ofp_card_id=db.save(
          table='teamwork_ofp',
          data=data
        )



        message=f"<p>Только что {form.manager['name']} создал(а) карту ОФП для компании {ov['firm']}( ИНН: {ov['inn']})</p>"+\
          f"<p><a href='{form.s.config['system_url']}edit_form/teamwork_ofp/{ofp_card_id}'>Перейти в карту</a></p>"

        # send_mes(
        #   from_addr='info@fascrm.ru',
        #   to='pzm@a-u-z.pro',
        #   subject=f"Создана новая карта ОФП: {ov['firm']}, ИНН: {ov['inn']}",
        #   message=message
        # )

        # Убрал копирование контактов, попросили сделать сквозными
        # contact_list=db.query(
        #   query=f'select * from user_contact where user_id={form.id}'
        # )
        # for contact in contact_list:
        #   db.save(
        #     table='teamwork_ofp_contact',
        #     data={
        #       'teamwork_ofp_id':ofp_card_id,
        #       'fio':contact['fio'],
        #       'email':contact['email'],
        #       'phone':contact['phone'],
        #       'position':contact['position'],
        #       'otv':contact['otv'],
        #       'comment':contact['comment']
        #     }
        #   )
        redirect_link=f"/edit_form/teamwork_ofp/{ofp_card_id}"
        #form.pre(f"<a href='{redirect_link}'>{redirect_link}</a>")
        form.redirect=redirect_link