#from lib.core import exists_arg

def get_old_values(form):
	ov=None
	if form.id:

		"""
			mfin.name mfin__name,mfin.id mfin__id,
            mfin.group_id mfin__group_id,

			LEFT JOIN manager mfin ON (mfin.id=u.manager_fin)
		"""
		ov=form.db.query(
			query='''
				SELECT 
                  wt.*,
                  mf.group_id manager_from_group, mf.email manager_from_email,
                  mf.phone manager_from_phone,
                  mt.group_id manager_to_group, mt2.group_id manager_to2_group,
                  mt.email manager_to_email, mt.phone manager_to_phone,
                  mt2.email manager_to2_email, mt2.phone manager_to2_phone,
                  u.city,
                  mu.name mu__name,
                  mg.header mg__header, mg.id m__group_id,
                  m_oso.id m_oso__id, m_oso.email m_oso__email, m_oso.group_id m_oso__group_id,
                  ( wt.product in (9,14,15) and wt.dat_session<>'0000-00-00' and date(wt.dat_session)<=curdate() and wt.win_status=0) block_card
                FROM
                  teamwork_ofp wt
                  LEFT JOIN user u ON (u.id=wt.user_id)
                  LEFT JOIN manager mf ON (mf.id=wt.manager_from)
                  LEFT JOIN manager mt ON (mt.id=wt.manager_to)
                  LEFT JOIN manager mt2 ON (mt2.id=wt.manager_to2)
                  LEFT JOIN manager mu ON (mu.id=u.manager_id)
                  LEFT JOIN manager_group mg ON (mg.id=mu.group_id)
                  LEFT JOIN manager m_oso ON (m_oso.id=wt.manager_oso)
                WHERE wt.teamwork_ofp_id=%s
			''',

			values=[form.id],
			onerow=1,
			errors=form.errors
		)

	
	if ov:
		ov['block_card']=0
	form.ov=ov
	form.old_values=ov

def permissions(form):
	form.is_manager_to=False
	form.is_manager_from=False

	get_old_values(form)
	#form.pre({'ov':form.ov})
	form.user_id=None


	if form.action in ('new','insert'):
	 	user_id=form.param('user_id')
	 	if user_id and user_id.isnumeric(): form.user_id=user_id
	
	if form.id:
		form.user_id=form.db.query(
			query='select user_id from teamwork_ofp where teamwork_ofp_id=%s',
			values=[form.id], onevalue=1
		)
		

events={
	'permissions':permissions
}