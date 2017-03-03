import os
import sys


class Plugin:
    vk = None

    def __init__(self, vk):
        self.vk = vk
        print('Список плагинов')

    def getkeys(self):
        keys = ['help', 'помощь', 'plugins']
        ret = {}
        for key in keys:
            ret[key] = self
        return ret

    def call(self, msg):
        lists = ''
        path = 'plugins/'
        sys.path.insert(0, path)
        for f in os.listdir(path):
            fname, ext = os.path.splitext(f)
            if ext == '.py':
                lists += fname + ' '
        sys.path.pop(0)
        self.vk.respond(msg, {'message': 'Functions:\n/автор - все книги данного автора в библиотеке\n/долг - ваши несданные книги\n/книга - проверка наличия данной книги в библиотеке\n/жанр - все книги данного жанра в библиотеке\n/rand - рандомное число от 1 до 6, /rand 6 10 - это рандомные числа от 6 до 10'})