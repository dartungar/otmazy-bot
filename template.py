# "я повезу жену в гипермаркет"
# "я повезу документы к нотариусу"
# "я поеду в гипермаркет"
# "я планирую поехать в гипермарке"
# "я поеду на работу"
# "я буду на работе"
# "я буду строить дом" "я собираюсь строить дом" 
import pymorphy2

from words import get_podlezh, get_skaz, get_noun_dop, get_noun_obst, get_predlog, get_must
import words_new

# http://www.mylanguage.ru/materials/130/3181


# TODO: переделать в класс
def template_1(words, morph):
    # подлежащее + сказуемое в буд. вр. + дополнение + предлог + обстоятельство
    beginning = words_new.Beginning(words=words)
    podlezh = words_new.Subject()
    skaz = words_new.Predicate(words=words, morph=morph, subject=podlezh, has_object=1)
    dopolnenie = words_new.Object(words, morph, predicate=skaz)
    obstoyatelstvo = words_new.Adverbial(words, morph, predicate=skaz, object=dopolnenie)
    
    text = f'{beginning.word} {podlezh.word} {skaz.word} {dopolnenie.word} {obstoyatelstvo.word}'
    return text


class Template:
    def __init__(self):
        
        self.text = ''


class Template_1(Template):
    pass
    