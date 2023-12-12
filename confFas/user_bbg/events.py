from lib.send_mes import send_mes
from lib.core_crm import get_email_list_from_manager_id # get_manager, get_owner,

def permissions(form):
    #pre=form.pre
    form.ov=None

    if form.id:
        form.ov=form.db.query(
            query=f"""
                SELECT
                    wt.*, u.firm, u.inn,
                    m.group_id group_id,
                    mbgg.group_id bbg_group_id
                FROM
                    {form.work_table} wt
                    LEFT JOIN manager m ON wt.manager_id=m.id
                    LEFT JOIN manager mbgg ON wt.manager_bbg=mbgg.id

                    LEFT JOIN user u ON wt.user_id=u.id

                where wt.id=%s
            """,
            values=[form.id],
            errors=form.errors,
            onerow=1
        )
        #pre(form.manager)
        if form.ov:
            is_manager = form.manager['id'] == form.ov.get('manager_id') or form.manager['CHILD_GROUPS_HASH'].get(form.ov['group_id'])
            is_manager_bbg = form.manager['id'] == form.ov.get('manager_bbg') or form.manager['CHILD_GROUPS_HASH'].get(form.ov['bbg_group_id'])


            if is_manager or is_manager_bbg or form.manager['permissions'].get('card_bbg_edit_all'):
                # для менеджеров, менеджеров ББГ, их руководителей
                # и для сотрудников с соответствующим правом доступа разрешаем редактировать
                form.read_only=False





def after_update(form):
    #form.pre([form.ov['manager_bbg'],form.values['manager_bbg']])

    if values:=form.R.get('values'):
        old_manager_bbg=form.ov.get('manager_bbg')
        new_manager_bbg=int(values.get('manager_bbg'))

        if new_manager_bbg and new_manager_bbg != old_manager_bbg:
            # в том случае, если сменился менеджер ББГ, отправляем ему уведомление
            to=get_email_list_from_manager_id(form.db, {new_manager_bbg: 1})

            message=f"На Вас была распределена карточка ББГ {form.ov['firm']}<br>"+\
                f"<a href='{form.s.config['system_url']}/edit_form/user_bbg/{form.id}'>перейти в карточку</a>"

            send_mes(
              from_addr='info@fascrm.ru',
              to=','.join(to.keys()),
              subject=f"На Вас была распределена карточка ББГ {form.ov['firm']}",
              message=message
            )


events={
    'permissions':permissions,
    #'before_update':before_update,
    'after_update':after_update
}