#uvicorn main:app --port=5021 --workers 5 &>/dev/null &
export config=config_crimea && uvicorn  --reload --port=5000 --workers 1 main:app

    # --reload-dir=./templates \
    # --reload-dir=./lib \
    # --reload-dir=./files \
    

#gunicorn main:app -b "127.0.0.1:5021"

