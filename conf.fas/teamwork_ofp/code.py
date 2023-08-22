import lib.core_crm
from lib.core import exists_arg




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