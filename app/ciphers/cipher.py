import re
import os


def cipher11(input_text: str, mode: bool):
    # Атбаш
    if re.search('[a-zA-Z0-9#$%&*+/=^@№;<>?!`\[\]{|}~:_.,-]', input_text):
        raise ValueError("Incorrect input")

    alpha = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"
    encoding = str.maketrans(alpha+alpha.upper(), alpha[::-1]+alpha[::-1].upper())
    result = input_text.translate(encoding)
    return result


def cipher12(input_text: str, key: int, mode: bool):
    # Скитала
    if mode == 0:
        if key >= len(input_text):
            raise ValueError("Incorrect input")
        
        while len(input_text)%key != 0:
            input_text += "_"
        cols = int(len(input_text)/key)
        data = [[char for char in input_text[i * cols: (i + 1) * cols]] for i in range(key)]
        result = ""
        while len(data[key-1]) != cols:
            data[key-1].append('_')
        for i in range(0, cols, 1):
            for k in range(0, key, 1)       :
                if data[k][i] == ' ': data[k][i] = '_'
                result += data[k][i]

    elif mode == 1:
        if len(input_text) % key != 0:
            raise ValueError("Incorrect input")
        
        rows = int(len(input_text)/key)
        data = [[char for char in input_text[i * key: (i + 1) * key]] for i in range(rows)]
        result = ""
        for i in range(0, key, 1):
            for k in range(0, rows, 1):
                if data[k][i] == '_': data[k][i] = ' '
                result += data[k][i]

    return result.rstrip()


def cipher13(input_text: str, key: int, mode: bool):
    # Цезарь

    if re.search('[a-zA-Z0-9]', input_text):
        raise ValueError("Incorrect input")

    alpha = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"
    alpha_key = alpha[key:] + alpha[:key]
    if mode == 0:
        encoding = str.maketrans(alpha+alpha.upper(), alpha_key+alpha_key.upper())

    elif mode == 1:
        encoding = str.maketrans(alpha_key+alpha_key.upper(), alpha+alpha.upper())

    result = input_text.translate(encoding)
    return result


def cipher14(input_text: str, mode: bool):
    # Полибий
    alpha = [
        ['а', 'б', 'в', 'г', 'д', 'е'],
        ['ё', 'ж', 'з', 'и', 'й', 'к'],
        ['л', 'м', 'н', 'о', 'п', 'р'],
        ['с', 'т', 'у', 'ф', 'х', 'ц'],
        ['ч', 'ш', 'щ', 'ъ', 'ы', 'ь'],
        ['э', 'ю', 'я', '.', ',', '?']
    ]
    if mode == 0:
        if re.search('[a-zA-Z0-9#$%&*+/=^@№;<>!`\[\]{|}~:_-]', input_text):
            raise ValueError("Incorrect input")
        
        result = ""
        for char in input_text:
            if char == " ":
                result += " "
            else:
                num_row = 0
                for row in alpha:
                    if char.lower() in row:
                        num_col = 0
                        for col in row:
                            if char.lower() == col:
                                result += "(" + str(num_row + 1) + ',' + str(num_col + 1) + ")"
                            num_col += 1
                    num_row += 1

    elif mode == 1:
        words = re.split('\s+', input_text)
        pattern_indexes = re.compile('(\d+,\d+)')
        result = ""
        for word in words:
            indexes = pattern_indexes.findall(word)
            for pare in indexes:
                pattern_num = re.compile('\d+')
                nums = pattern_num.findall(pare)
                result += alpha[int(nums[0])-1][int(nums[1])-1]
            result += " "

    return result.rstrip()


def cipher21(input_text: str, key: str, mode: bool):
    # Колонная перестановка
    if mode == 0:
        if re.search('[a-zA-Z0-9#$%&*+/=^@№;<>?!`\[\]{|}~:_.,-]', input_text):
            raise ValueError("Incorrect input")
        key_num = re.split('\s+', key)
        cols = int(max(key_num))

        if len(input_text) < cols:
            raise ValueError("Incorrect input")

        while len(input_text) % cols != 0: input_text += "_"
        rows = int(len(input_text) / cols)
        input_text = input_text.replace(" ", "_")
        data = [[char for char in input_text[i * cols: (i + 1) * cols]] for i in range(rows)]

        result = ""
        for i in key_num:
            for k in range(0, rows, 1):
                result += data[k][int(i) - 1]
    if mode == 1:
        if re.search('[a-zA-Z0-9#$%&*+/=^@№; <>?!`\[\]{|}~:.,-]', input_text):
            raise ValueError("Incorrect input")
        key_num = re.split('\s+', key)
        cols = int(max(key_num))

        if len(input_text) % cols != 0:
            raise ValueError("Incorrect input")
        rows = int(len(input_text) / cols)
        input_text = input_text.replace("_", " ")
        data = [[char for char in input_text[i * rows: (i + 1) * rows]] for i in range(cols)]
        result = ""
        for i in range(0, rows, 1):
            for k in range(1, len(key_num) + 1, 1):
                result += data[key_num.index(str(k))][i]
    return result.rstrip()


def cipher22(input_text: str, losung: str, mode: bool):
    # Лозунговый
    import re
    if re.search('[a-zA-Z0123456789#$%&*+/=^@№;<>?!()`\[\]}{~|:_.,-]', input_text):
        raise ValueError("Incorrect input")
    alpha = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"
    key = "".join(dict.fromkeys(losung.lower()))
    key = key.replace(' ', '')
    for i in range(0, len(alpha), 1):
        if alpha[i] not in key: key += alpha[i]
    if mode == 0:
        map_ = str.maketrans(alpha + alpha.upper(), key + key.upper())

    elif mode == 1:
        map_ = str.maketrans(key + key.upper(), alpha + alpha.upper())

    result = input_text.translate(map_)
    return result


