from fastapi import Depends, FastAPI, Request, Response

from starlette.responses import JSONResponse, Response
from routes import router
from lib.engine import s
from db import db
# uvicorn main:app --reload --port=5000
app = FastAPI(Debug=True)

@app.on_event("startup")
async def startup():
    await db.create_pool()
    print('create_pool end')


@app.middleware("http") # ""
async def for_all_requests(request: Request,call_next): # , response=Response
  #response_obj=response()
  #response = await call_next(request)
  await s.reset(
    request=request,
    status_code=200,
    #response=response_obj
  )

  #print('RESET END',s.manager)
  # Пишем информацию о посещениях пользователей
  #stat_log_record(s,request)

  if( s._end):
    return Response(s.to_json(s._content))
  else:
    #print('request.state.manager: ',request.state.manager['login'])
    response = await call_next(request)

    # set cookies
    for k in s.request.state.cookies.keys():
      response.set_cookie(key=k,value=s.request.state.cookies[k])
    # delete_cookies
    for k in s.request.state.cookies_for_delete:
      response.delete_cookie(k)
    
    # print_headers
    for h in s.headers:
      response.headers[h[0]] = h[1]

  return response


app.include_router(router)


