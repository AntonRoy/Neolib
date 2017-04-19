import urllib
import json


def correct(string):
    s = string.strip().replace(' ', '+')
    blank = urllib.urlopen('http://speller.yandex.net/services/spellservice.json/checkText?text=%20' + s)
    blank = blank.read()
    blank = json.loads(blank)

    for word in blank:
        string = string.decode('utf-8').replace(word[u'word'], word[u's'][0]).encode('utf-8')

    return string

print(correct("Лидя"))
