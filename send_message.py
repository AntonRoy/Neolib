import settings
from vkplus import VkPlus

vk = VkPlus(settings.vk_login, settings.vk_password, settings.vk_app_id)


def send_msg(chat_id, msg):
    global vk
    vk.respond({u'user_id': chat_id}, {'message': msg})
