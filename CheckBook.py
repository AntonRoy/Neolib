# -*- coding: utf-8 -*-
import executes_from_bot
import correcter as cr

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
        request = msg['body'].split()
        in_out = 0
        try:
            in_out = executes_from_bot.Book_In_Library(request[1], request[2])
            if in_out:
                self.vk.respond(msg, {'message': 'Книга в библиотеке'})
            else:
                self.vk.respond(msg, {'message': "Извините, но данной книги нет в библиотеке"})
        except:
            self.vk.respond(msg, {'message': "Что-то пошло не так..."})
            self.vk.respond(msg, {'message': "Возможно ты имели ввиду " + cr.correct(msg['body'][1:])})