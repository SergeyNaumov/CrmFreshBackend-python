from fastapi import Depends, FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware

from starlette.responses import JSONResponse, Response
from routes import router
from lib.engine import Engine
from db import get_db

# uvicorn main:app --reload --port=5000
app = FastAPI(Debug=True)
origins = [
    "http://localhost",
    "http://localhost:8081",
    "http://localhost:8082",
    "*:*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["Content-Disposition"]
)
@app.on_event("startup")
async def startup():
    db=get_db()
    await db.create_pool()


    print('create_pool end')


@app.middleware("http") # ""
async def for_all_requests(request: Request,call_next): # , response=Response
  #response_obj=response()
  #response = await call_next(request)
  engine = Engine(request=request)

  await engine.reset(
    request=request,
    status_code=200,
    #response=response_obj
  )
  
  request.state.engine = engine

  if( engine._end):
    return Response(engine.to_json(engine._content))
  else:
    response = await call_next(request)

    # set cookies
    for k in engine.request.state.cookies.keys():
      response.set_cookie(key=k,value=engine.request.state.cookies[k])
    # delete_cookies
    for k in engine.request.state.cookies_for_delete:
      response.delete_cookie(k)
    
    # print_headers
    for h in engine.headers:
      response.headers[h[0]] = h[1]
    
  return response


app.include_router(router)


