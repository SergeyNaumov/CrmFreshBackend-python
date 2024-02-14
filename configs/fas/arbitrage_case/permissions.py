from .query_search_tables import get_query_search_tables
from lib.core import exists_arg

def permissions(form):
    form.QUERY_SEARCH_TABLES=get_query_search_tables()


    # form.ov=None
    # form.is_admin=True

    # perm=form.manager['permissions']
    # #form.pre(perm)
    # if perm['admin_paids']:
    #     form.is_admin=True
    #     form.read_only=False
    #     form.make_delete=True

    # if form.id:
    #     form.ov=get_values(form)

    #     if form.ov:
    #         form.title=f"Акт №{form.ov['number']} от {form.ov['registered']}"
