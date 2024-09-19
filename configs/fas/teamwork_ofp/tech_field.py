from lib.core import date_to_rus
async def before_code(form,field):
	# http://localhost:8081/edit_form/teamwork_ofp/58452
	if not(form.id):
		return
	db=form.db
	application = await db.query(
		query="""
			SELECT
				d.docpack_id dogovor_id, d.number dogovor_number,
				s.header service, t.bill_id bill1_id, t.postpaid_bill_id bill2_id,
				t.id, b1.number bill1_number, b2.number bill2_number,
				 date(t.registered) registered, t.summ, t.summ_post, t.num_of_dogovor number
			FROM
				tech t
				JOIN service s ON s.id=t.service_id
				JOIN bill b1 ON b1.id=t.bill_id
				JOIN dogovor d ON d.docpack_id=b1.docpack_id
				LEFT JOIN bill b2 ON b2.id=t.postpaid_bill_id

			WHERE
				t.card_id=%s AND s.type=1
			LIMIT 1
		""",
		values=[form.id],
		onerow=1
	)
	if a:=application:
		app_values = await db.query(
			query="""
				SELECT
					sf.header,
					wt.value
				FROM
					tech_values wt
					join service_field sf ON sf.id=wt.field_id
				WHERE
					tech_id=%s
				ORDER BY sf.sort
			""",
			values=[a['id']]
		)
		#form.pre(a)
		a['registered']=date_to_rus(a['registered'])

		field['after_html']=form.template(
	        f"./{form.s.config['config_folder']}/teamwork_ofp/template/tech.html",
	        a=a,
	        av=app_values,
	        backend_base=form.s.config['BakendBase']
	    )






tech_field={
	'type':'code',
	'name':'tech',
	'tab':'paids',
	'before_code':before_code
}