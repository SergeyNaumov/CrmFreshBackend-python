from lib.core import exists_arg
# Преобразует список в дерево, основываясь на parent_id
def tree_use_transform(list,table_id='id'):
  list_hash={}
  new_list=[]
  for l in list:
    l['child']=[]
    list_hash[l[table_id]]=l

  for l in list:

    if exists_arg('parent_id',l):
      if exists_arg(l['parent_id'],list_hash):
        parent_item=list_hash[l['parent_id']]
        parent_item['child'].append(l)
    else:
      new_list.append(l)


  return new_list

# Преобразование massive
def massive_transform(rez):
  list=[]
  for r in rez:
    for k in r.keys():
      list.append(r[k])

  return list
