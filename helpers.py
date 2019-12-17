# функции-помощники для логики конструктора
# выбор типов, падежей итд
import random


# TODO: выделить в отдельные функции genderify, timify, personify, multify
def declensify(morph, word_parsed, tags=None, tense='pres', case=None, context=None):
    word = word_parsed
    # словосочетания пока не парсим от слова совсем
    if len(word.word.split()) > 1:
        raise Exception('can not declensify more than 1 word at once!')

    # if subj:
    #     tags = str(subj.parsed.tag).replace(' ', ',')
    #     tags = tags.split(',')
        
    #     # чтобы не менять часть речи
    #     forbidden_grammemes = ['anim', 'nomn', 'NOUN', 'ADJF', 'ADJS', 'COMP', 'VERB', 'INFN', 'PRTF', 'PRTS', 'GRND', 'NUMR', 'ADVB', 'NPRO', 'PRED', 'PREP', 'CONJ', 'PRCL', 'INTJ']
    #     for tag in tags:
    #         if tag in forbidden_grammemes:
    #             tags.remove(tag)

    # if 'VERB' in word_parsed.tag and 'nomn' in tags:
    #     tags.remove('nomn')

    if tense == 'pres' and 'anim' in tags:
        word = word_parsed.inflect({'3per'})
        
        if not word:
            raise Exception(f'could not inflect on word {word_parsed.word}')
    else:
        for grm in tags:
            word_modified = word_parsed.inflect({grm})
            if word_modified:
                word = word_modified
            else:
                print(f'could not declensify word {word_parsed.word} with grammeme {grm}')
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
        # "Черное море"
        text_declensified += declensify(morph, words_parsed[0], tags=tags, tense=tense, context=context).word + ' '
        if 'ADJF' in words_parsed[0].tag and 'NOUN' in words_parsed[1].tag:
            text_declensified += declensify(morph, words_parsed[1], tags=tags, tense=tense, context=context).word
        if 'NOUN' in words_parsed[0].tag and 'NOUN' in words_parsed[1].tag:        
            text_declensified += words_parsed[1].word
    else:
        raise Exception('can not declensify_text more than 2 words at once!')
    
    return text_declensified


# финальный марафет для сгенерированного текста
def prettify_text(morph, text):
    text = text.split('.')
    prettified_text = ''
    
    for sentence in text:
        sentence = sentence.strip()
        sentence_new = []
        
        if sentence:
            sentence_split = sentence.split(' ')
            
            for word in sentence_split:
                word = word.strip().replace('.', '')
                if word:
                    if needs_capitalizing(morph, word):
                        word = word.capitalize()
                    sentence_new.append(word)
            
            sentence_new[0] = sentence_new[0].capitalize()
            sentence = ' '.join(sentence_new)
            prettified_text += sentence
            prettified_text += '. '
    
    return prettified_text


# капитализируем имена собственные
def needs_capitalizing(morph, word):
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
        

