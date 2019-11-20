# "глупые" классы - принимают готовые параметры для подбора слова
import random

def declensify(morph, word_parsed, subj, tense='pres'):
    word = word_parsed
    if tense == 'pres' and 'anim' in subj.tag:
        word = word_parsed.inflect({'3per'})
    else:
        for grm in ['1per', '2per', '3per', 'sing', 'plur', 'masc', 'femn']:
            if grm in subj.tag:
                word_modified = word_parsed.inflect({grm})
                if word_modified:
                    word = word_modified
                else:
                    continue
                    #raise Exception(f'Error: Could not inflect on word "{word_parsed.word}" !')
    return word


# существительное
class Subject():
    def __init__(self, words, morph, subject_is_myself=True):
        # TODO: другие существительные (тёща, жена, итд) из таблицы + зависимость от времени (в дательном падеже прошлое время - нельзя?..)
        # + зависимость от контекста
        # TODO: если субъект не ты, то добавлять что-то типа "надо помочь", "не могу отказаться", "придется помочь" и т.д.
        # возможно это уже совсем другой шаблон

        subjects = words['subj'].fillna(value=0)

        self.is_myself = subject_is_myself
        self.info = subjects[subjects.is_myself==subject_is_myself].sample()
        self.word = self.info.iloc[0, 0]
        self.parsed = morph.parse(self.word)[0]


        

# TODO: реворкнуть в выбор из БД PredicateSpice?
# TODO: учитывать время
class PredicateSpice():
    def __init__(self, words, morph, tense='pres', subj=None, to_be=False):

        subj = morph.parse(subj.word)[0]

        if to_be:
            tobe = morph.parse('быть')[0]
            tobe = tobe.inflect({tense})

        # мне нужно, тёща придется
        if 'datv' in subj.tag:
            if to_be:
                self.word = f"{tobe} {random.choice(['нужно', 'надо', 'необходимо'])}"
            if not to_be:
                self.word = random.choice(['нужно', 'надо', 'необходимо', 'придется', 'давно пора', 'позарез надо', 'припекло'])
            self.parsed = morph.parse(self.word)[0]
        # я собираюсь, тёща хочет
        elif 'nomn' in subj.tag:
            n = morph.parse(random.choice(['собираться', 'планировать', 'хотеть', 'обещать']))[0]
            # TODO: избавиться от необходимости передавать подлежащее
            if tense=='pres' and 'anim' in subj.tag:
                n = n.inflect({'3per'})
            else:
                n = declensify(morph, n, subj)
            n = n.inflect({tense})
            self.word = n.word
            self.parsed = n 
        else:
            raise Exception('Invalid Case for Predicate Spice!')
        




class Predicate():
    def __init__(self, words, morph, tense='pres', noun_type=None, case=None):
        if noun_type:
            # тип
            verbs = words['verb'].fillna(value=0)
                
            self.info = verbs[verbs.noun_type == noun_type].sample()
            self.parsed = morph.parse(self.info.iloc[0, 0])[0]
            # спайс
            self.word = self.parsed.normal_form
            # TODO: более изящное решение через БД
            self.case_obj = self.info.iloc[0, 3]

        else:
            self.info = None
            self.word = ''

        # принимает падеж? TODO: разобраться, надо ли оно мне
        pass


# класс-родитель для всех существительных
class Noun():
    def __init__(self, words, morph, noun_type=None, case=None):
        if noun_type:
            nouns = words['noun'].fillna(value='')
            self.info = nouns[nouns.type==noun_type].sample()
            n = morph.parse(self.info.iloc[0, 0])[0]
            #print(f'type: {noun_type}, case: {case}')
            self.word = n.inflect({case}).word
        else:
            self.info = None
            self.word = ''



# склоняем по умолчанию или с obj_case от predicate
class Object(Noun):
    pass
        
        


# TODO SHIT GETS REAL
# or not. можно сделать тупую функцию, а всю логику добавить в конструктор
class Adverbial(Noun):
    pass

        


class Predlog():
    def __init__(self, words, morph, predlog_type=None, case=None):
        if predlog_type:
            predlogs = words['predlog'].fillna(value='')
            self.info = predlogs[(predlogs.noun_type==predlog_type) & (predlogs.noun_case==case)].sample()
            self.word = self.info.iloc[0, 0]
        else:
            self.info = None
            self.word = ''        
        


class Beginning():
    def __init__(self, words, morph):
        beginnings = words['beginning']
        self.info = beginnings.sample()
        self.word = self.info.iloc[0, 0]
        if self.info.iloc[0, 1]:
            self.word += ','
        

# TODO
class Ending():
    def __init__(self, words, morph):
        endings = words['ending']
        self.info = endings.sample()
        self.word = self.info.iloc[0, 0]

        #if not subject.is_myself:
        #     pass
        