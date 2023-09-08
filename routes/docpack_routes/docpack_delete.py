
#if($R->{docpack_id}=~m/^\d+$/){
def action_docpack_delete(form,R):
    count_bill=form.db.query(
        query='SELECT count(*) from bill where docpack_id=%s',
        values=[R['docpack_id']],
        onevalue=1
    )
    if count_bill:
        form.errors.append('данный пакет документов содержит счета')

    else:
        form.db.query(
            query='DELETE FROM docpack where id=%s',
            values=[R['docpack_id']]
    );


    return {'success':form.success(),'errors':form.errors}