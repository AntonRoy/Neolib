import urllib
import json


def correct(string):
    words = string.split(' ')
    blank = ''

    for word in words:
        blank += word+'+'

    blank = 'http://speller.yandex.net/services/spellservice.json/checkText?text=%20' + blank[:-1]
    result = urllib.urlopen(blank).read()
    result = json.loads(result)

    for word in result:
        if len(word['s']) > 0 :
            string = string.replace(word[u'word'], word[u's'][0])

    return string

print correct('hellomyname')
