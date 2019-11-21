# функции-помощники для логики конструктора
# выбор типов, падежей итд
import random

def get_predicate_noun_type(object_type=None):
    if object_type:
        noun_type = object_type
    else:
        # TODO: выбор из словаря или что-то такое же изящное
        noun_type = 'place'
    return noun_type



def get_adverbial_type(object_type, predicate_noun_type):
    # TODO: переделать из той залупы в таблицу соответствий object_type <-> adv_type
    # тогда и функция не нужна будет
    if object_type:
        if object_type == 'person':
            return random.choice(['place', 'place_open', 'event', 'person'])
        if object_type == 'thing':
            return random.choice(['place', 'place_open', 'event', 'person'])
        if object_type == 'project':
            return random.choice(['place', 'place_open', 'event', 'person'])
        else:
            raise Exception(f'Could not find Adverbial type for Object type {object_type}')
    else:
        return predicate_noun_type


def get_adverbial_case(object_type, adverbial_type):
    # TODO: переделать в таблицу соответствий!
    if adverbial_type == 'person':
        if object_type == 'person':
            return 'datv'
        if object_type == 'thing':
            return 'gent'
        if object_type == 'project':
            return 'gent'
            #return random.choice(['gent', 'ablt'])               
    else:
        # TODO: более продвинутое присвоение падежей
        cases = {'thing': 'ablt', 'event': 'accs', 'place': 'accs', 'place_open': 'accs', 'project': 'ablt'}
        return cases[adverbial_type]        
    raise Exception(f'Could not find Adverbial case for obj {object_type} adv {adverbial_type}')



