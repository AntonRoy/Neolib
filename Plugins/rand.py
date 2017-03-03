# -*- coding: utf-8 -*-

import random


class Plugin:
    vk = None

    def __init__(self, vk):
        self.vk = vk
        print('Рандом')

    def getkeys(self):
        keys = [u'рандом', u'ранд', 'random', 'rand', 'dice', 'кубик']
        ret = {}
        for key in keys:
            ret[key] = self
        return ret

    def call(self, msg):
        args = msg['body'].split()
        num = 0
        try:
            if len(args) == 3:
                if int(args[1]) < 0:
                    num = random.randint(int(args[1]), 0)
                else:
                    num = random.randint(0, int(args[1]))
            elif len(args) > 3:
                if int(args[1]) < int(args[2]):
                    num = random.randint(int(args[2]), int(args[3]))
                else:
                    num = random.randint(int(args[3]), int(args[2]))
            else:
                num = random.randint(1, 6)

            self.vk.respond(msg, {'message': str(num)})
        except:
            print('Некорректный формат запроса')
            return