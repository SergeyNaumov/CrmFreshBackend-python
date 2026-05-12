from lib.fas.create_fin_card import create_fin_card
from lib.fas.create_ofp_card import create_ofp_card

async def action_create_sr(form,field,R):
	db=form.db
	app_id=R.get('app_id',None)
	#print('app_id:',app_id)
	if not(form.id):
		form.errors.append('не указан id карты')
	if not(app_id) or not(type(app_id) is int):
		form.errors.append('app_id не указан или указан не корректно')
	item={}

	if form.success():
		app=await db.query(
			query="""
				select
					a.*,
					s.type,
					u.id user_id, u.firm
				from
					dogovor_app a
					join docpack dp ON dp.id=a.dogovor_id
					join user u ON u.id=dp.user_id
					LEFT JOIN service s ON s.id=a.service_id
				where a.id=%s
			""",
			onerow=1,
			values=[app_id]
		)

		if not(app):
			form.errors.append('не найдено такое приложение к договору')
		elif app['card_id']:
			form.errors.append('карта уже была создана ранее')
		elif not(app['type']) or (app['type']!=1 and app['type']!=2):
			form.errors.append('не удалось обнаружить услугу')

		if form.success():
			card_id=None
			sr_link=None
			if app['type']==1:
				# юр. услуга
				card_id=await create_ofp_card(form, app['user_id'])
			elif app['type']==2:
				# фин. услуга
				card_id=await create_fin_card(form, app['user_id'])

			print('card_id: ',card_id)
			if card_id:
				if app['type']==1:
				  sr_link=f"/edit_form/teamwork_ofp/{card_id}"
				elif app['type']==2:
				   sr_link=f"/edit_form/user_fin/{card_id}"

				await db.query(
					query=f"UPDATE dogovor_app set card_id={card_id} WHERE id={app['id']}",
					debug=1
				)
				item={
					'card_id':card_id,
					'sr_name':app['firm'],
					'sr_link':sr_link
				}

	return {'success':form.success(),'errors':form.errors, 'item':item}