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
        self.person = '1per'
        if '1per' not in self.parsed.tag and '2per' not in self.parsed.tag: 
            self.person = '3per'
        self.plural = 'sing'
        for plur in ['sing', 'plur']:
            if plur in self.parsed.tag:
                self.plural = plur
 

# TODO: реворкнуть в выбор из БД PredicateSpice?
# TODO: учитывать время
class PredicateSpice():
    def __init__(self, words, morph, tense='pres', subj=None, to_be=False, context=None):

        #subj = morph.parse(subj.word)[0]
        tobe = morph.parse('быть')[0]


            #self.word = declensify(morph, tobe, subj, tense='futr').word
            #print(self.word)

        # мне нужно, мне нужно будет, тёще придется
        if 'datv' in subj.parsed.tag:
            if to_be:
                self.word = f"{random.choice(['нужно', 'надо', 'необходимо'])} {tobe.inflect({tense, '3per', subj.plural}).word}"
            else:
                self.word = random.choice(['нужно', 'надо', 'необходимо', 'придется', 'давно пора', 'позарез надо', 'припекло'])
                self.parsed = morph.parse(self.word)[0]

        # я буду, он будет
        elif to_be == True:
            self.word = tobe.inflect({tense, subj.person, subj.plural}).word

        # я собираюсь, тёща хочет
        elif 'nomn' in subj.parsed.tag:
            if to_be:
                self.word = tobe
            else:
                n = morph.parse(random.choice(['собираться', 'планировать', 'хотеть', 'обещать', 'пообещать', 'обязаться', 'поклясться']))[0]
                # TODO: избавиться от необходимости передавать подлежащее
                #print(n)
                n = declensify(morph, n, subj, tense='past')
                #n = n.inflect({'past', subj.person, subj.plural})
                #if n:
                #print(n)
                #print(f"n {n.word}")            
                self.word = n.word
                self.parsed = n 
        else:
            raise Exception('Invalid Case for Predicate Spice!')
        

# сказуемое
class Predicate():
    def __init__(self, words, morph, tense='pres', verb_type=None, has_object=True, noun_type=None, case=None, aspc='impf', context=None):
        
        verbs = words['verb'].fillna(value=0)

        # фильтр раз
        verbs = verbs[verbs.has_object==has_object]
        
        # можем прямо определить тип сказуемого
        if verb_type:
            self.info = verbs[(verbs.type==verb_type) & (verbs.aspc==aspc)].sample()
        # ...или прямо определить согласование с существительными
        elif noun_type:
            # тип
            self.info = verbs[(verbs.noun_type==noun_type) & (verbs.aspc==aspc)].sample()
        # ... или всё-таки выбрать по-честному ;)
        else:
            self.info = verbs[verbs.aspc==aspc].sample()
        

        # TODO: более изящное решение через БД
        self.case_object = self.info.case_object.iloc[0]
        self.aspc = aspc
        self.type = self.info.type.iloc[0]
        self.type_alt = self.info.type_alt.iloc[0]

        self.parsed = morph.parse(self.info.word.iloc[0])[0]
        self.word = self.parsed.word



# класс-родитель для всех существительных
class Noun():
    def __init__(self, words, morph, noun_type=None, case=None, context=None):
        if noun_type:
            self.type = noun_type
            nouns = words['noun'].fillna(value='')
            self.info = nouns[nouns.type==noun_type].sample()
            n = morph.parse(self.info.iloc[0, 0])[0]
            #print(f'type: {noun_type}, case: {case}')
            # ёбаный костыль FIXME
            if len(n.word.split()) < 2:
                n_case = n.inflect({case})
            else:
                n_case = n
            if n_case:
                self.word = n_case.word
            else:
                self.word = n.word
                # print('could not inflect case!')
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
        self.info = endings[(endings.tense==tense)|(endings.tense=='all')].sample()
        self.word = self.info.word.iloc[0]
        #print(self.word)
        # + помогать

        # TODO: Реализовать subject is myself
        #if not subject.is_myself:
        #     pass
        