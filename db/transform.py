# Преобразует список в дерево, основываясь на parent_id
def tree_use_transform(list,table_id='id'):
  list_hash={}
  new_list=[]
  for l in list:
    l['child']=[]
    list_hash[l[table_id]]=l

  for l in list:
    #print('l:',l)
    if l['parent_id']:
      parent_item=list_hash[l['parent_id']]
      # if not(exists_arg('child',parent_item)):
      #   parent_item['child']=[]

      parent_item['child'].append(l)
      print('parent_item:',parent_item)

    else:
      new_list.append(l)

  #print(new_list)
  return new_list

# Преобразование massive
def massive_transform(rez):
  list=[]
  for r in rez:
    for k in r.keys():
      list.append(r[k])

  return list
