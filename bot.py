import pandas as pd
import pymorphy2
import random
from template import template_1
from words import get_podlezh, get_skaz, get_noun_dop, get_noun_obst, get_predlog, get_must

morph = pymorphy2.MorphAnalyzer()

def get_form(word, morph, case):
    parsed = morph.parse(word)[0]
    morphed = parsed.inflect({case})[0]
    return morphed
   




if __name__ == '__main__':

    df = pd.read_excel('otmazy_words.xlsx', index_col=0, sheet_name=None)

    print(template_1(words=df, morph=morph))
    exit()





