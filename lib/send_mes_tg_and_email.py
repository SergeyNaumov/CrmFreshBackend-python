from lib.send_mes_tg import send_mes_tg_managers, send_mes_vk_managers
from lib.send_mes import send_mes_email_managers
from lib.send_mes_max import send_mes_max_managers
async def send_mes_tg_and_email(ids, subject, message):
    # ids =
    #await send_mes_tg_managers(ids,message)
    await send_mes_max_managers(ids,message)
    await send_mes_vk_managers(ids,message)
    await send_mes_email_managers(ids,subject,message)

