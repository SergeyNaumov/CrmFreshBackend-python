def pr_bonus(form,field):
    # form.id -- action.id
    #form.pre(form.manager['ur_lico_ids'])
    #form.pre(form.manager['apt_list_ids'])
    bonus_list=[]
    if form.id and form.manager['type']==2:
        if len(form.manager['ur_lico_ids']):
            bonus_list=form.db.query(
                query=f"""
                    SELECT
                        pb.*,u.header
                    FROM
                        prognoz_bonus pb
                        LEFT JOIN ur_lico u ON u.id=pb.ur_lico_id
                    WHERE
                        pb.action_id=%s and pb.ur_lico_id in ({','.join(form.manager['ur_lico_ids'])})
                """,
                values=[form.id]
            )
            #form.pre(bonus_list)

    field['after_html']=form.template(
      './conf/action_plan/templates/prognoz_bonus.html',
      bonus_list=bonus_list
    )
    #form.pre(form.ov)