def cipher23(input_text: str, alpha_key: str, mode: bool, key: str = ""):
    # Альберти
    if re.search('[a-zA-Z0-9#$%&*+/=^@№; <>?!`\[\]{|}~:_.,-]', input_text):
        raise ValueError("Incorrect input")
    alpha = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"
    if mode == 0:
        key = key.lower()
        key_split = key.split()
        path = int(key_split[-1:][0])
        letters = key_split[:-1]
        input_text = input_text.lower()
        indicator = 0
        result = ""
        if len(letters)*path < len(input_text):
            raise ValueError("Incorrect input")
        while indicator*path < len(input_text):
            index = alpha.find(letters[indicator])
            alpha_key_final = alpha_key[index:] + alpha_key[:index]
            result += letters[indicator].upper()
            for i in range(indicator*path, indicator*path + path, 1):
                if i == len(input_text): break
                result += alpha_key_final[alpha.find(input_text[i])]
            indicator += 1

    elif mode == 1:
        upper_index = []
        upper_letters = []
        for i in range(0, len(input_text), 1):
            if input_text[i].isupper():
                upper_index.append(i)
                upper_letters.append(input_text[i])
        if len(upper_index) == 0:
            raise ValueError("Incorrect input")
        elif upper_index[0] != 0:
            raise ValueError("Incorrect input")
        else:
            if len(upper_index) == 2:
                if upper_index[1] - upper_index[0] != len(input_text)-1 - upper_index[1]:
                    raise ValueError("Incorrect input")
            elif len(upper_index) == 3:
                if upper_index[1] - upper_index[0] != upper_index[2] - upper_index[1]:
                        raise ValueError("Incorrect input")
                last = 0
                for k in range(upper_index[2]+1, len(input_text)-1, 1):
                    last += 1
                    if input_text[k].isupper():
                        raise ValueError("Incorrect input")
                if last > upper_index[1] - upper_index[0]:
                    raise ValueError("Incorrect input")
            elif len(upper_index) > 3:
                for i in range(0, len(upper_index)-3, 1):
                    if upper_index[i+1] - upper_index[i] != upper_index[i+2] - upper_index[i+1]:
                        raise ValueError("Incorrect input")
                last = 0
                for k in range(upper_index[len(upper_index)-1]+1, len(input_text)-1, 1):
                    last += 1
                    if input_text[k].isupper():
                        raise ValueError("Incorrect input")
                if last > upper_index[1] - upper_index[0]:
                    raise ValueError("Incorrect input")
            indicator = 0
            alpha_key_final = ""
            result = ""
            while indicator < len(input_text):
                if input_text[indicator].isupper():
                    index = alpha.find(input_text[indicator].lower())
                    alpha_key_final = alpha_key[index:] + alpha_key[:index]
                else:
                    result += alpha[alpha_key_final.find(input_text[indicator])]
                indicator += 1
    return result


def cipher24(input_text: str, first: str, mode: bool, second: str):
    # Два квадрата
    result = ""
    first = first.upper()
    second = second.upper()
    input_text = input_text.upper()
    for char in input_text.replace(" ", "_"):
        if char not in first:
            raise ValueError("Incorrect input")

    f_square = []
    s_square = []
    for i in range(0, 7, 1):
        f_square.append([])
        s_square.append([])
        for k in range(i * 5, (i + 1) * 5, 1):
            f_square[i].append(first[k])
            s_square[i].append(second[k])

    if mode == 0:
        if len(input_text) % 2 == 1:
            input_text += " "
        input_text = input_text.upper().replace(" ", "_")

        for i in range(0, len(input_text), 2):
            for k in range(0, 7, 1):
                if input_text[i] in f_square[k]:
                    f_string = k
                    f_row = f_square[k].index(input_text[i])
                    break
            for k in range(0, 7, 1):
                if input_text[i + 1] in s_square[k]:
                    s_string = k
                    s_row = s_square[k].index(input_text[i + 1])
                    break

            if f_string == s_string:
                result += s_square[s_string][f_row]
                result += f_square[f_string][s_row]
            else:
                result += s_square[f_string][s_row]
                result += f_square[s_string][f_row]
    elif mode == 1:
        if len(input_text) % 2 == 1:
            raise ValueError("Incorrect input")

        for i in range(0, len(input_text), 2):
            for k in range(0, 7, 1):
                if input_text[i] in s_square[k]:
                    s_string = k
                    s_row = s_square[k].index(input_text[i])
                    break
            for k in range(0, 7, 1):
                if input_text[i + 1] in f_square[k]:
                    f_string = k
                    f_row = f_square[k].index(input_text[i + 1])
                    break

            if f_string == s_string:
                result += f_square[f_string][s_row]
                result += s_square[s_string][f_row]
            else:
                result += f_square[s_string][f_row]
                result += s_square[f_string][s_row]

            result = result.replace("_", " ")

    return result.rstrip()


