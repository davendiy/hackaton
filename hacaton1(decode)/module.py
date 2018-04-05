

CODE = {1620: 11, 2025: 31, 775: 37, 76: 3}


def read_code(filename):
    global CODE
    lines = {}
    flag_n = False
    flag_read = False
    count = 1
    tmp = ''
    with open(filename, 'r', encoding='utf-8') as file:
        for line in file:
            if '\n' != line and flag_n:
                count += 1
                if count in CODE.keys():
                    flag_read = True
            elif '\n' == line and flag_read:
                lines[count] = tmp
                tmp = ''
                flag_n = True
                flag_read = False
            elif '\n' == line and not flag_n:
                flag_n = True

            if flag_read:
                tmp += line
    return lines


def search():
    a = read_code('01-Азазель.txt')
    b = read_code('02-Статский-советник.txt')
    c = read_code('03-Турецкий-гамбит.txt')
    r = [a, b, c]
    return r


if __name__ == "__main__":
    r = search()
    for row in r:
        print("\n\n\n")
        for row2, rowv in row.items():
            print(row2, ':', rowv)
