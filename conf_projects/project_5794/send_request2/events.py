async def permissions(form):
	form.fields.append(
        {
            'description':'Дата и время регистрации',
            'type':'text',
            'name':'registered',
            'filter_on':1
        }
	)

events={
	'permissions':permissions
}