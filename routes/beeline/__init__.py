from fastapi import APIRouter, Request
router = APIRouter()
# {"subscriptionId":"3df9db17-3d2c-4ad7-929b-b483e0b6377b","expires":3600}
"""
url -X PUT --header 'X-MPBX-API-AUTH-TOKEN: a521ced8-d1f2-43c5-a18a-2b369de279c6' --header 'Content-Type: application/json' -d ' { "pattern" : "200", "expires" : 3600, "subscriptionType" : "BASIC_CALL", "url" : "https://fas.crm-dev.ru/backend/beeline/subscription" }'
"""
@router.get('/subscription')
async def beeline_get(subscriptionId:str):
    print(f'BEELINE GET / {subscriptionId}')
    return {'detail':'thanks'}

@router.post('/subscription')
async def beeline_post(R:dict):
    print('BEELINE POST:',R)
    return {'detail':'thanks'}