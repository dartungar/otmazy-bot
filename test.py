import pandas as pd
import pymorphy2
import random
import template
from construct import constructor
#from words import get_podlezh, get_skaz, get_noun_dop, get_noun_obst, get_predlog, get_must


def test_constructor(words, morph):
    tense = random.choice(['past', 'futr']) # TODO: разобраться почему не работает, cейчас везде прошлое о_О
    subjim = random.randint(0, 1)

    text = constructor(words=words, 
                        morph=morph, 
                        tense=tense, 
                        subject_is_myself=subjim, 
                        has_predicate_spice=random.randint(0, 1),
                        to_be=random.randint(0, 1),
                        has_object=random.randint(0, 1),
                        has_beginning=random.randint(0, 1), 
                        has_ending=1#random.randint(0, 1)
                        )

    text = text.replace('  ', ' ').strip().capitalize()

    # костыль поганый. FIXME
    text = text.split('.')
    prettified_text = ''
    for sentence in text:
        if sentence.strip():
            sentence = sentence.replace('.', '')
            sentence = sentence.replace('  ', ' ').strip().capitalize()
            prettified_text += sentence
            prettified_text += '. '

    return prettified_text


if __name__ == '__main__':

    df = pd.read_excel('otmazy_words.xlsx', index_col=0, sheet_name=None)
    morph = pymorphy2.MorphAnalyzer()

    for i in range(10):
        #temp = create_random_template()
        #text = f'{str(temp[0])} {temp[1].text}'
        #str(create_random_template()[0]) +' '+  create_random_template()[1].text
        text = test_constructor(words=df, morph=morph)
        print(text)







