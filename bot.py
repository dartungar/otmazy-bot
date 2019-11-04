import pandas as pd
import pymorphy2
import random
import template
from words import get_podlezh, get_skaz, get_noun_dop, get_noun_obst, get_predlog, get_must

morph = pymorphy2.MorphAnalyzer()

def get_form(word, morph, case):
    parsed = morph.parse(word)[0]
    morphed = parsed.inflect({case})[0]
    return morphed


def create_random_template():
    number = random.randint(1, 3)
    if number == 1:
        tmplt = template.Template_1(words=df, morph=morph)
    if number == 2:
        tmplt = template.Template_2(words=df, morph=morph)
    if number == 3:
        tmplt = template.Template_3(words=df, morph=morph)
    if number == 4:
        tmplt = template.Template_4(words=df, morph=morph)

    return (number, tmplt)


if __name__ == '__main__':

    df = pd.read_excel('otmazy_words.xlsx', index_col=0, sheet_name=None)

    for i in range(10):
        text = str(create_random_template()[0]) +' '+  create_random_template()[1].text

        print(text)

    exit()





