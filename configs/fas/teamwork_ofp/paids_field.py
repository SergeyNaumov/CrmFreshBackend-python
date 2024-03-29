def paids_before_code(form,field):
    if not(form.ov) or not(form.ov.get('user_id')):
        return ''
    user_id=form.ov.get('user_id')
    _list=form.db.query(query="""
        SELECT
            b.id, b.docpack_id, b.number,  DATE_FORMAT(b.paid_date,%s) paid_date, b.summ,
            m.name manager, t.header tarif, ul.firm ur_lico
        FROM
            docpack dp
            join bill b ON b.docpack_id=dp.id
            LEFT join manager m ON b.manager_id=m.id
            LEFT JOIN tarif t ON t.id=dp.tarif_id
            LEFT JOIN ur_lico ul ON dp.ur_lico_id = ul.id
        WHERE
            dp.user_id=%s and b.paid=1""",

        values=['%d.%m.%Y', user_id],
        #errors=form.errors
    )
    #form.pre(_list)
    if len(_list):
        field['after_html']=form.template(
                #'confFas/win_our_clients/template/table.html',
                f"./{form.s.config['config_folder']}/user/templates/paids.html",
                list=_list,
        )
    else:
        field['after_html']='<p align="center">Оплаченных счетов нет</p>'

paids_field={
  'type':'code',
  'name':'paids',
  'tab':'paids',
  'before_code':paids_before_code
}