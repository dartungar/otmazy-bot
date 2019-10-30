import pandas as pd
import pymorphy2
import random

morph = pymorphy2.MorphAnalyzer()

def get_form(word, morph, case):
    parsed = morph.parse(word)[0]
    morphed = parsed.inflect({case})[0]
    return morphed
   




if __name__ == '__main__':

    df = pd.read_excel('otmazy_words.xlsx', sheet_name=None, index_col=0)

    text = ''

    spice = df['spice'].sample().iloc[0, 0]
    text += str(spice) + ', '
    #print(text)

    subj_info = df['subj'].sample()
    subj = subj_info.iloc[0, 0]
    text += str(subj) + ' '
    subj_beginning = subj_info.iloc[0, 2]
    text += str(subj_beginning) + ' '



    glagol_info = df['glagol'].sample()

    glagol = glagol_info.iloc[0, 0]
    #print(glagol_info)
    text += str(glagol) + ' '

    #TODO: всё что можно распихать по функциям

    #если есть ивент И объект, рандомно решаем что выбрать
    if glagol_info.iloc[0, 1] and glagol_info.iloc[0, 3]:
        choice = random.randint(0, 1)
        if choice:
            objects = df['object']
            #if not glagol_info.iloc[0, 4]:
            #objects = objects[objects['animate']==1]
            if not glagol_info.iloc[0, 5]:
                objects = objects[objects['animate']==0]
                objct = objects.sample().iloc[0, 0]
                sklonenie_obj = str(glagol_info.iloc[0, 7])
                objct = get_form(str(objct), morph, sklonenie_obj) 
                text += objct + ' '
        if not choice:
            event_info = df['event'].sample()
            event_predlog = event_info.iloc[0, 2]
            text += str(event_predlog) + ' '
            dest = event_info.iloc[0, 0]
            sklonenie_event = str(event_info.iloc[0, 3])
            text += get_form(str(dest), morph, sklonenie_event) + ' '
        print(text)
        exit()

    # если есть объект
    if glagol_info.iloc[0, 1]:
        objects = df['object']
        #if not glagol_info.iloc[0, 4]:
            #objects = objects[objects['animate']==1]
        if not glagol_info.iloc[0, 5]:
            objects = objects[objects['animate']==0]
        objct = objects.sample().iloc[0, 0]
        sklonenie_obj = str(glagol_info.iloc[0, 7])
        objct = get_form(str(objct), morph, sklonenie_obj) 
        text += objct + ' '

    # если есть пункт назначения
    if glagol_info.iloc[0, 2]:
        dest_info = df['destination'].sample()
        dest_predlog = dest_info.iloc[0, 2]
        text += str(dest_predlog) + ' '
        dest = dest_info.iloc[0, 0]
        sklonenie_dest = str(dest_info.iloc[0, 3])
        text += get_form(str(dest), morph, sklonenie_dest) + ' '

    # если есть ивент
    if glagol_info.iloc[0, 3]:
        event_info = df['event'].sample()
        event_predlog = event_info.iloc[0, 2]
        text += str(event_predlog) + ' '
        dest = event_info.iloc[0, 0]
        sklonenie_event = str(event_info.iloc[0, 3])
        text += get_form(str(dest), morph, sklonenie_event) + ' '

    print(text)
    exit()





