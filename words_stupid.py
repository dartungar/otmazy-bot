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
        self.gender = 'masc'
        for gender in ['masc', 'femn', 'neut']:
            if gender in self.parsed.tag:
                self.gender = gender

 

# TODO: реворкнуть в выбор из БД PredicateSpice?
# TODO: учитывать время
class PredicateSpice():
    def __init__(self, words, morph, tense='pres', subj=None, to_be=False, context=None):

        #subj = morph.parse(subj.word)[0]
        tobe = morph.parse('быть')[0]

        self.word = ''


            #self.word = declensify(morph, tobe, subj, tense='futr').word
            #print(self.word)

        # мне нужно, мне нужно будет, тёще придется
        if 'datv' in subj.parsed.tag:
            if to_be:
                if tense == 'futr':
                    self.word = f"{random.choice(['нужно', 'надо', 'необходимо'])} {tobe.inflect({tense, '3per', subj.plural}).word}"
                elif tense == 'past':
                    self.word = f"{random.choice(['нужно', 'надо', 'необходимо'])} {tobe.inflect({tense, 'neut'}).word}"
            else:
                if tense == 'futr':
                    self.word = random.choice(['нужно', 'надо', 'необходимо', 'придется', 'давно пора', 'позарез надо', 'припекло'])
                elif tense == 'past':
                    self.word = random.choice(['нужно было', 'надо было', 'необходимо было', 'пришлось', 'давно пора было', 'позарез надо было', 'припекло'])
                self.parsed = morph.parse(self.word)[0]

        # я буду, он будет
        elif to_be == True and tense == 'futr':
            self.word = tobe.inflect({tense, subj.person, subj.plural}).word
        

        # я собираюсь, тёща хочет
        elif 'nomn' in subj.parsed.tag:
            if to_be:
                #self.word = tobe.word
                pass
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
        #verbs = verbs[verbs.has_object==has_object]  #по факту у глаголов типа Travel никогда не объекта, если не считать "путешествие с тёщей на Кавказ" объектом тёщу
        
        if has_object:
            verbs = verbs[verbs.type!='travel'] 
        else:
            verbs = verbs[verbs.type=='travel']

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
        self.case = case
        self.type = noun_type
        if noun_type:
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
            self.parsed = morph.parse(self.word)[0]

        else:
            self.info = None
            self.word = ''
            self.parsed = ''



# склоняем по умолчанию или с obj_case от predicate
class Object(Noun):
    def __init__(self, words, morph, noun_type=None, case=None, context=None):
        Noun.__init__(self, words, morph, noun_type=noun_type, case=case, context=context)
        self.member = 'object'
    
        
        


# TODO SHIT GETS REAL
# or not. можно сделать тупую функцию, а всю логику добавить в конструктор
class Adverbial(Noun):
    def __init__(self, words, morph, noun_type=None, case=None, context=None):
        Noun.__init__(self, words, morph, noun_type=noun_type, case=case, context=context)
        self.member = 'adverbial'
        


class Predlog():
    def __init__(self, words, morph, word=None, context=None):
        if word.case == 'accs' and word.type == 'event' and word.member == 'object':
            self.word = ''
        # elif word.case == 'accs':
        #     if word.type in ['event', 'project']:
        #         if word.member == 'adverbial':
        #             self.word = 'для'
        elif word.type:
            predlogs = words['predlog'].fillna(value='')
            self.info = predlogs[(predlogs.noun_type==word.type) & (predlogs.noun_case==word.case)].sample()
            self.word = self.info.iloc[0, 0]
        else:
            self.info = None
            self.word = ''        
        


class Beginning():
    def __init__(self, words, morph, tense='pres', context=None):
        beginnings = words['beginning']
        self.info = beginnings[(beginnings.tense==tense)|(beginnings.tense=='all')].sample()
        self.word = self.info.iloc[0, 0]
        if self.info.iloc[0, 1]:
            self.word += ','


class Greeting():
    def __init__(self, words, morph, tense='pres', type='beginning', context=None):
        self.word = random.choice([
            'Привет',
            'Приветствую',
            'Салам',
            'Хай',
            'Здравствуй',
            'Здравствуйте',
            '',
            '',
        ])


# разные предложения, добавляемые до или после основного, ради правдоподобности
class EndingSentence():
    def __init__(self, words, morph, tense='pres', type='beginning', custom_word_parsed=None, context=None):
        sentences = words['sentences']
        if custom_word_parsed:
            self.info = sentences[((sentences.tense==tense)|(sentences.tense=='all'))&(sentences.type==type)&(sentences.is_custom==True)].sample()
            self.word = self.info.sentence.iloc[0]
            case = self.info.word_case.iloc[0]
            #print(f'custon_word_parsed: {custom_word_parsed}, case {case}')
            word = custom_word_parsed.inflect({case}).word
            self.word = self.word.replace('<word>', word)
        else:
            self.info = sentences[((sentences.tense==tense)|(sentences.tense=='all'))&(sentences.type==type)&(sentences.is_custom==False)].sample()
            self.word = self.info.sentence.iloc[0]
        self.word = self.word.strip().capitalize()
        #print(self.word)
    





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
        