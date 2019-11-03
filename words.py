import pandas as pd
import pymorphy2
import random

morph = pymorphy2.MorphAnalyzer()
df = pd.read_excel('otmazy_words.xlsx', index_col=0, sheet_name=None)

# функции для быстрой склейки шаблона
# возможно шаблон - это dict с правилами или просто list типа [word_type, word_type, word_type]
# а может быть и функция высокого уровня, вызывающая подбор речи с заданными мной параметрами
# потом параметры можно хранить в настройках

# подлежащее - я...а может и кто-то другой, но это уже сложнее

# TODO: сделать декораторы для передачи morph'а и массива слов из Pandas


def get_podlezh():
    # ;)
    # я и "мне", "жене" - совсем разные кейсы. дательный падеж подлежащего надо учитывать
    return random.choice(['я', 'мне'])


# всякие "нужно", "придется" и т.д.
# TODO
def get_must(word_parsed):
    p = word_parsed
    if 'datv' in p.tag:
        return random.choice(['нужно', 'придется', 'давно пора']) + ' '
    return ''


# сказуемое. в отмазках глаголы бывают нескольких основных типов 
def get_skaz(podlezh, has_object=0, type=None, to_be=0):
    # глаголы есть совершенные и несовершенные! помни это! 
    # сказуемое зависит от подлежащего: лицо, ???
    # типы глаголов: движение, занятие, созидание\креатив\мышление, решение вопроса (решить, разобраться, закончить итд)
    # нужны более подробные глаголы. "отвезти" и "нужно отвезти" - разные. 
    # TODO: склонять по времени
    # TODO: добавить работу с "буду ..."
    
    # парсим подлежащее
    p = morph.parse(podlezh)[0]

    # TODO: выбираем сказуемое
    df_verb = df['verb']
    if has_object == 0:
        skaz_info = df_verb[df_verb.noun.isin(['place', 'project'])].sample()
    else:
        skaz_info = df_verb[df_verb.noun.isin(['thing', 'person'])].sample()
    #skaz_info = df['verb'].sample()
    skaz = skaz_info.iloc[0, 0]
    # TODO: нормализуем и парсим сказуемое
    s = morph.parse(skaz)[0]

    # склоняем по всяким признакам! v1, тупо перебираем нужные граммемы
    for grm in ['1per', '2per', '3per', 'sing', 'plur']:
        if grm in p.tag:
            s = s.inflect({grm})

    # для "мне", "ей" и т.д. инфинитив ("мне нужно")
    if 'datv' in p.tag:
        s = s.normal_form
    else:
        s = s.word

    must = get_must(p)
    


    return (f'{must}{s}', skaz_info)


# FIXME: откуда-то nan берется
def get_predlog(noun_data):
    if pd.isna(noun_data.iloc[0, 4]) is False:
        return noun_data.iloc[0, 4]
    
    predlogs = {'person': 'к', 'thing': 'за', 'place': 'в', 'place_open': 'на', 'event': 'на', 'project': 'над'}
    noun_type = noun_data.iloc[0, 3]
    return predlogs[noun_type]
    # выбор предлога зависит от главного слова
    # судя по всему, без привязки не обойтись :\ 
    # что делать с разными предлогами "в работе \ на работе" - хз


# субъект может встречаться несколько раз - как дополнение и как обстоятельство!
# в некоторых случаях нужен предлог. это зависит от слова и контекста
# например дополнению, как правило не нужен предлог, а обстоятельству нужен

# дополнение: кого или что. объект, короче
def get_noun_dop(skaz_info=None):
    # выбор дополнения зависит от сказуемого
    # TODO: нужен кастомный признак для сказуемого - движение, и т.д.
    # например если сказуемое=движение то place в качестве noun-add точно отменяется
    # а вот в качестве noun-circ наоборот приветствуется!
    # 

    # TODO: реализовать передачу инфы о сказуемом!

    
    noun_type = skaz_info.iloc[0, 3]
        

    # подходят люди и вещи
    # TODO: реализовать это
    #df = df['noun']
    noun_data = df['noun'][df['noun'].type == noun_type].sample()
    noun = noun_data.iloc[0, 0]
    n = morph.parse(noun)[0]
    n = n.inflect({'accs'}).word
    return n




def get_noun_obst(has_object=0):
    # подходят люди, вещи, места и ивенты. TODO: предлоги типа "повезу тёщу ЗА женой"
    # TODO: в БД у существительных колонка с указанием падежа, если они в роле обстоятельства - "куда", "к кому"
    # НО! вроде можно сделать просто на основе одушевленности! если одуш то К КОМУ, если неодуш то КУДА
    if has_object:
        noun_data = df['noun'][df['noun'].type.isin(['place', 'event'])].sample()
    else:
        noun_data = df['noun'][df['noun'].type.isin(['place', 'event', 'project'])].sample()

    noun = noun_data.iloc[0, 0]
    n = morph.parse(noun)[0]


    # TODO: кейсы К тёще и ЗА тёщей!
    # К - только для person, ЗА - person и thing!

    if noun_data.iloc[0, 3] == 'person':
        n = n.inflect({'datv'})
    else:
        # TODO: добавить person в кейсе ЗА тёщей, но там надо логику в целом улучшать
        cases = {'thing': 'ablt', 'event': 'accs', 'place': 'accs', 'project': 'ablt'}
        n = n.inflect({cases[noun_data.iloc[0, 3]]})       
    
    predlog = get_predlog(noun_data)
    print(f'{predlog}')
    n = n.word
    n = f'{predlog} {n}'
    return n





    
