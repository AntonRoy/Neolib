import datetime

def fin_date():
    now = list(map(int, str(datetime.date.today()).split('-')))
    now[2] += 14
    if now[1] in (1, 3, 5, 7, 8, 10, 12):
        if now[2] > 31:
            now[1] += 1
            now[2] %= 31
    elif now[1] == 2:
        if now[2] > 28 and now[0] % 4 != 0:
            now[1] += 1
            now[2] %= 28
        elif now[2] > 29:
            now[1] += 1
            now[2] %= 29
    else:
        if now[2] > 30:
            now[1] += 1
            now[2] %= 30

    if now[1] > 12:
        now[1] %= 12
        now[0] += 1

    fin = list(map(str, now))
    if len(fin[1]) == 1:
        fin[1] = '0' + fin[1]
    return '-'.join(fin)


print(fin_date())