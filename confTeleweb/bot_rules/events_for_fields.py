def photo_before_code(form,field):
    field['filedir']=f"./files/project_{form.s.shop_id}/bot_rules"

events={
    'photo':{
        'before_code':photo_before_code,
        #'after_save_code':photos_after_save_code
    },
}