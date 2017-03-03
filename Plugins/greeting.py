# -*- coding: utf-8 -*-

import random


class Plugin:
    vk = None

    def __init__(self, vk):
        self.vk = vk
        print('Приветствия')

    def getkeys(self):
        keys = ['приветствие', 'greeting', 'привет']
        ret = {}
        for key in keys:
            ret[key] = self
        return ret

    def call(self, msg):
        greetings = []

        greetings.append('Я - чатбот')
        greetings.append('Запущен и готов служить')

        self.vk.respond(msg, {'message': random.choice(greetings)})
