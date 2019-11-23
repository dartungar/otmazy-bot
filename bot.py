import pandas as pd
import pymorphy2
import random
import template
from construct import constructor
#from words import get_podlezh, get_skaz, get_noun_dop, get_noun_obst, get_predlog, get_must



def get_form(word, morph, case):
    parsed = morph.parse(word)[0]
    morphed = parsed.inflect({case})[0]
    return morphed


def create_random_template():
    number = random.randint(1, 4)
    if number == 1:
        tmplt = template.Template_1(words=df, morph=morph)
    if number == 2:
        tmplt = template.Template_2(words=df, morph=morph)
    if number == 3:
        tmplt = template.Template_3(words=df, morph=morph)
    if number == 4:
        tmplt = template.Template_4(words=df, morph=morph)

    return (number, tmplt)


def test_constructor(words, morph):
    tense = 'futr' # TODO: разобраться почему не работает, cейчас везде прошлое о_О
    subjim = random.randint(0, 1)
    obj_type = random.choice(['person', 'project', 'thing'])
    has_pred_spice = random.randint(0, 1)
    beginning = random.randint(0, 1)
    if obj_type == 'project':
        adv_type = random.choice(['person', 'event'])
    else:
        adv_type = None
    ending = False if subjim else True

    return constructor(words=words, 
                        morph=morph, 
                        tense=tense, 
                        subject_is_myself=subjim, 
                        has_predicate_spice=has_pred_spice,
                        object_type=obj_type,
                        adv_type=adv_type, 
                        has_beginning=beginning, 
                        has_ending=ending)


if __name__ == '__main__':

    df = pd.read_excel('otmazy_words.xlsx', index_col=0, sheet_name=None)
    morph = pymorphy2.MorphAnalyzer()

    for i in range(10):
        #temp = create_random_template()
        #text = f'{str(temp[0])} {temp[1].text}'
        #str(create_random_template()[0]) +' '+  create_random_template()[1].text
        text = test_constructor(words=df, morph=morph)
        print(text)