def cipher31(input_text: str, mode: bool):
    # Тритемий
    if re.search('[a-zA-Z0-9]', input_text):
        raise ValueError("Incorrect input")
    alpha = "абвгдежзийклмнопрстуфхцчшщъыьэюя"
    simbols = "#$%&*+/=^@№; <>?!\`[\]{|}~-:_.,"
    count = 0
    path = 0
    result = ""
    input_text = input_text.lower()
    input_text = input_text.replace("ё", "е")
    if mode == 0:
        while len(result) != len(input_text):
            if input_text[count] in simbols:
                result += input_text[count]
                count += 1
            else:
                point = alpha.find(input_text[count])
                if point + path % 32 >= len(alpha):
                    index = point + path % 32 - len(alpha)
                else:
                    index = point + path % 32
                result += alpha[index]
                count += 1
                path += 1

    elif mode == 1:
        while len(result) != len(input_text):
            if input_text[count] in simbols:
                result += input_text[count]
                count += 1
            else:
                point = alpha.find(input_text[count])
                if point - path % 32 < 0:
                    index = len(alpha) + point - path % 32
                else:
                    index = point - path % 32
                result += alpha[index]
                count += 1
                path += 1

    return result


def cipher32(input_text: str, key: str, mode: bool):
    # Виженер
    if re.search('[a-zA-Z]', input_text):
        raise ValueError("Incorrect input")
    alpha = "абвгдежзийклмнопрстуфхцчшщъыьэюя"
    result = ""
    input_text = input_text.replace('ё', 'е')
    text = input_text
    simbols = "#$%&*+/=^@№; <>?!\`[\]{|}~-:_.,0123456789"
    count = 0
    for char in text:
        if char in simbols:
            text = text[:count] + text[count + 1:]
        else:
            count += 1
    while len(key) < len(text):
        key += key
    map = list(zip(text.lower(), key.lower()))

    if mode == 0:
        for i in range(0, len(text), 1):
            point = alpha.find(map[i][0])
            path = alpha.find(map[i][1])
            if point + path >= len(alpha):
                index = point + path - len(alpha)
            else:
                index = point + path
            result += alpha[index]

    elif mode == 1:
        for i in range(0, len(text), 1):
            index = alpha.find(map[i][0])
            path = alpha.find(map[i][1])
            if index - path < 0:
                point = len(alpha) + index - path
            else:
                point = index - path
            result += alpha[point]
    points = [i for i, c in enumerate(input_text) if c in simbols]
    for i in points:
        result = result[:i] + input_text[i] + result[i:]

    return result


def cipher33(input_text: str, key: str, mode: bool):
    # Гронсфельд
    if re.search('[a-zA-Z]', input_text):
        raise ValueError("Incorrect input")
    alpha = "абвгдежзийклмнопрстуфхцчшщъыьэюя"
    result = ""
    input_text = input_text.replace('ё', 'е')
    text = input_text
    simbols = "#$%&*+/=^@№; !\`][\{|}~-?,.0123456789"
    count = 0
    for char in text:
        if char in simbols:
            text = text[:count] + text[count+1:]
        else:
            count += 1
    if len(text) < len(key):
        raise ValueError("Incorrect input")
    while(len(key) < len(input_text)):
        key += key
    map = list(zip(text.lower(), key.lower()))

    if mode == 0:
        for i in range(0, len(text), 1):
            point = alpha.find(map[i][0])
            path = int(map[i][1])
            if point + path >= len(alpha): index = point + path - len(alpha)
            else: index = point + path
            result += alpha[index]

    elif mode == 1:
        for i in range(0, len(text), 1):
            index = alpha.find(map[i][0])
            path = int(map[i][1])
            if index - path < 0: point = len(alpha) + index - path
            else: point = index - path
            result += alpha[point]

    points = [i for i, c in enumerate(input_text) if c in simbols]
    for i in points:
        result = result[:i] + input_text[i] + result[i:]

    return result


def cipher34(input_text: str, key: str, mode: bool):
    # Плейфер
    if re.search('[a-zA-Z#$%&*+/=^@№<₽>()\[\]{|}~_0123456789]', input_text):
        raise ValueError("Incorrect input")
    key = key.lower()
    input_text = input_text.lower()
    key = key.replace("ё", "е")
    input_text = input_text.replace("ё", "е")
    alpha = "абвгдежзийклмнопрстуфхцчшщъыьэюя"
    simbols = " ?!.,-:;`'"""

    text = input_text
    count = 0
    for char in text:
        if char in simbols:
            text = text[:count] + text[count+1:]
        else:
            count += 1
    if len(text) == 0:
        raise ValueError("Incorrect input")
    
    count = 0
    for char in key:
        if char in simbols:
            key = key[:count] + key[count+1:]
        else:
            count += 1
    key = "".join(dict.fromkeys(key.lower()))
    key = key.replace(' ', '')
    for i in range(0, len(alpha), 1):
        if alpha[i] not in key: key += alpha[i]
    key_map = []
    for i in range(0, 4, 1):
        key_map.append([])
        for k in range(i*8, i*8+8, 1):
            key_map[i].append(key[k])
    letter_str = -1
    letter_row = -1
    for i in range(0, 4, 1):
            if "ъ" in key_map[i]:
                letter_str = i
                letter_row = key_map[i].index("ъ")

    f_string = -1
    f_row = -1
    s_string = -1
    s_row = -1
    if mode == 0:
        if len(text)%2 == 1:
            if text[len(text)-1] == "ъ":
                raise ValueError("Incorrect input")
            else:
                text += "ъ"

        result = ""
        for i in range(0, len(text), 2):
            for k in range(0, 4, 1):
                if text[i] in key_map[k]:
                    f_string = k
                    f_row = key_map[k].index(text[i])
                    break
            for k in range(0, 4, 1):
                if text[i+1] in key_map[k]:
                    s_string = k
                    s_row = key_map[k].index(text[i+1])
                    break

            if key_map[f_string][f_row] == key_map[s_string][s_row]:
                s_string = letter_str
                s_row = letter_row
            
            if f_row == s_row:
                result += key_map[(f_string+1)%4][f_row]
                result += key_map[(s_string+1)%4][s_row]
            elif f_string == s_string:
                result += key_map[f_string][(f_row+1)%8]
                result += key_map[s_string][(s_row+1)%8]
            else:
                result += key_map[f_string][s_row]
                result += key_map[s_string][f_row]

    elif mode == 1:
        if len(text)%2 == 1:
            raise ValueError("Incorrect input")
        
        result = ""
        for i in range(0, len(text), 2):
            for k in range(0, 4, 1):
                if text[i] in key_map[k]:
                    f_string = k
                    f_row = key_map[k].index(text[i])
                    break
            for k in range(0, 4, 1):
                if text[i+1] in key_map[k]:
                    s_string = k
                    s_row = key_map[k].index(text[i+1])
                    break
            
            if key_map[f_string][f_row] == key_map[s_string][s_row]:
                raise ValueError("Incorrect input")
            
            if f_row == s_row:
                result += key_map[(4+f_string-1)%4][f_row]
                result += key_map[(4+s_string-1)%4][s_row]
            elif f_string == s_string:
                result += key_map[f_string][(8+f_row-1)%8]
                result += key_map[s_string][(8+s_row-1)%8]
            else:
                result += key_map[f_string][s_row]
                result += key_map[s_string][f_row]
    
    points = [i for i, c in enumerate(input_text) if c in simbols]
    for i in points:
        result = result[:i] + input_text[i] + result[i:]
    return result


