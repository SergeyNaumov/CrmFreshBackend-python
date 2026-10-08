from pprint import pprint
from db import get_db

db=get_db(sync=1)
u=db.query(query="select * from user limit 1", onerow=1)
pprint(u)
