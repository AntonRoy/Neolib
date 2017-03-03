# -*- coding: utf-8 -*-
import executes_from_bot

class Plugin:
    vk = None

    def __init__(self, vk):
        self.vk = vk
        print('автор')

    def getkeys(self):
        keys = [u'Автор', u'автор']
        ret = {}
        for key in keys:
            ret[key] = self
        return ret

    def call(self, msg):
        workwith = 'а ты уверен'
        author = msg['body'].split()[1]
        books = executes_from_bot.Books_Of_Author_In_Library(author)
        try:
            cnt = 0
            for book in books:
                cnt += 1
                self.vk.respond(msg, {'message': str(cnt) + ')' + book[0] + ',' + ' доступно ' + str(book[1])})
        except:
            self.vk.respond(msg, {'message': books})
