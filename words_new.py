'''
Объекты, представляющие части речи
'''


# существительное
class Subject:
    def __init__(self, words):
        self.word = random.choice(['я', 'мне'])
        pass
    pass


# сказуемое
class Predicate:
    def __init__(self, words, morph, has_object=0, to_be=0):
        self.has_object = has_object
        pass
    pass


# дополнение
class Object:
    def __init__(self, words, morph, predicate=None):
        pass
    pass


# обстоятельство
class Adverbial:
    def __init__(self, words, morph, predicate=None):
        pass
    pass


# определение
class Attribute:
    def __init__(self, words, morph):
        pass
    pass