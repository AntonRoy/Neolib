# -*- coding: utf-8 -*-
import executes_from_bot

class Plugin:
    vk = None

    def __init__(self, vk):
        self.vk = vk
        print('Наличие книги')

    def getkeys(self):
        keys = [u'наличие', 'книга']
        ret = {}
        for key in keys:
            ret[key] = self
        return ret

    def call(self, msg):
        req = msg['body'].split(', ')
        req[0] = req[0][7:]
        req = list(map(lambda x: x.lower(), req))
        in_out = 0
        try:
            in_out = executes_from_bot.Book_In_Library(req[0], req[1])
            if in_out[0]:
                self.vk.respond(msg, {'message': 'Книга {0}, {1} - в библиотеке'.format(in_out[1], in_out[2])})
            else:
                self.vk.respond(msg, {'message': "Извините, но данной книги нет в библиотеке"})
        except:
            self.vk.respond(msg, {'message': "Что-то пошло не так, попробуйте еще раз"})