def cipher41(input_text: str, key_alpha: str, mode: bool, key_word: str):
    # ADFGVX
    alpha = "abcdefghijklmnopqrstuvwxyz"
    key = "ADFGVX"

    result = ""
    if mode == 0:
        if re.search('[а-яА-Я#$%&,.!?*+/=^@№<₽>()`\[\]{|}~_]', input_text):
            raise ValueError("Incorrect input")

        map = []
        for i in range(0, 6, 1):
            map.append([])
            for k in range(i * 6, (i + 1) * 6, 1):
                map[i].append(key_alpha[k])
        text = input_text.lower()
        count = 0
        for char in text:
            if char == " ":
                text = text[:count] + text[count + 1:]
            else:
                count += 1

        code = ""
        for char in text:
            for i in range(0, 6, 1):
                if char in map[i]:
                    index = map[i].index(char)
                    code += key[i] + key[index]
        key_map = []
        while (len(code) % len(key_word) != 0):
            code += "_"
        for i in range(0, int(len(code) / len(key_word)), 1):
            key_map.append([])
            for k in range(i * len(key_word), (i + 1) * len(key_word), 1):
                key_map[i].append(code[k])

        ordered_word = ""
        count = 0
        for char in key_word.lower():
            if count == 0:
                ordered_word += char
            elif count == 1:
                if alpha.index(char) < alpha.index(ordered_word[0]):
                    ordered_word = char + ordered_word
                else:
                    ordered_word = ordered_word + char
            else:
                len_before = len(ordered_word)
                for i in range(0, len(ordered_word), 1):
                    if alpha.index(char) <= alpha.index(ordered_word[i]):
                        if i == 0:
                            ordered_word = char + ordered_word
                        else:
                            ordered_word = ordered_word[:i] + char + ordered_word[i:]
                        break
                if len_before == len(ordered_word):
                    ordered_word += char
            count += 1

        for i in range(0, len(ordered_word), 1):
            count = 0
            if i > 0:
                if ordered_word[i] == ordered_word[i - 1]:
                    count += 1
                    while i - count > 0:
                        if ordered_word[i - count] == ordered_word[i - 1 - count]:
                            count += 1
                        else:
                            break
            if count == 0:
                index = key_word.lower().index(ordered_word[i])
            else:
                index = key_word.lower().find(ordered_word[i], key_word.lower().find(ordered_word[i]) + count)
            for i in range(0, int(len(code) / len(key_word)), 1):
                result += key_map[i][index]

    elif mode == 1:
        if re.search('[а-яА-Я0123456789#$%&*+/=^.,!?@№<₽>()\[\]{|}~ ]', input_text):
            raise ValueError("Incorrect input")

        for char in input_text:
            if char != "_":
                if char not in key:
                    raise ValueError("Incorrect input")

        map = []
        for i in range(0, 6, 1):
            map.append([])
            for k in range(i * 6, (i + 1) * 6, 1):
                map[i].append(key_alpha[k])
        text = input_text.upper()
        if len(text) % len(key_word) != 0:
            raise ValueError("Incorrect input")

        ordered_word = ""
        count = 0
        for char in key_word.lower():
            if count == 0:
                ordered_word += char
            elif count == 1:
                if alpha.index(char) < alpha.index(ordered_word[0]):
                    ordered_word = char + ordered_word
                else:
                    ordered_word = ordered_word + char
            else:
                len_before = len(ordered_word)
                for i in range(0, len(ordered_word), 1):
                    if alpha.index(char) <= alpha.index(ordered_word[i]):
                        if i == 0:
                            ordered_word = char + ordered_word
                        else:
                            ordered_word = ordered_word[:i] + char + ordered_word[i:]
                        break
                if len_before == len(ordered_word):
                    ordered_word += char
            count += 1
        count = 0
        code = ""

        for i in range(0, len(key_word), 1):
            index = ordered_word.index(key_word.lower()[i])
            count = 0
            while index + count < len(ordered_word) - 1:
                if ordered_word[index + count] == ordered_word[index + 1 + count]:
                    count += 1
                else:
                    break

            minus = count
            for k in range(0, i, 1):
                if key_word[k] == ordered_word[index]:
                    minus -= 1
            count -= minus
            if count != 0:
                index = ordered_word.find(key_word[i], ordered_word.find(key_word[i]) + count)
            code += text[index * (int(len(text) / len(key_word))):(index + 1) * (int(len(text) / len(key_word)))]
        ordered_map = []
        for i in range(0, int(len(text) / len(key_word)), 1):
            ordered_map.append([])
        for i in range(0, len(key_word), 1):
            for k in range(0, int(len(text) / len(key_word)), 1):
                ordered_map[k].append(code[i * int(len(text) / len(key_word)) + k])
        code = ""
        for i in range(0, int(len(text) / len(key_word)), 1):
            for k in range(0, len(key_word), 1):
                code += ordered_map[i][k]
        result = ""
        for i in range(0, len(code), 2):
            if code[i] == "_":
                break
            y = key.find(code[i])
            x = key.find(code[i + 1])
            result += map[y][x]

    return result


