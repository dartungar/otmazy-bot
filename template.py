# "я повезу жену в гипермаркет"
# "я повезу документы к нотариусу"
# "я поеду в гипермаркет"
# "я планирую поехать в гипермарке"
# "я поеду на работу"
# "я буду на работе"
# "я буду строить дом" "я собираюсь строить дом" 
import pymorphy2

from words import get_podlezh, get_skaz, get_noun_dop, get_noun_obst, get_predlog, get_must

#http://www.mylanguage.ru/materials/130/3181

#TODO: переделать в класс
def template_1():
    # подлежащее + сказуемое в буд. вр. + дополнение + предлог + обстоятельство
    podlezh = get_podlezh()
    skaz = get_skaz(podlezh, has_object=1, to_be=0)
    skaz_word = skaz[0]
    skaz_info = skaz[1]
    dopolnenie = get_noun_dop(skaz_info=skaz_info)
    obstoyatelstvo = get_noun_obst(has_object=1)
    

    text = f'{podlezh} {skaz_word} {dopolnenie} {obstoyatelstvo}'
    return text


class Template:
    def __init__(self):
        
        self.text = ''


class Template_1(Template):
    pass
    