from .ajax import ajax
def permissions(form):
    #form.s.project_id=0
    form.ajax=ajax

    if hasattr(form.s,'project_id') and form.s.project_id:
      fld=form.get_field('photo')
      fld['filedir']=fld['filedir'].replace('[project_id]',str(form.s.project_id) )

    header_field=form.get_field('header')
    header_field['frontend']={'ajax':{'name':'gen_url','timeout':100}}

    if form.id:
      r=form.ov=form.db.query(
        query=f"""
          select
            r.tech, r2.tech rp_tech
          from
            {form.work_table} wt
            LEFT join struct_5794_rubricator r ON wt.rubricator_id=r.id
            LEFT JOIN struct_5794_rubricator r2 ON r.parent_id=r2.id
          where wt.id={form.id}
        """,
        onerow=1
      )
      if r:
        tech=r.get('tech') or r.get('rp_tech')

        if tech:
          tech_field=form.get_field('tech')
          tech_field['values']=[
                {'d':'загрузить из рубрики','v':tech}
          ]
    #tech_field=form.get_field('tech')
    #tech_field['after_html']="""<p><a href="">dsddsds</a></p>"""



events={
  'permissions':permissions,
}
