import module

CODE = {1620: 11, 2025: 31, 775: 37, 76: 3}


def search_for_word(s, ind):
    data = ['.', ',', ':', ';', '-', '!', '?', "'", chr(8212), chr(171), chr(187), chr(8230)]
    res = s.split()
    for i in range(len(res)):
        for symb in data:
            res[i] = res[i].replace(str(symb), '')

    while '' in res:
        res.remove("")
    if ind - 1 in range(len(res)):
        s = res[ind - 1]
    else:
        s = None
    return s


r = module.search()

words = []

for row in r:
    tmp_words = {}
    for i, v in row.items():
        tmp = search_for_word(v, CODE[i])
        tmp_words[i] = tmp
    words.append(tmp_words)

for row in words:
    print("\n\n")
    for i, v in row.items():
        print(i, ':', v)
