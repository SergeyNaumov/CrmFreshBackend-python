from fastapi import Depends, FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from inspect import signature

from starlette.responses import JSONResponse, Response
from routes import router
from lib.engine import Engine
from config import config
from db import get_db

# uvicorn main:app --reload --port=5000
app = FastAPI(Debug=True)

# Локальная отладка: фронт (vite/webpack dev-server) живёт на 127.0.0.1:8081 или
# localhost:8081, поэтому перечислять порты списком бессмысленно -- vite меняет
# порт при заняттом 8081. Разрешаем петлю на любом порту.
# ВАЖНО: в allow_origins нужен именно "*", а не "*:*" -- только "*" включает
# режим allow_all_origins в starlette. "*:*" не совпадёт ни с одним Origin.
dev_origin_regex = r"^https?://(localhost|127\.0\.0\.1|\[::1\])(:\d+)?$"

# Прод-домены (если фронт и бэк на разных хостах). Задаются в config_*.py
# ключом 'cors_origins'. Если ключа нет -- запросы идут same-origin через
# nginx (location /backend/ -- см. settings/nginx_section.txt) и CORS не нужен.
origins = config.get('cors_origins', [])

# Заголовки, которые браузер разрешает читать из ответа (Access-Control-Expose-Headers).
# Content-Disposition нужен, чтобы фронт мог взять имя файла из FileResponse
# (routes/docpack_routes/response_doc.py), остальные -- из того же FileResponse
# и для корректной отдачи больших файлов.
expose_headers = [
  'Content-Disposition',  # attachment; filename="..." -- имя скачиваемого файла
  'Content-Length',       # размер файла, нужен для прогресс-бара
  'Content-Range',        # докачка (Accept-Ranges: bytes)
  'Accept-Ranges',
  'Last-Modified',
  'ETag',
]

@app.on_event("startup")
async def startup():
    db=get_db()
    await db.create_pool()


    print('create_pool end')

    # Фоновые задачи (очередь crm_background): воркеры внутри процесса uvicorn.
    from lib.background import start_workers
    await start_workers()


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
      c=engine.request.state.cookies[k]
      response.set_cookie(
        key=k,
        value=c['value'],
        path=c['path'],
        samesite=c['samesite'],
        secure=c['secure'],
        httponly=c['httponly'],
      )
    # delete_cookies
    # Атрибуты должны совпадать с теми, что ставились при set_cookie,
    # иначе браузер не удалит cookie (Delete-Cookie отличается от Set-Cookie).
    for k in engine.request.state.cookies_for_delete.keys():
      c=engine.request.state.cookies_for_delete[k]
      response.delete_cookie(
        key=k,
        path=c['path'],
        samesite=c['samesite'],
        secure=c['secure'],
        httponly=c['httponly'],
      )
    
    # print_headers
    for h in engine.headers:
      response.headers[h[0]] = h[1]
    
  return response


# CORS регистрируется ПОСЛЕ for_all_requests, чтобы оказаться внешним слоем.
# Starlette кладёт каждый add_middleware в начало стека, т.е. последний
# добавленный middleware выполняется первым. Иначе при engine._end (например,
# неавторизованный запрос -> redirect из session_start) for_all_requests
# возвращает Response напрямую, не вызывая вложенное приложение, и заголовки
# Access-Control-Allow-* в ответ не попадают -- браузер показывает CORS-ошибку
# вместо 401.
cors_kwargs = {
    'allow_origins': origins,
    'allow_origin_regex': dev_origin_regex,
    'allow_credentials': True,
    'allow_methods': ["*"],
    'allow_headers': ["*"],
    'expose_headers': expose_headers,
    # Кэшировать preflight в браузере, чтобы не слать его на каждый запрос.
    'max_age': 3600,
}

# Chrome (Private Network Access) шлёт Access-Control-Request-Private-Network: true,
# когда страница открыта с внешнего/сетевого адреса, а запрос уходит на localhost
# или во внутреннюю сеть. Без этого флага starlette отвечает на такой preflight
# "400 Disallowed CORS private-network". На проверку origin это не влияет --
# allow_private_network добавляет только заголовок ответа.
# Параметр появился в starlette не сразу: в старом окружении (~/.venv,
# starlette 0.48) его нет, и переданный kwargs роняет build_middleware_stack() c
# TypeError на КАЖДОМ запросе (включая lifespan -> startup-хук create_pool не
# выполняется). Поэтому передаём флаг только если он есть в сигнатуре.
# try/except вокруг add_middleware не поможет: starlette собирает стек лениво,
# уже при обработке запроса.
if 'allow_private_network' in signature(CORSMiddleware.__init__).parameters:
    cors_kwargs['allow_private_network'] = True

app.add_middleware(CORSMiddleware, **cors_kwargs)

app.include_router(router)


