from .dp.get_acts import get_acts
from .dp.ur_lico_list import ur_lico_list
from .dp.create_bill import create_bill
from .dp.number_rules import *

# from .dp.get_acts import get_acts
# from .dp.ur_lico_list import ur_lico_list
# from .dp.create_bill import create_bill
# from .dp.number_rules import *

# # async def paids_before_code(form,field):
# #     if not(form.ov) or not(form.ov.get('user_id')):
# #         return ''
# #     user_id=form.ov.get('user_id')
# #     _list=await form.db.query(query="""
# #         SELECT
# #             b.id, b.docpack_id, b.number,  DATE_FORMAT(b.paid_date,%s) paid_date, b.paid_summ summ,
# #             m.name manager, t.header tarif, ul.firm ur_lico
# #         FROM
# #             docpack dp
# #             join bill b ON b.docpack_id=dp.id
# #             LEFT join manager m ON b.manager_id=m.id
# #             LEFT JOIN tarif t ON t.id=dp.tarif_id
# #             LEFT JOIN ur_lico ul ON dp.ur_lico_id = ul.id
# #         WHERE
# #             dp.user_id=%s and b.paid=1""",

# #         values=['%d.%m.%Y', user_id],
# #         #errors=form.errors
# #     )
# #     #form.pre(_list)
# #     if len(_list):
# #         field['after_html']=form.template(
# #                 #'confFas/win_our_clients/template/table.html',
# #                 f"./{form.s.config['config_folder']}/user/templates/paids.html",
# #                 list=_list,
# #         )
# #     else:
# #         field['after_html']='<p align="center">Оплаченных счетов нет</p>'

# #     # Акты:
# #     _list=await form.db.query(
# #         query="""
# #             select
# #                 a.id, a.ur_lico_id, a.number,
# #                 DATE_FORMAT(a.dat,%s) dat, a.summa,
# #                  ul.firm ur_lico
# #             from
# #                 act2 a
# #                 join docpack dp ON dp.id=a.docpack_id
# #                 join ur_lico ul ON ul.id=dp.ur_lico_id
# #             WHERE
# #                 dp.user_id=%s
# #         """,
# #         values=['%d.%m.%Y',user_id]
# #     )
# #     if len(_list):
# #         field['after_html']+=form.template(
# #             f"./{form.s.config['config_folder']}/user/templates/acts.html",
# #             list=_list,
# #             backend_base=form.s.config.get('bakend_base','/backend')
# #         )

# # paids_field={
# #   'type':'code',
# #   'name':'paids',
# #   'tab':'paids',
# #   'before_code':paids_before_code
# # }
async def paids_field_before_code(form,field):
    #form.pre(form.ov)
    if form.ov and form.id:
        exists_app = await form.db.query(
            query="""
                SELECT
                    a.*
                FROM
                    dogovor_app a
                    JOIN service s ON s.id=a.service_id
                WHERE s.type=1 and a.card_id=%s
            """,
            values=[form.id],
            onerow=1
        )
        if exists_app:
            field['form_id']=form.ov['user_id']
            field['only_dogovor']=exists_app['dogovor_id']
            field['only_app']=exists_app['id']
        #field['form_id']=form.ov['user_id']
        #field['only_dogovor_id']=await form.db(
        #    query=""
        #)

paids_field={
  'before_code':paids_field_before_code,
  'type':'docpack',
  'name':'docpack',
  'tab':'paids',
  'not_create_docpack':True,
  'not_filter':1,
  'docpack_foreign_key':'user_id',
  'dogovor_number_rule':dogovor_number_rule,
  'bill_number_rule':bill_number_rule,
  'act_number_rule':act_number_rule,
  'ur_lico_list': ur_lico_list,
  #'get_bills':get_bills,
  'get_acts': get_acts,
  'need_services_on_bill':True,
  'service_table':'service',
  'service_field_table':'service_field',
  'create_bill':create_bill
}