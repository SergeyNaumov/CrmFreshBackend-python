import lib.core_crm
from lib.core import exists_arg


def link_to_card_code(form,field):
	html=''
	if form.user_id:
		html=f'''<a href="/edit_form/user/{form.user_id}" target="_blank">В карту ОП</a>'''
	field['after_html']=html

# для поля "статус клиента"
def client_status_before_code(form,field):
	if form.is_manager_to:
		
		if not(form.ov['block_card']):
			field['read_only']=False

		field['regexp_rules']=[
			'/^[1-9]$/','Выберите значение'
		]



# для поля "вид продукта"
def product_before_code(form,field):
    ap=form.param('add_param')
    if ap=='13':
        field['value']=8
        field['values']=[{'v':'8', 'd':'Подготовка документации'}]

def dat_session_before_code(form,field):
	if (not(form.ov) or not form.ov['block_card']) and (form.is_manager_from or form.is_manager_to):
            field['read_only']=False

def manager_from_before_code(form,field):
	if form.manager['login'] in ('sed','admin','akulog'): field['read_only']=False

	if form.ov and form.ov['manager_from']:
		manager_email=''
		form.pre(form.ov["manager_from_email"])
		if form.ov["manager_from_email"]:
			manager_email=f'<a href="mailto:{form.ov["manager_from_email"]}">{form.ov["manager_from_email"]}</a> ;'

		if manager_email or form.ov['manager_from_phone']:
			field['after_html']=f'''<small> {manager_email} {form.ov['manager_from_phone']}</small>'''
def group_owner_before_code(form,field):
	manager_from=None
	if form.ov:
		manager_from=core_crm.get_manager(
			id=form.ov['manager_from'],
			db=form.db
		)
	owner_from=None
	if manager_from:
		print('manager_from:',manager_from)
		# owner_from=core_crm.get_owner(
		# 	cur_manager=manager_from,
		# 	db=db
		# )
		oener_from=None
	if owner_from:
		field['after_html']='{owner_from["name"]} ; <a href="mailto:{owner_from["email"]}">owner_from["email"]</a> ; {owner_from["phone"]}';

    # code => sub{
    
    #     my $manager_from=undef;
        
    #     $manager_from=core_trade::get_manager(
    #       id=>$form->{old_values}->{manager_from},
    #       connect=>$form->{connects}->{rosexport_read}
    #     ) if($form->{old_values}->{manager_from});
    #     my $owner_from;
    #     if($manager_from){
    #       $owner_from=core_trade::get_owner(
    #         cur_manager=>$manager_from,
    #         connect=>$form->{connects}->{rosexport_read}
    #       );
    #     }
    #     return qq{$owner_from->{name} ; <a href="mailto:$owner_from->{email}">$owner_from->{email}</a> ; $owner_from->{phone}};

    # },