def get_const(db,shop_id):
    const={}

    const_list=db.query(
        query='select name,value from const where name like (%s) and shop_id=%s',
        values=["yandexgpt%",shop_id]

    )
    if len(const_list):
        for c in const_list:
            const[c['name']]=c['value']

    return const