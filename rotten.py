import datetime
import executes_from_bot as ex
import vkplus
import settings
from time import sleep

def main():
    time = datetime.datetime.now()
    vk = vkplus.VkPlus(settings.vk_login, settings.vk_password, settings.vk_app_id)
    if time.hour <= 21 and time.hour >= 8 and time.second == 0 and time.minute == 0:
        for i in ex.return_date():
            if i[1] >= int(time.day.split('/')[1])-1:
                vk.vk.respond({'chat_id': i[0]}, {'message':'Не думаешь, что стоит сдать книгу?'})


while True:
    main()

