from db import db
import os.path 
from fastapi.responses import HTMLResponse
from .check_document_data import check_dogovor, out_debug
from .num_to_text import num_to_text
from .response_doc import response_doc

async def load_bill(docpack_id,bill_id,ext:str,need_print: int, debug=0):
	dp = await db.query(
		query=f'''
			SELECT
				bcr.*,

				m.name manager_name,
				t.header tarif_name,
				t.summ tarif_summ, t.cnt_orders tarif_cnt_orders,
				t.count_days tarif_count_days, t.percent_pob, t.comment tarif_comment,
				b_bill.header b_bill_header,
				b_bill.attach bill_blank, b_bill.id b_bill_id,

				dp.registered dp_registered, dp.id dp_id, dp.tarif_id,
				ur_lico.firm ur_lico_firm, ur_lico.gen_dir_fio_im ur_lico_gen_dir_fio_im, ur_lico.gen_dir_fio_rod ur_lico_gen_dir_fio_rod,
				ur_lico.buh_fio_im ur_lico_buh_fio_im, ur_lico.buh_fio_rod ur_lico_buh_fio_rod, ur_lico.inn ur_lico_inn, ur_lico.ogrn ur_lico_ogrn,
				ur_lico.kpp ur_lico_kpp, ur_lico.rs ur_lico_rs, ur_lico.ks ur_lico_ks, ur_lico.bik ur_lico_bik, ur_lico.bank ur_lico_bank,
				ur_lico.attach ur_lico_attach, ur_lico.ur_address ur_lico_ur_address, ur_lico.address ur_lico_address,
				ur_lico.attach_pechat ur_lico_attach_pechat,ur_lico.gendir_podp ur_lico_gendir_podp, ur_lico.buh_podp ur_lico_buh_podp,
				ur_lico.gen_dir_f_in ur_lico_gen_dir_f_in, dogovor.number dogovor_number, 
				dogovor.registered dogovor_registered, dp.ur_lico_id,
				DATE_FORMAT(dogovor.registered,%s) dogovor_from,
				b.number bill_number, 
				DATE_FORMAT(b.registered,%s) bill_from, b.summ bill_summ
			FROM
				user u 
				LEFT JOIN buhgalter_card_requisits bcr ON bcr.user_id = u.id
				LEFT JOIN manager m ON (u.manager_id =m.id)
				JOIN docpack dp ON dp.user_id = u.id
				JOIN bill b ON b.docpack_id = dp.id
				LEFT JOIN dogovor  ON (dp.id=dogovor.docpack_id)
				LEFT JOIN tarif t ON (t.id = dp.tarif_id)
				LEFT JOIN blank_document b_bill ON (b_bill.id = t.blank_bill_id)
				LEFT JOIN ur_lico ON (ur_lico.id=dp.ur_lico_id)
			WHERE dp.id = %s and b.id=%s ORDER BY bcr.main desc LIMIT 1
		''', 
		#debug=1,
		values=['%e %M %Y', '%e %M %Y', docpack_id, bill_id],onerow=1
	)

	if not(dp):
		return {'error': f'пакет документов №{docpack_id} не найден'}
	
	if not(dp['bill_blank']):
		return {'error': f'не найден бланк счёта'}

	dp['dogovor_blank']=f"./files/blank_document/{dp['bill_blank']}"
	
	# Проверка бланка
	if not os.path.exists(dp['dogovor_blank']):
		message=f'''
		<div style="color: red;">Бланк документа не найден: {dp['dogovor_blank']}!</div><br>
		Возможно, он был удалён<br><br>

		Подробности:
			Тариф: <a href="/edit_form/tarif/{dp['tarif_id']}">{dp['tarif_name']}</a><br>
			tarif_id: {dp['tarif_name']}<br>
			Бланк счёта: <a href="/edit_form/blank_document/{dp['b_bill_id']}">{dp['b_bill_header']}</a><br>
		'''
		return HTMLResponse(message)

	for a in ('ur_lico_gendir_podp', 'ur_lico_buh_podp', 'ur_lico_attach_pechat'):
		if dp[a]: dp[a]=f'./files/ur_lico/{dp[a]}'

	if debug:
		return out_debug(dp)

	dp['bill_summ_prop']=num_to_text(dp['bill_summ'])
	
	empty='./routes/docpack_routes/img/empty.png'

	if not(need_print):
		dp['ur_lico_gendir_podp']=empty
		dp['ur_lico_attach_pechat']=empty


	replace_images=[
		['ur_lico_gendir_podp',dp['ur_lico_gendir_podp'] ],
		['ur_lico_attach_pechat',dp['ur_lico_attach_pechat'] ]
	]

	output_filename=f"Счёт №{dp['bill_number']}"
	return response_doc(dp['dogovor_blank'], output_filename, ext, dp, replace_images) # images_list

	return dp
