# "я повезу жену в гипермаркет"
# "я повезу документы к нотариусу"
# "я поеду в гипермаркет"
# "я планирую поехать в гипермарке"
# "я поеду на работу"
# "я буду на работе"
# "я буду строить дом" "я собираюсь строить дом" 
# "я поеду с женой в гипермаркет"
import pymorphy2

from words import get_podlezh, get_skaz, get_noun_dop, get_noun_obst, get_predlog, get_must
import words_new

# http://www.mylanguage.ru/materials/130/3181


class Template:
    def __init__(self, words=None, morph=None):
        pass


# повезу жену в супермаркет
class Template_1():
    def __init__(self, words=None, morph=None):
        beginning = words_new.Beginning(words=words)
        podlezh = words_new.Subject(words=words, subject_is_myself=1)
        skaz = words_new.Predicate(words=words, morph=morph, subject=podlezh, has_object=1)
        dopolnenie = words_new.Object(words, morph, predicate=skaz)
        dopoln_predl = words_new.Predlog(words=words, noun=dopolnenie)
        obstoyatelstvo = words_new.Adverbial(words, morph, predicate=skaz, object=dopolnenie)
        obst_predl = words_new.Predlog(words=words, noun=obstoyatelstvo)
        
        self.text = f'{beginning.word} {podlezh.word} {skaz.word} {dopoln_predl.word} {dopolnenie.word} {obst_predl.word} {obstoyatelstvo.word}'


# поеду в супермаркет
class Template_2():
    def __init__(self, words=None, morph=None):
        beginning = words_new.Beginning(words=words)
        podlezh = words_new.Subject(words=words, subject_is_myself=1)
        skaz = words_new.Predicate(words=words, morph=morph, subject=podlezh)
        obstoyatelstvo = words_new.Adverbial(words=words, morph=morph, predicate=skaz)
        obst_predl = words_new.Predlog(words=words, noun=obstoyatelstvo)


        self.text = f'{beginning.word} {podlezh.word} {skaz.word} {obst_predl.word} {obstoyatelstvo.word}'
    

# поработаю над 
class Template_3():
    def __init__(self, words=None, morph=None):
        beginning = words_new.Beginning(words=words)
        podlezh = words_new.Subject(words=words, subject_is_myself=1)
        skaz = words_new.Predicate(words=words, morph=morph, noun_type='project', subject=podlezh, has_object=1)
        dopolnenie = words_new.Object(words, morph, predicate=skaz)
        dop_predl = words_new.Predlog(words=words, noun=dopolnenie)

        self.text = f'{beginning.word} {podlezh.word} {skaz.word} {dop_predl.word} {dopolnenie.word}'


# "жена хотела ... "
class Template_4():
    def __init__(self, words=None, morph=None):
        beginning = words_new.Beginning(words=words)
        podlezh = words_new.Subject(words=words, subject_is_myself=0)
        skaz = words_new.Predicate(words=words, morph=morph, subject=podlezh, has_object=1)
        dopolnenie = words_new.Object(words, morph, predicate=skaz)
        dop_predl = words_new.Predlog(words=words, noun=dopolnenie)
        obstoyatelstvo = words_new.Adverbial(words, morph, predicate=skaz, object=dopolnenie)
        obst_predl = words_new.Predlog(words=words, noun=obstoyatelstvo)
        ending = words_new.Ending(words=words, subject=podlezh)
        
        self.text = f'{beginning.word} {podlezh.word} {skaz.word} {dop_predl.word} {dopolnenie.word} {obst_predl.word} {obstoyatelstvo.word}, {ending.word}'