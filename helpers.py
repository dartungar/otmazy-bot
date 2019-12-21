# функции-помощники для логики конструктора
# выбор типов, падежей итд
import random


# TODO: выделить в отдельные функции genderify, timify, personify, multify
def declensify(morph, word_parsed, tags=None, tense='pres', case=None, context=None):
    word = word_parsed
    # SOME THINGS JUST CANT BE DONE RIGHT
    if word.word == 'море' or word.word == 'мор':
        word = morph.parse('море')[5]
        #print(f'exception море! {word}')
    if word.word == 'волга':
        word = morph.parse('волга')[1]

    # словосочетания пока не парсим от слова совсем
    if len(word.word.split()) > 1:
        raise Exception('can not declensify more than 1 word at once!')

    if tense == 'pres' and 'anim' in tags:
        word = word.inflect({'3per'})
        
        if not word:
            raise Exception(f'could not inflect on word {word.word}')
    else:
        for grm in tags:
            word_modified = word.inflect({grm})
            if word_modified:
                word = word_modified
            else:
                print(f'could not declensify word {word.word} with grammeme {grm}')
                pass #TODO: логировать в info импотенцию склонятора
        if tense == 'futr' and 'NOUN' in tags and ('3per' and '1per') not in tags:
            #print('ding')
            word = word.inflect({'3per'})

    return word



# TODO: склонение целого словосочетания - для beginning & ending чтобы не вылавливать из середины "могу", "могла" итд
def declensify_text(morph, text, tags, tense='pres', context=None):
    text_declensified = ''
    words_parsed = []
    for word in text.split():
        words_parsed.append(morph.parse(word)[0])
    if len(words_parsed) == 2:
        
        text_declensified += declensify(morph, words_parsed[0], tags=tags, tense=tense, context=context).word + ' '
        # "Черное море"
        if 'ADJF' in words_parsed[0].tag and 'NOUN' in words_parsed[1].tag:
            text_declensified += declensify(morph, words_parsed[1], tags=tags, tense=tense, context=context).word
        if 'NOUN' in words_parsed[0].tag and 'NOUN' in words_parsed[1].tag:        
            text_declensified += words_parsed[1].word
    else:
        raise Exception('can not declensify_text more than 2 words at once!')
    
    return text_declensified


def create_text_from_list(morph, word_list):
    text = ''

    for word in word_list:
        if needs_capitalizing(morph, word):
            word = word.capitalize()
        text += word
        text += ' '

    text = text.replace(' . ', '. ')
    text = text.replace('  ', ' ')
    return text


# капитализируем имена собственные
def needs_capitalizing(morph, word):
    if len(word.split()) > 1:
        word = word.split()[0]

    word_parsed = morph.parse(word)[0]
    for grm in ['Name', 'Geox']:
        if grm in word_parsed.tag:
            return True

    return False


# правила для подбора существительных и предлогов на основе сказуемого
def get_rules(words, predicate):
    rules = words['rules']
    rules = rules[rules.verb_type==predicate.type].sample()
    return rules
        

