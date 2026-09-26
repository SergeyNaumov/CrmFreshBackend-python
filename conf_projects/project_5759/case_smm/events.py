def after_insert(form):
    form.db.query(
        query=f"UPDATE {form.work_table} SET sort=id*10 WHERE id=%s",
        values=[form.id]
    )

events={
    #'after_insert':after_insert
}