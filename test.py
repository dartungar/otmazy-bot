import pandas as pd
import pymorphy2
import random
import template
from construct import constructor
from helpers import create_text_from_list, needs_capitalizing
#from words import get_podlezh, get_skaz, get_noun_dop, get_noun_obst, get_predlog, get_must


def test_constructor(words, morph, seriousness=None, min_seriousness=None, max_seriousness=None, context=None):
    tense = random.choice(['past', 'futr']) 
    subjim = random.randint(0, 1)

    word_list = constructor(words=words, 
                        morph=morph, 
                        tense=tense, 
                        subject_is_myself=subjim, 
                        subj_datv=random.randint(0, 1),
                        has_predicate_spice=random.randint(0, 1),
                        to_be=random.randint(0, 1),
                        #has_object=random.randint(0, 1),
                        has_greeting=random.randint(0, 1),
                        has_beginning=random.randint(0, 1), 
                        has_ending=random.randint(0, 1),
                        min_seriousness=min_seriousness,
                        max_seriousness=max_seriousness,
                        context=context
                        )


    # костыль поганый. FIXME
    text = create_text_from_list(morph, word_list)

    return text


if __name__ == '__main__':

    df = pd.read_excel('otgovorki.xlsx', index_col=0, sheet_name=None)
    morph = pymorphy2.MorphAnalyzer()

    for i in range(10):
        #temp = create_random_template()
        #text = f'{str(temp[0])} {temp[1].text}'
        #str(create_random_template()[0]) +' '+  create_random_template()[1].text
        text = test_constructor(words=df, morph=morph, context='family')
        print(text)