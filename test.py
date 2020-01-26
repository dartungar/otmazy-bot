import pandas as pd
import pymorphy2
import random
import template
from construct import constructor
from helpers import create_text_from_list, needs_capitalizing
#from words import get_podlezh, get_skaz, get_noun_dop, get_noun_obst, get_predlog, get_must


def test_constructor(words, morph, is_nonsense=False, subject_is_myself=True, min_seriousness=None, max_seriousness=None, context=None, subj_sex=None, tense=None):
    if not tense:
        tense = random.choice(['past', 'futr'])     

    word_list = constructor(words=words, 
                        morph=morph, 
                        tense=tense, 
                        is_nonsense=is_nonsense,
                        subject_is_myself=random.randint(0, 1),
                        subj_datv=random.randint(0, 1),
                        has_predicate_spice=random.randint(0, 1),
                        to_be=random.randint(0, 1),
                        has_greeting=random.randint(0, 1),
                        has_beginning=random.randint(0, 1), 
                        has_ending=random.randint(0, 1),
                        min_seriousness=min_seriousness,
                        max_seriousness=max_seriousness,
                        context=context,
                        subj_sex=subj_sex
                        )


    text = create_text_from_list(morph, word_list)

    return text


if __name__ == '__main__':

    df = pd.read_excel('otgovorki.xlsx', index_col=0, sheet_name=None)
    morph = pymorphy2.MorphAnalyzer()

    for i in range(10):
        excuse_context = random.choice(['family', 'personal', 'health', 'leisure', 'work', 'study', 'official'])
        text = test_constructor(words=df, morph=morph, subj_sex='female', tense='futr', context=excuse_context)
        print(f'{excuse_context}: {text}')