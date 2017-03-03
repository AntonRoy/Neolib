import vk_api


class VkPlus:
    api = None

    def __init__(self, login, password, app_id=-1):
        try:
            if app_id == -1:
                self.api = vk_api.VkApi(login, password)  
            else:
                self.api = vk_api.VkApi(login, password, app_id)  

            self.api.authorization()
        except vk_api.AuthorizationError as error_msg:
            print(error_msg)
            return None


    def respond(self, to, values):
        if 'chat_id' in to:
            values['chat_id'] = to['chat_id']
            self.api.method('messages.send', values)

        else:
            values['user_id'] = to['user_id']
            self.api.method('messages.send', values)

    def send(self, body, user):
        values = {
            'message':body,
            'user_id':user
        }
        self.api.method('messages.send', values)


    def markasread(self, id):
        values = {
            'message_ids': id
        }
        self.api.method('messages.markAsRead', values)