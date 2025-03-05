def before_search(form):
    qs=form.query_search
    # Фильтр "юр.лицо"
    #form.pre(qs)
    on_filters_hash=qs['on_filters_hash']
    if ('ur_lico_id' in on_filters_hash) and len(on_filters_hash['ur_lico_id']):
            ids=[]
            for id in on_filters_hash['ur_lico_id']:
                ids.append(str(id))
            ids=','.join(ids)
            qs['WHERE'].append(f'(ul.id in ({ids}) OR ul2.id in ({ids}))')
    
    
    if 'apteka_id' in on_filters_hash and len(on_filters_hash['apteka_id']) :
        ids=[]
        for id in on_filters_hash['apteka_id']:
            ids.append(str(id))
        ids=','.join(ids)
        qs['WHERE'].append(f'(apt.id in ({ids}))')
    
    if 'action' in on_filters_hash:
        if 'click' in on_filters_hash['action'] and not( 'show' in on_filters_hash['action']):
            qs['WHERE'].append(f'(wt.action="click")')
        
        if 'show' in on_filters_hash['action'] and not( 'click' in on_filters_hash['action']):
            qs['WHERE'].append(f'(wt.action="show")')

events={
    'before_search':before_search
}

