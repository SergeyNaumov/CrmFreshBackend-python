def events_permission1(form):
    print('perm1')

def events_permission2(form):
    print(perm2)

def events_before_code(form):
    print('is_before_code')

events={
  'permissions':[
      events_permission1,
      events_permission2
  ],
  'before_code':events_before_code
}