def cipher42(input_text: str, key: str, mode: bool):
    # Энигма
    if mode == 0 and re.search('[а-яА-Я#$%&*+/=^@№<₽>()`\[\]{|}~_0123456789]', input_text):
        raise ValueError("Incorrect input")
    elif mode == 1 and re.search('[а-яА-Я#$%&*+/=^@№<₽>()`\[\]{|}~_0123456789]', input_text):
        raise ValueError("Incorrect input")
    import pandas as pd

    path = os.path.abspath("enums/vars_for_enigma.xlsx")
    file = pd.read_excel(io=path,
                         engine='openpyxl',
                         sheet_name=['Лист1', 'Лист2', 'Лист3'])
    if len(file["Лист1"].values.tolist()) < len(input_text):
        raise ValueError("Incorrect input")
    alpha = "abcdefghijklmnopqrstuvwxyz"
    keys = ["TCP AES", "PLP QLO", "WMJ ISF"]
    keys_cip = ["TCP IJT", "PLP WXJ", "WMJ KDJ"]
    result = ""
    if mode == 0:
        vars = file["Лист" + str(keys.index(key.upper()) + 1)]
        letters = vars.values.tolist()
        result = keys_cip[keys.index(key.upper())] + " "
        step = 0
        for char in input_text.lower().replace(" ", ""):
            num = alpha.index(char)
            result += letters[step][num]
            step += 1
            if step % 5 == 0:
                result += " "
    elif mode == 1:
        vars = file["Лист" + str(keys_cip.index(key.upper()) + 1)]
        letters = vars.values.tolist()
        result = keys[keys_cip.index(key.upper())] + " "
        step = 0
        for char in input_text.lower().replace(" ", ""):
            num = letters[step].index(char)
            result += alpha[num]
            step += 1
    return result


def cipher43(input_text: str, key_word: str, mode: bool):
    # Вернам
    if re.search('[a-zA-Z#$%&*+/=.,!?^@№<₽>()`\[\]{|}~_0123456789ё]', input_text):
        raise ValueError("Incorrect input")

    text = input_text.lower()
    count = 0
    for char in text:
        if char == " ":
            text = text[:count] + text[count + 1:]
        else:
            count += 1

    key = key_word.lower()
    count = 0
    for char in key:
        if char == " ":
            key = key[:count] + key[count + 1:]
        else:
            count += 1
    if len(text) != len(key):
        raise ValueError("Incorrect input")

    result = ""
    alpha = {
        "а": "00000", "б": "00001", "в": "00010", "г": "00011", "д": "00100", "е": "00101",
        "ж": "00110", "з": "00111", "и": "01000", "й": "01001", "к": "01010", "л": "01011",
        "м": "01100", "н": "01101", "о": "01110", "п": "01111", "р": "10000", "с": "10001",
        "т": "10010", "у": "10011", "ф": "10100", "х": "10101", "ц": "10110", "ч": "10111",
        "ш": "11000", "щ": "11001", "ъ": "11010", "ы": "11011", "ь": "11100", "э": "11101",
        "ю": "11110", "я": "11111"
    }
    for i in range(0, len(text), 1):
        num_text = alpha.get(text[i])
        num_key = alpha.get(key[i])
        num_letter = ""
        for k in range(0, 5, 1):
            if num_key[k] == num_text[k]:
                num_letter += "0"
            else:
                num_letter += "1"
        for letter, num in alpha.items():
            if num == num_letter:
                result += letter
                break
    points = [i for i, c in enumerate(input_text) if c == " "]
    for i in points:
        result = result[:i] + input_text[i] + result[i:]
    return result


