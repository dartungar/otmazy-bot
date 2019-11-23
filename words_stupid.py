# "глупые" классы - принимают готовые параметры для подбора слова
import random
from helpers import declensify


# существительное
class Subject():
    def __init__(self, words, morph, subject_is_myself=True, context=None):
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
    def __init__(self, words, morph, tense='pres', subj=None, to_be=False, context=None):

        subj = morph.parse(subj.word)[0]

        if to_be:
            tobe = morph.parse('быть')[0]
            tobe = tobe.inflect({tense})

        # мне нужно, тёща придется
        if 'datv' in subj.tag:
            if to_be:
                self.word = f"{random.choice(['нужно', 'надо', 'необходимо'])} {tobe}"
            if not to_be:
                self.word = random.choice(['нужно', 'надо', 'необходимо', 'придется', 'давно пора', 'позарез надо', 'припекло'])
            self.parsed = morph.parse(self.word)[0]
        # я собираюсь, тёща хочет
        elif 'nomn' in subj.tag:
            n = morph.parse(random.choice(['собираться', 'планировать', 'хотеть', 'обещать', 'пообещать', 'обязаться', 'клясться']))[0]
            # TODO: избавиться от необходимости передавать подлежащее
            
            n = declensify(morph, n, subj, tense=tense)
            #if n:
            #print(n)
            #print(f"n {n.word}")            
            self.word = n.word
            self.parsed = n 
        else:
            raise Exception('Invalid Case for Predicate Spice!')
        




class Predicate():
    def __init__(self, words, morph, tense='pres', noun_type=None, case=None, aspc='impf', context=None):
        if noun_type:
            # тип
            verbs = words['verb'].fillna(value=0)
                
            self.info = verbs[(verbs.noun_type==noun_type) & (verbs.aspc==aspc)].sample()
            self.parsed = morph.parse(self.info.iloc[0, 0])[0]
            # спайс
            self.word = self.parsed.normal_form
            # TODO: более изящное решение через БД
            self.case_obj = self.info.iloc[0, 3]
            self.aspc = aspc

        else:
            self.info = None
            self.word = ''

        # принимает падеж? TODO: разобраться, надо ли оно мне
        pass


# класс-родитель для всех существительных
class Noun():
    def __init__(self, words, morph, noun_type=None, case=None, context=None):
        if noun_type:
            nouns = words['noun'].fillna(value='')
            self.info = nouns[nouns.type==noun_type].sample()
            n = morph.parse(self.info.iloc[0, 0])[0]
            #print(f'type: {noun_type}, case: {case}')
            n_case = n.inflect({case})
            if n_case:
                self.word = n_case.word
            else:
                raise Exception(f'Could not inflect case {case} on word {n.word}')
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
    def __init__(self, words, morph, predlog_type=None, case=None, context=None):
        if predlog_type:
            predlogs = words['predlog'].fillna(value='')
            self.info = predlogs[(predlogs.noun_type==predlog_type) & (predlogs.noun_case==case)].sample()
            self.word = self.info.iloc[0, 0]
        else:
            self.info = None
            self.word = ''        
        


class Beginning():
    def __init__(self, words, morph, tense='pres', context=None):
        beginnings = words['beginning']
        self.info = beginnings.sample()
        self.word = self.info.iloc[0, 0]
        if self.info.iloc[0, 1]:
            self.word += ','
        

# TODO : ending spice, склоняемый по времени +  помогать
class Ending():
    def __init__(self, words, morph, tense='pres', context=None):
        endings = words['ending']
        self.info = endings[endings.tense==tense].sample()
        self.word = self.info.iloc[0, 0]
        # + помогать

        # TODO: Реализовать subject is myself
        #if not subject.is_myself:
        #     pass
        