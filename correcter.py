from urllib import request
from urllib.parse import quote
import json


def correct(string):
    s = string.strip().replace(' ', '+')
    blank = request.urlopen('http://speller.yandex.net/services/spellservice.json/checkText?text=%20' + quote(s))
    blank = blank.read()

    blank = json.loads(blank.decode())
    for word in blank:
        string = string.replace(word[u'word'], word[u's'][0])

    return string

print(correct('Привет рбят'))
    