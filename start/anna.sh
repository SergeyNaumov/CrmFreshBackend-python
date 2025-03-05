#uvicorn main:app --port=5021 --workers 5 &>/dev/null &
export config=config_anna && uvicorn  --reload --port=5000 --workers 1 main:app


