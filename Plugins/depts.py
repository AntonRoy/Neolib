# -*- coding: utf-8 -*-
import executes_from_bot

class Plugin:
    vk = None

    def __init__(self, vk):
        self.vk = vk
        print('Долги')

    def getkeys(self):
        keys = [u'долг', u'долги']
        ret = {}
        for key in keys:
            ret[key] = self
        return ret

    def call(self, msg):
        id = executes_from_bot.ID_Of_Name(msg['user_id'])
        retrn = executes_from_bot.list_of_debts(id)
        cnt = 0
        for debt in retrn:
            cnt += 1
            self.vk.respond(msg, {'message': str(cnt) + ')' + debt[3] + ', ' + debt[4]})