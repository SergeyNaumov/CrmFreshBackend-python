from fastapi.responses import HTMLResponse

def out_debug(dp):
	tabs=[
		{'description':'Договор','name':'dog'},
		{'description':'Приложение к договору','name':'app'},
		{'description':'Счёт','name':'bill'},
		{'description':'Клиент','name':'client'},
		{'description':'Наше юр. лицо','name':'ur_lico'},
		{'description':'Изображения','name':'img'},

	]
	
	fields=[
		{
			'description':'номер договора',
			'name':'dogovor_number',
			'tab':'dog'
		},
		{'description':'дата договора','name':'dogovor_from','tab':'dog'},

		# Приложение к договору
		{
			'description':'номер приложения в рамках договора',
			'name':'app_num_of_dogovor',
			'tab':'app'
		},
		{
			'description':'сумма предоплаты',
			'name':'app_summ',
			'tab':'app'
		},
		{
			'description':'сумма предоплаты прописью',
			'name':'app_summ_prop',
			'tab':'app'
		},
		{
			'description':'сумма постоплаты','name':'app_summ_post',
			'tab':'app'
		},
		{
			'description':'сумма постоплаты прописью','name':'app_summ_post_prop',
			'tab':'app'
		},
		{
			'description':'дата создания приложения','name':'app_from',
			'tab':'app'
		},
		{
			'description':'доп. поля','name':'app_fields',
			'tab':'app'
		},
		{
			'description':'бланк для приложения','name':'app_blank',
			'tab':'app'
		},

		{'description':'должность ответственного лица в родительном падеже','name':'position_otv_rod','tab':'client'},
		{'description':'ген. дир в именительном падеже (кратко)','name':'gen_dir_f_im','tab':'client'},
		{'description':'ген. дир в именительном падеже','name':'fio_dir','tab':'client'},

		{'description':'ген. дир в родительном падеже','name':'fio_dir_rod','tab':'client'},
		
		{'description':'организация','name':'firm','tab':'client'},
		{'description':'юридический адрес','name':'ur_address','tab':'client'},
		{'description':'почтовый адрес','name':'address','tab':'client'},
		{'description':'ОГРН','name':'ogrn','tab':'client'},
		{'description':'ИНН','name':'inn','tab':'client'},
		{'description':'КПП','name':'kpp','tab':'client'},
		{'description':'банк','name':'bank','tab':'client'},
		{'description':'рассчётный счёт','name':'rs','tab':'client'},
		{'description':'кор. счёт','name':'ks','tab':'client'},


		{'description':'ген. дир в именительном падеже (кратко)','name':'ur_lico_gen_dir_f_in','tab':'ur_lico'},
		{'description':'ген. дир в именительном падеже','name':'ur_lico_gen_dir_fio_im','tab':'ur_lico'},
		{'description':'ген. дир в родительном падеже','name':'ur_lico_gen_dir_fio_rod','tab':'ur_lico'},

		
		{'description':'организация','name':'ur_lico_firm','tab':'ur_lico'},
		{'description':'рассчётный счёт','name':'ur_lico_rs','tab':'ur_lico'},
		{'description':'кор. счёт','name':'ur_lico_ks','tab':'ur_lico'},
		{'description':'ОГРН','name':'ur_lico_ogrn','tab':'ur_lico'},
		{'description':'ИНН','name':'ur_lico_inn','tab':'ur_lico'},
		{'description':'КПП','name':'ur_lico_kpp','tab':'ur_lico'},
		{'description':'БИК','name':'ur_lico_bik','tab':'ur_lico'},
		{'description':'банк','name':'ur_lico_bank','tab':'ur_lico'},
		{'description':'юр. адрес','name':'ur_lico_ur_address','tab':'ur_lico'},
		
		
		{'description':'номер счёта','name':'bill_number', 'tab':'bill'},
		{'description':'счёт от','name':'bill_from', 'tab':'bill'},
		{'description':'сумма счёта','name':'bill_summ', 'tab':'bill'},
		#{'description':'','name':''},
		# {'description':'','name':''},
		# {'description':'','name':''},
		# {'description':'','name':''},
		# {'description':'','name':''},
		# {'description':'','name':''},
		# {'description':'','name':''},

		{'description':'Печать нашего юрлица','name':'ur_lico_attach_pechat','tab':'img'},
		{'description':'Подпись генерального','name':'ur_lico_gendir_podp','tab':'img'},
		{'description':'Подпись главного бухгалтера','name':'ur_lico_buh_podp','tab':'img'},

	]

	out_html=[]
	out_html.append('<table>')
	for t in tabs:
		out_html.append(f"<tr><td colspan='2'><h2>{t['description']}</h2></td></tr>")
		tab_out=[]
		for f in fields:
			
			if f['tab']==t['name']:
				v='<span style="color: red;">не установлено</span>'
				if f['name'] in dp:
					v=dp[f['name']]
					if f['tab']=='img':
						v=f"{v} / <img src='/files/ur_lico/{v}'>"
				tab_out.append(f"""
					<tr>
						<td>{f['description']} {f['tab']}</td>
						<td>{v}</td>
						<td>{f['name']}</td>
					</tr>""")



		out_html.append(f"{''.join(tab_out)}")
	out_html.append('</table>')
	return HTMLResponse(''.join(out_html) )
"""
Клиент:


{{ur_lico_gen_dir_fio_rod}}
{{ur_lico_gen_dir_fio_im}}
{{ur_lico_firm}}
{{ur_lico_rs}}
{{ur_lico_ks}}
{{ur_lico_ogrn}}
{{ur_lico_inn}}
{{ur_lico_kpp}}
{{ur_lico_bik}}
{{ur_lico_bank}}
{{ur_lico_ur_address}}
{{ur_lico_gen_dir_fio_im}}
{{ur_lico_attach_pechat}}

{{ur_lico_gendir_podp}}
{{ur_lico_buh_fio_im}}

{{bill_number}}
{{bill_from}}
{{bill_summ}}
{{bill_summ_prop}}
{{ur_lico_gen_dir_fio_im}}
{{ur_lico_buh_podp}}
	]
"""
def check_dogovor(txt):

	return HTMLResponse()