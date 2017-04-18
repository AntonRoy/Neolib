import datetime
import executes_from_bot as ex


class Potato:
    def __init__(self, vk):
        self.vk = vk

    def run(self):
        time = datetime.datetime.now()

        if time.hour == 20 and time.second == 0 and time.minute == 0:
            for i in ex.return_date():
                if i[1] >= int(time.day.split('/')[1])-1:
                    self.vk.respond({'chat_id': i[0]}, {'message':'Не думаешь, что стоит сдать книгу?'})