def cipher51(input_text: str, key: str, mode: str):
    # DES
    from bitarray import bitarray
    if mode == 0:
        bits = bitarray(''.join([bin(int('1' + hex(c)[2:], 16))[3:] for c in input_text.encode('utf-8')])).to01()
        if len(bits) > 14528:
            raise ValueError("Incorrect input")
        symbols = "abcdefghijklmnopqrstuvwxyzабвгдеёжзийклмнопрстуфхцчшщъыьэюя#$%&*+/ -=`.,!?^@№<₽>()\[:]{|}~_0123456789"
        for char in input_text.lower():
            if char not in symbols:
                raise ValueError("Incorrect input")
    elif mode == 1:
        symbols = "0x123456789abcdef"
        for char in input_text.lower():
            if char not in symbols:
                raise KeyError("Incorrect input")
    s_box_table = (
        (
            (14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7),
            (0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8),
            (4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0),
            (15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13),
        ),
        (
            (15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10),
            (3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5),
            (0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15),
            (13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9),
        ),
        (
            (10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8),
            (13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1),
            (13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7),
            (1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12),
        ),
        (
            (7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15),
            (13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9),
            (10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4),
            (3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14),
        ),
        (
            (2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9),
            (14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6),
            (4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14),
            (11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3),
        ),
        (
            (12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11),
            (10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8),
            (9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6),
            (4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13),
        ),
        (
            (4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1),
            (13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6),
            (1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2),
            (6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12),
        ),
        (
            (13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7),
            (1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2),
            (7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8),
            (2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11),
        )
    )

    begin_replace_table = (
        58, 50, 42, 34, 26, 18, 10, 2,
        60, 52, 44, 36, 28, 20, 12, 4,
        62, 54, 46, 38, 30, 22, 14, 6,
        64, 56, 48, 40, 32, 24, 16, 8,
        57, 49, 41, 33, 25, 17, 9, 1,
        59, 51, 43, 35, 27, 19, 11, 3,
        61, 53, 45, 37, 29, 21, 13, 5,
        63, 55, 47, 39, 31, 23, 15, 7
    )

    end_replace_table = (
        40, 8, 48, 16, 56, 24, 64, 32,
        39, 7, 47, 15, 55, 23, 63, 31,
        38, 6, 46, 14, 54, 22, 62, 30,
        37, 5, 45, 13, 53, 21, 61, 29,
        36, 4, 44, 12, 52, 20, 60, 28,
        35, 3, 43, 11, 51, 19, 59, 27,
        34, 2, 42, 10, 50, 18, 58, 26,
        33, 1, 41, 9, 49, 17, 57, 25
    )

    key_replace_table = (
        57, 49, 41, 33, 25, 17, 9, 1, 58, 50, 42, 34, 26, 18,
        10, 2, 59, 51, 43, 35, 27, 19, 11, 3, 60, 52, 44, 36,
        63, 55, 47, 39, 31, 23, 15, 7, 62, 54, 46, 38, 30, 22,
        14, 6, 61, 53, 45, 37, 29, 21, 13, 5, 28, 20, 12, 4
    )
    key_select_table = (
        14, 17, 11, 24, 1, 5, 3, 28, 15, 6, 21, 10,
        23, 19, 12, 4, 26, 8, 16, 7, 27, 20, 13, 2,
        41, 52, 31, 37, 47, 55, 30, 40, 51, 45, 33, 48,
        44, 49, 39, 56, 34, 53, 46, 42, 50, 36, 29, 32
    )

    extend_table = (
        32, 1, 2, 3, 4, 5,
        4, 5, 6, 7, 8, 9,
        8, 9, 10, 11, 12, 13,
        12, 13, 14, 15, 16, 17,
        16, 17, 18, 19, 20, 21,
        20, 21, 22, 23, 24, 25,
        24, 25, 26, 27, 28, 29,
        28, 29, 30, 31, 32, 1
    )

    p_box_replace_table = (
        16, 7, 20, 21, 29, 12, 28, 17, 1, 15, 23, 26, 5, 18, 31, 10,
        2, 8, 24, 14, 32, 27, 3, 9, 19, 13, 30, 6, 22, 11, 4, 25,
    )

    left_shift_amounts = (1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1)

    def text_in_bin(text: str):
        return bitarray(
            ''.join([bin(int('1' + hex(c)[2:], 16))[3:]
                     for c in text.encode('utf-8')])).to01()

    def bin_in_text(text: str) -> str:
        bytes_data = int(text, 2).to_bytes((len(text) + 7) // 8, byteorder='big')
        try:
            res = bytes_data.decode('utf-8')
        except:
            raise ValueError("Incorrect input")
        return str(res)

    def not_or(a: str, b: str) -> str:
        result = ""
        size = len(a) if len(a) < len(a) else len(b)
        for i in range(size):
            result += '0' if a[i] == b[i] else '1'
        return result

    def s_box_replace(block48: str) -> str:
        result = ""
        for i in range(8):
            row_bit = (block48[i * 6] + block48[i * 6 + 5]).encode("utf-8")
            line_bit = (block48[i * 6 + 1: i * 6 + 5]).encode("utf-8")
            row = int(row_bit, 2)
            line = int(line_bit, 2)
            data = s_box_table[i][row][line]
            no_full = str(bin(data))[2:]
            while len(no_full) < 4:
                no_full = '0' + no_full
            result += no_full
        return result

    def s_box_compression(key: str, block48: str) -> str:
        result_not_or = not_or(block48, key)
        return s_box_replace(result_not_or)

    def left_shift(bits, amount):
        return bits[amount:] + bits[:amount]

    def generate_keys(key: str):
        binary_key = cipher53(key, 1)
        permuted_key = replace_block(binary_key, key_replace_table)
        left_half = permuted_key[:28]
        right_half = permuted_key[28:]

        round_keys = []
        for i in range(16):
            left_half = left_shift(left_half, left_shift_amounts[i])
            right_half = left_shift(right_half, left_shift_amounts[i])
            combined_key = left_half + right_half
            round_key = [combined_key[index - 1] for index in key_select_table]
            round_keys.append(round_key)
        return round_keys

    def union_blocks(right: str, is_decode: bool, num: int, key_list: list):
        extended_block = ""
        for i in extend_table:
            extended_block += right[i - 1]
        if is_decode:
            sbc_result = s_box_compression(key_list[15 - num], extended_block)
        else:
            sbc_result = s_box_compression(key_list[num], extended_block)
        return replace_block(sbc_result, p_box_replace_table)

    def encode_input(text: str, key: str, mode: bool):
        result = ""
        blocks = []
        bin_string_text = text_in_bin(text)
        if len(bin_string_text) % 64 != 0:
            for i in range(64 - len(bin_string_text) % 64):
                bin_string_text += '0'
        for i in range(len(bin_string_text) // 64):
            blocks.append(bin_string_text[i * 64: i * 64 + 64])
        for i in range(0, len(blocks), 1):
            block = replace_block(blocks[i], begin_replace_table)
            key_list = generate_keys(key)
            for k in range(16):
                left, right = block[0: 32], block[32: 64]
                next_left = right
                f_result = union_blocks(right, mode, k, key_list)
                right = not_or(left, f_result)
                block = next_left + right
            block_result = block[32:] + block[:32]
            block_result = replace_block(block_result, end_replace_table)
            result += str(hex(int(block_result, 2)))
        return result

    def formating_decode_text(enter: str) -> list:
        result = []
        try:
            input_list = enter.split("0x")[1:]
            int_list = [int("0x" + i, 16) for i in input_list]
            for i in int_list:
                bin_data = str(bin(i))[2:]
                while len(bin_data) < 64:
                    bin_data = '0' + bin_data
                result.append(bin_data)
            return result
        except Exception as e:
            raise

    def decode_input(text: str, key: str, mode: bool):
        blocks = formating_decode_text(text)
        result = []
        for i in range(0, len(blocks), 1):
            block = replace_block(blocks[i], begin_replace_table)
            key_list = generate_keys(key)
            for k in range(16):
                left, right = block[0: 32], block[32: 64]
                next_left = right
                f_result = union_blocks(right, mode, k, key_list)
                right = not_or(left, f_result)
                block = next_left + right
            block_result = block[32:] + block[:32]
            block_result = replace_block(block_result, end_replace_table)
            for k in range(0, len(block_result), 8):
                result.append(block_result[k: k + 8])
        return bin_in_text(''.join(result))

    def replace_block(block: str, replace_table: tuple) -> str:
        result = ""
        for i in replace_table:
            result += block[i - 1]
        return result

    result = ""
    if mode == 0:
        result = encode_input(input_text, key, 0)
    elif mode == 1:
        result = decode_input(input_text, key, 1).rstrip('\x00')
    return result


def cipher52(input_text: str, key: str, mode: bool):
    # Threefish
    if mode == 0 and len(input_text) > 32:
        raise ValueError("Incorrect input")
    elif mode == 1:
        symbols = "0x123456789abcdef"
        for char in input_text.lower():
            if char not in symbols:
                raise ValueError("")
        res = [str(num) for num in
               [bin(int(hex_num, 16)).replace('0b', '').zfill(64) for hex_num in input_text.split('0x')[1:]]]
        if len(''.join(res)) != 512:
            raise ValueError("Incorrect input")
    import numpy as np
    from bitarray import bitarray
    np.seterr(all='ignore')

    blockSize = 512
    Nw = 8
    Nr = 72
    tweak_value = ["1000000000000001", "0000000110000000"]
    p = np.array([2, 1, 4, 7, 6, 5, 0, 3], dtype=np.uint32)
    p_1 = np.array([6, 1, 0, 7, 2, 5, 4, 3], dtype=np.uint32)

    r = np.array([
        [38, 30, 50, 53],
        [48, 20, 43, 31],
        [34, 14, 15, 27],
        [26, 12, 58, 7],
        [33, 49, 8, 42],
        [39, 27, 41, 14],
        [29, 26, 11, 9],
        [33, 51, 39, 35]
    ], dtype=np.uint32)

    t = np.zeros(3, dtype=np.uint64)
    subKeys = np.zeros((Nr // 4 + 1, Nw), dtype=np.uint64)

    def _mix(x, r, y):
        y[0] = x[0] + x[1]
        # Выполнение циклического сдвига влево и вправо
        left_shifted = (x[1] << r) & 0xFFFFFFFFFFFFFFFF  # Циклический сдвиг влево
        rr = np.uint64(64 - r)
        right_shifted = (x[1] >> rr) & 0xFFFFFFFFFFFFFFFF  # Циклический сдвиг вправо
        y[1] = np.uint64(left_shifted | right_shifted)
        # XOR операция
        y[1] ^= y[0]

    def _demix(y, r, x):
        y[1] ^= y[0]
        rr = np.uint64(64 - r)
        left_shifted = (y[1] << rr) & 0xFFFFFFFFFFFFFFFF  # Циклический сдвиг влево
        right_shifted = (y[1] >> r) & 0xFFFFFFFFFFFFFFFF  # Циклический сдвиг вправо
        x[1] = np.uint64(left_shifted | right_shifted)
        x[0] = y[0] - x[1]

    def crypt(plain, c):
        v = np.array(plain, dtype=np.uint64)
        for round in range(Nr):
            if round % 4 == 0:
                s = round // 4
                e = v + subKeys[s]
            else:
                e = v.copy()
            f = np.zeros(Nw, dtype=np.uint64)
            for i in range(Nw // 2):
                x = np.zeros(2, dtype=np.uint64)
                x[0] = e[i * 2]
                x[1] = e[i * 2 + 1]
                y = np.zeros(2, dtype=np.uint64)
                _mix(x, r[round % 8][i], y)
                f[i * 2] = y[0]
                f[i * 2 + 1] = y[1]
            v = f[p]
        c[:] = v + subKeys[Nr // 4]

    def decrypt(plain, c):
        v = np.array(plain, dtype=np.uint64)
        for round in range(Nr, 0, -1):
            if round % 4 == 0:
                s = round // 4
                f = v - subKeys[s]
            else:
                f = v.copy()
            e = f[p_1]
            for i in range(Nw // 2):
                y = np.zeros(2, dtype=np.uint64)
                y[0] = e[i * 2]
                y[1] = e[i * 2 + 1]
                x = np.zeros(2, dtype=np.uint64)
                _demix(y, r[(round - 1) % 8][i], x)
                v[i * 2] = x[0]
                v[i * 2 + 1] = x[1]
        c[:] = v - subKeys[0]

    def setup(keyData, tweakData):
        K = np.array(keyData, dtype=np.uint64)
        T = np.array(tweakData, dtype=np.uint64)
        kNw = np.uint64(6148914691236517205)
        key = np.zeros(9, dtype=np.uint64)
        key[:Nw] = K
        key[Nw] = kNw
        t[0], t[1] = T[0], T[1]
        t[2] = T[0] ^ T[1]
        for round in range(Nr // 4 + 1):
            for i in range(Nw):
                subKeys[round][i] = key[(round + i) % (Nw + 1)]
                if i == Nw - 3:
                    subKeys[round][i] += t[round % 3]
                elif i == Nw - 2:
                    subKeys[round][i] += t[(round + 1) % 3]
                elif i == Nw - 1:
                    subKeys[round][i] += round

    def text_in_data(text: str):
        # Преобразуем текст в байтовую строку в кодировке UTF-8
        encoded_text = text.encode('utf-8')
        # Создаем список шестнадцатеричных представлений каждого символа в тексте
        hex_list = [hex(byte) for byte in encoded_text]
        # Удаляем префикс '0x' из каждого элемента списка
        stripped_hex_list = [h[2:] for h in hex_list]
        # Дополняем каждое шестнадцатеричное представление нулями слева до двух символов
        zero_padded_hex_list = [h.zfill(2) for h in stripped_hex_list]
        # Преобразуем каждый элемент списка в двоичное представление и убираем первый бит
        binary_list = [bin(int('1' + h, 16))[3:] for h in zero_padded_hex_list]
        # Объединяем двоичные представления в единую строку
        binary_string = ''.join(binary_list)
        # Преобразуем строку в объект bitarray и возвращаем в виде строки из нулей и единиц
        bitstring = bitarray(binary_string).to01()
        res = []
        if len(bitstring) % 64 != 0:
            last = len(bitstring) % 64
            string = bitstring[:-last] + "0" * (64 - last) + bitstring[-last:]
        else:
            string = bitstring
        for i in range(0, len(string), 64):
            res.append(int(string[i:i + 64], 2))
        for i in range(0, Nw - len(res), 1):
            res.insert(0, 0)
        return res

    def data_in_text(data: list):
        res = []
        for num in data:
            if num != 0:
                res.append(num)
        # Преобразуем каждое число в двоичное представление и дополняем нулями до 16 бит
        binary_list = [bin(num).replace('0b', '').zfill(64) for num in res]
        binary_list[len(binary_list) - 1] = binary_list[len(binary_list) - 1][
                                            binary_list[len(binary_list) - 1].index("1"):]
        if len(binary_list[len(binary_list) - 1]) % 8 != 0:
            last = 8 - len(binary_list[len(binary_list) - 1]) % 8
            binary_list[len(binary_list) - 1] = "0" * last + binary_list[len(binary_list) - 1]
        # Объединяем двоичные представления в единую строку
        binary_string = ''.join(binary_list)
        # Разбиваем строку на куски по 8 бит
        chunks = [binary_string[i:i + 8] for i in range(0, len(binary_string), 8)]
        # Преобразуем каждый кусок в 16cc
        hex_list = [hex(int(num, 2)) for num in chunks]
        # Преобразуем 16сс в байты
        bytes_string = b''.join([bytes.fromhex(num[2:].zfill(2)) for num in hex_list])
        decoded_text = bytes_string.decode('utf-8')
        return decoded_text

    def data_in_num(data: list):
        res = ''.join([hex(int(num, 2)) for num in [bin(num).replace('0b', '').zfill(64) for num in data]])
        return res

    def num_in_data(num: str):
        result = []
        try:
            input_list = num.split("0x")[1:]
            result = [int("0x" + i, 16) for i in input_list]
            return result
        except Exception as e:
            raise

    key_data = text_in_data(key)
    setup(key_data, tweak_value)
    if mode == 0:
        text_data = text_in_data(input_text)
        ciphertext = np.zeros(Nw, dtype=np.uint64)
        crypt(text_data, ciphertext)
        return data_in_num(ciphertext)
    else:
        text_data = num_in_data(input_text)
        plaintext = np.zeros(Nw, dtype=np.uint64)
        decrypt(text_data, plaintext)
        return data_in_text(plaintext)


def cipher53(input_text: str, mode: bool):
    # Kessak
    from Crypto.Hash import keccak
    k = keccak.new(digest_bits=256)
    k.update(input_text.encode("utf-8"))
    if mode == 0:
        return k.hexdigest()
    else:
        return str(bin(int(k.hexdigest(), 16)))[2:66]
