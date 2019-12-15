# функции-помощники для логики конструктора
# выбор типов, падежей итд
import random


# TODO: выделить в отдельные функции genderify, timify, personify, multify
def declensify(morph, word_parsed, subj, tense='pres', context=None):
    word = word_parsed
    # словосочетания пока не парсим от слова совсем
    if len(word.word.split()) > 1:
        return word
    
    if tense == 'pres' and 'anim' in subj.parsed.tag:
        word = word_parsed.inflect({'3per'})
        
        if not word:
            raise Exception(f'could not inflect on word {word_parsed.word}')
    else:
        for grm in [subj.person, subj.plural, tense, 'masc', 'femn']:
            if grm in subj.parsed.tag or grm==tense:
                #print(f'word before: {word.word}, tense {tense}')
                word_modified = word_parsed.inflect({grm})
                if word_modified:
                    word = word_modified
                    #print(tense)
                    #print(word.word)
                else:
                    print(f'could not declensify word {word_parsed.word}')
                    pass #TODO: логировать в info импотенцию склонятора
        if tense == 'futr' and ('3per' and '1per') not in subj.parsed.tag:
            #print('ding')
            word = word.inflect({'3per'})
    return word


def declensify_predicate(morph, word_parsed, subj, tense='pres', context=None):
    word = word_parsed
    if tense == 'pres' and 'anim' in subj.parsed.tag:
        word = word_parsed.inflect({'3per'})
        
        if not word:
            raise Exception(f'could not inflect on word {word_parsed.word}')
    else:
        for grm in [subj.person, subj.plural, tense, 'masc', 'femn']:
            if grm in subj.parsed.tag:
                word_modified = word_parsed.inflect({grm})
                if word_modified:
                    word = word_modified
                    print(word)
                else:
                    print(f'could not declensify word {word_parsed.word}')
                    pass #TODO: логировать в info импотенцию склонятора
                    #raise Exception(f'Error: Could not inflect on word "{word_parsed.word}" !')                    
    #print(f'declensified word {word}')            
    return word  


# TODO: склонение целого словосочетания - для beginning & ending чтобы не вылавливать из середины "могу", "могла" итд
def declensify_text(morph, text, subj, tense, context):
    text_declensified = ''
    for word in text.split():
        word = morph.parse(word)[0]
        text_declensified += declensify(morph, word, subj, tense=tense, context=context).word + ' '
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
        

