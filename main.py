from fastapi import Depends, FastAPI, Request, Response
from starlette.responses import JSONResponse, Response
from routes import router
from lib.engine import s
# uvicorn main:app --reload --port=5000
app = FastAPI(Debug=True)
@app.middleware("http")
async def for_all_requests(request: Request,call_next, response=Response):

  #host=request.headers['host']

  response_obj=response()
  #body = request.json()
  

  #print('BODY: ',body)
  s.reset(
    request=request,
    status_code=200
    #response=response_obj
  )

  if( s._end):
    return Response(s.to_json(s._content))
  else:

    response = await call_next(request)
    # set cookies
    for k in s.cookies.keys():
      response.set_cookie(key=k,value=s.cookies[k])
    # delete_cookies
    for k in s.cookies_for_delete:
      response.delete_cookie(k)
    
    # print_headers
    for h in s.headers:
      response.headers[h[0]] = h[1]

  return response


app.include_router(router)
