import re


def key_validation12(key_number: str):
    try:
        val = int(key_number)
        if val <= 0:
            raise ValueError("Incorrect input")
    except ValueError:
        raise ValueError("Incorrect input")


def key_validation13(key_number: str):
    try:
        val = int(key_number)
        if val <= 0:
            raise ValueError("Incorrect input")
        if val > 32:
            raise ValueError("Incorrect input")
    except ValueError:
        raise ValueError("Incorrect input")


def key_validation21(key_number: str):
    try:
        numbers = re.split('\s+', key_number)
        numbers = list(map(int, numbers))
        max_num = max(numbers)
        if len(numbers) != max_num:
            raise ValueError("Incorrect input")
        elif sorted(numbers) != list(range(1, max_num+1)):
            raise ValueError("Incorrect input")
    except ValueError:
        raise ValueError("Incorrect input")


def key_validation22(key_string: str):
    try:
        if re.search('[a-zA-Z0123456789#$%&*+/=^@№;<>?!()`\[\]}{~|:_.,-]', key_string):
            raise ValueError("Incorrect input")
    except ValueError:
        raise ValueError("Incorrect input")


def key_validation23(alpha: str):
    try:
        alphabet = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"
        if re.search('[a-zA-Z0-9:#$%&*+/=^@№;<>?!`\[\] {|}~-]', alpha):
            raise ValueError("Incorrect input")
        input_text = alpha.lower()
        missing = ''
        for letter in alphabet:
            if letter not in input_text:
                missing = missing+letter
        if len(missing) != 0:
            raise ValueError("Incorrect input")
    except ValueError:
        raise ValueError("Incorrect input")


def key_validation23_2(key: str):
    try:
        if re.search('[a-zA-Z:#$%&*+/=^@№;<>?!`\[\]{|}~-]', key):
            raise ValueError("Incorrect input")
        key = key.lower()
        key_split = key.split()
        try:
            int(key_split[-1:][0])
        except ValueError:
            raise ValueError("Incorrect input")
        letters = key_split[:-1]
        for point in letters:
            if len(point) != 1:
                raise ValueError("Incorrect input")
    except ValueError:
        raise ValueError("Incorrect input")


def key_validation24(key_alpha: str):
    try:
        alpha = "абвгдежзиклмнопрстуфхцчшщъыьэюя:_.,"
        if re.search('[a-zA-Z0-9#$%&*+/=^@№;<>?!\[\] {|}~-]', key_alpha):
            raise ValueError("Incorrect input")
        input_text = key_alpha.lower()
        missing = ''
        for letter in alpha:
            if letter not in input_text:
                missing = missing+letter
        if len(missing) != 0:
            raise ValueError("Incorrect input")
    except ValueError:
        raise ValueError("Incorrect input")


def key_validation24_2(key_alpha: str):
    try:
        alpha = "абвгдежзиклмнопрстуфхцчшщъыьэюя:_.,"
        if re.search('[a-zA-Z0-9#$%&*+/=^@№;<>?!`\[\] {|}~-]', key_alpha):
            raise ValueError("Incorrect input")
        input_text = key_alpha.lower()
        missing = ''
        for letter in alpha:
            if letter not in input_text:
                missing = missing+letter
        if len(missing) != 0:
            raise ValueError("Incorrect input")
    except ValueError:
        raise ValueError("Incorrect input")


def key_validation32(key_number: str):
    try:
        if re.search('[ёa-zA-Z0-9#$%&*+/=^@№; <>?!`\[\]{|}~:_.,-]', key_number):
            raise ValueError("Incorrect input")
        if len(key_number.split()) > 1:
            raise ValueError("Incorrect input")
    except ValueError:
        raise ValueError("Incorrect input")


def key_validation33(key_number: str):
    try:
        if re.search('[a-zA-Z#$%&*+/=^@№; <>?!`\[\]{|}~:_.,-]', key_number):
            raise ValueError("Incorrect input")
        try:
            int(key_number)
        except ValueError:
            raise ValueError("Incorrect input")
    except ValueError:
        raise ValueError("Incorrect input")


def key_validation34(key: str):
    try:
        simbols = " ?!.,-:;`'"""
        if re.search('[a-zA-Z:#$%&*+/=^@№<₽>()`\[\]{|}~_0123456789]', key):
            raise ValueError("Incorrect input")
        count = 0
        for char in key:
            if char in simbols:
                key = key[:count] + key[count+1:]
            else:
                count += 1
        if len(key) == 0:
            raise ValueError("Incorrect input")
    except ValueError:
        raise ValueError("Incorrect input")


def key_validation41(key_alpha: str):
    try:
        alpha = "abcdefghijklmnopqrstuvwxyz0123456789"
        missing = ''
        for letter in alpha:
            if letter not in key_alpha:
                missing = missing + letter
        if len(missing) != 0:
            raise ValueError("Incorrect input")
        elif len(key_alpha) != 36:
            raise ValueError("Incorrect input")
    except ValueError:
        raise ValueError("Incorrect input")


def key_validation41_2(key_word: str):
    try:
        import re
        if re.search('[а-яА-Я:#$%&*+/=.,!?^@№<₽>()`\[\]{|}~_ 0123456789]', key_word):
            raise ValueError("Incorrect input")
    except ValueError:
        raise ValueError("Incorrect input")


def key_validation42(key: str, mode: bool):
    try:
        keys = []
        key = key.replace(" ", "")
        if mode == 0:
            keys = ["TCPAES", "PLPQLO", "WMJISF"]
        elif mode == 1:
            keys = ["TCPIJT", "PLPWXJ", "WMJKDJ"]
        if key.upper() not in keys:
            raise ValueError("Incorrect input")
    except ValueError:
        raise ValueError("Incorrect input")


def key_validation43(key_word: str):
    try:
        import re
        if re.search('[a-zA-Z:#$%&*+/=.,!?^@№<₽>()`\[\]{|}~_0123456789ё]', key_word):
            raise ValueError("Incorrect input")
    except ValueError:
        raise ValueError("Incorrect input")


def key_validation51(key_word: str):
    pass


def key_validation52(key_word: str):
    try:
        from bitarray import bitarray
        import re
        if re.search('[а-яА-Я]', key_word):
            raise ValueError("Incorrect input")
        if len(bitarray(''.join([bin(int('1' + hex(c)[2:], 16))[3:]for c in key_word.encode('utf-8')])).to01()) > 64:
            raise ValueError("Incorrect input")
    except ValueError:
        raise ValueError("Incorrect input")