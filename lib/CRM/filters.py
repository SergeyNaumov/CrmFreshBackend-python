from lib.core import is_errors, create_fields_hash, exists_arg,success
from lib.all_configs import read_config
def get_filters(**arg):
  response={}
  form=read_config(
    config=arg['config'],
    script=arg['script']
  )
  #form.info()
  if is_errors(form):
    return form.fields

  #form.run_all_fields_before_code()

  filters=[]
  order=1
  for f in form.fields:
    # if(ref($f->{before_code}) eq 'CODE'){
    #   run_event(event=>$f->{before_code},description=>'before_code for '.$f->{name},form=>$form,arg=>$f);
    # }
    #if f['not_filter']: next
    #if f['type'] in ('password','code','1_to_m','hidden'): next

    if f['type'] in ('textarea','filter_extend_text'):
      f['type']='text'

    if exists_arg('filter_type',f):
      f['range']=1
    
    filters.append(f)

    # foreach my $k ( keys %{$f}){
    #   if(ref $f->{$k} eq 'CODE'){
    #     delete $f->{$k}
    #   }
    # }
  make_create=1
  if form.not_create: make_create=0
  return {
    'success':1,
    'title':form.title,
    'filters':filters,
    'search_links':form.search_links,
    'before_filters_html':form.before_filters_html,
    'javascript':form.javascript['admin_table'],
    'filters_groups':form.filters_groups,
    'log':form.log,
    'permissions':{
      'make_create':make_create,
      'make_delete':form.make_delete,
      'not_edit':form.not_edit
    },
    'on_filters':form.on_filters,
    'search_plugin':form.search_plugin,
    'search_on_load':form.search_on_load,
    'errors':form.errors

  }

  
