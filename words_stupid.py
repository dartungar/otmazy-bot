# "глупые" классы - принимают готовые параметры для подбора слова
import random
from helpers import declensify, declensify_text, needs_capitalizing


# существительное
class Subject():
    def __init__(self, words, morph, subject_is_myself=True, datv=False, context=None, min_seriousness=None, max_seriousness=None):
        # TODO: другие существительные (тёща, жена, итд) из таблицы + зависимость от времени (в дательном падеже прошлое время - нельзя?..)
        # + зависимость от контекста
        # TODO: если субъект не ты, то добавлять что-то типа "надо помочь", "не могу отказаться", "придется помочь" и т.д.
        # возможно это уже совсем другой шаблон

        subjects = words['subj'].fillna(value=0)

        if min_seriousness:
            subjects = subjects[subjects.seriousness>=min_seriousness]
        if max_seriousness:
            subjects = subjects[subjects.seriousness<=max_seriousness]

        self.is_myself = subject_is_myself
        self.info = subjects[subjects.is_myself==subject_is_myself].sample()
        self.word = self.info.iloc[0, 0]
        self.parsed = morph.parse(self.word)[0]
        if datv:
            if len(self.word.split(' ')) == 1:
            #self.word = self.parsed.inflect({'datv'}).word
                self.word = declensify(morph, self.parsed, ['datv']).word
                self.parsed = morph.parse(self.word)[0]
            else:
                self.word = declensify_text(morph, self.word, ['datv'])
                #print(self.word)
                self.parsed = morph.parse(self.word.split(' ')[1])[0]
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
                pass
            else:
                n = morph.parse(random.choice(['собираться', 'планировать', 'хотеть', 'обещать', 'пообещать', 'обязаться', 'поклясться', 'решить', 'решиться', 'собраться', 'запланировать']))[0]
                # TODO: избавиться от необходимости передавать подлежащее
                n = declensify(morph, n, tags=[subj.person, subj.plural, subj.gender], tense='past')         
                self.word = n.word
                self.parsed = n 
        else:
            raise Exception('Invalid Case for Predicate Spice!')
        

# сказуемое
class Predicate():
    def __init__(self, words, morph, tense='pres', verb_type=None, noun_type=None, case=None, aspc='impf', context=None, min_seriousness=None, max_seriousness=None):
        
        verbs = words['verb'].fillna(value=0)

        # фильтр раз

        if min_seriousness:
            verbs = verbs[verbs.seriousness>=min_seriousness]
        if max_seriousness:
            verbs = verbs[verbs.seriousness<=max_seriousness]

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
        #self.case_object = self.info.case_object.iloc[0]
        self.aspc = aspc
        self.type = self.info.type.iloc[0]
        if self.type == 'volit':
            self.can_be_composite = True
        else:
            self.can_be_composite = False

        self.parsed = morph.parse(self.info.word.iloc[0])[0]
        self.word = self.parsed.word



class NounSpice():
    def __init__(self, words, morph, noun_parsed=None):
        if ('anim' in noun_parsed.tag and 'Name' not in noun_parsed.tag and 'Geox' not in noun_parsed.tag) or 'anim' not in noun_parsed.tag:
            self.word = random.choice(['мой', 'свой'])
            self.parsed = morph.parse(self.word)[0]
        else:
            self.word = ''


# класс-родитель для всех существительных
class Noun():
    def __init__(self, words, morph, noun_type, case=None, context=None, min_seriousness=None, max_seriousness=None):
        self.case = case
        self.type = noun_type
        nouns = words['noun'].fillna(value='')
        
        if min_seriousness:
            nouns = nouns[nouns.seriousness>=min_seriousness]
        if max_seriousness:
            nouns = nouns[nouns.seriousness<=max_seriousness]
        
        self.info = nouns[nouns.type==noun_type].sample()   

        n = morph.parse(self.info.iloc[0, 0])[0]
        #print(f'type: {noun_type}, case: {case}')
        self.word = n.word
        
        if len(self.word.split(' ')) == 1:
        #self.word = self.parsed.inflect({'datv'}).word
            self.parsed = n
            self.parsed = declensify(morph, self.parsed, [case])
            self.word = self.parsed.word
        else:
            #print(self.word)
            self.word = declensify_text(morph, self.word, [case])
            #print(self.word)
            self.parsed = morph.parse(self.word.split(' ')[1])[0]

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



# склоняем по умолчанию или с obj_case от predicate
class Object(Noun):
    def __init__(self, words, morph, noun_type=None, case=None, context=None, min_seriousness=None, max_seriousness=None):
        Noun.__init__(self, words, morph, noun_type=noun_type, case=case, context=context, min_seriousness=min_seriousness, max_seriousness=max_seriousness)
        self.member = 'object'
    
        
        


# TODO SHIT GETS REAL
# or not. можно сделать тупую функцию, а всю логику добавить в конструктор
class Adverbial(Noun):
    def __init__(self, words, morph, noun_type=None, case=None, context=None, min_seriousness=None, max_seriousness=None):
        Noun.__init__(self, words, morph, noun_type=noun_type, case=case, context=context, min_seriousness=min_seriousness, max_seriousness=max_seriousness)
        self.member = 'adverbial'
        


# class Predlog():
#     def __init__(self, words, morph, word=None, context=None):
#         if word.case == 'accs' and word.type == 'event' and word.member == 'object':
#             self.word = ''
#         # elif word.case == 'accs':
#         #     if word.type in ['event', 'project']:
#         #         if word.member == 'adverbial':
#         #             self.word = 'для'
#         elif word.type:
#             predlogs = words['predlog'].fillna(value='')
#             self.info = predlogs[(predlogs.noun_type==word.type) & (predlogs.noun_case==word.case)].sample()
#             self.word = self.info.iloc[0, 0]
#         else:
#             self.info = None
#             self.word = ''        
        


class Beginning():
    def __init__(self, words, morph, tense='pres', context=None, min_seriousness=None, max_seriousness=None):
        beginnings = words['beginning']
        if min_seriousness:
            beginnings = beginnings[beginnings.seriousness>=min_seriousness]
        if max_seriousness:
            beginnings = beginnings[beginnings.seriousness<=max_seriousness]        
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
    def __init__(self, words, morph, tense='pres', type='beginning', custom_word_parsed=None, context=None, min_seriousness=None, max_seriousness=None):
        sentences = words['sentences']

        if min_seriousness:
            sentences = sentences[sentences.seriousness>=min_seriousness]
        if max_seriousness:
            sentences = sentences[sentences.seriousness<=max_seriousness]


        if custom_word_parsed:
            self.info = sentences[((sentences.tense==tense)|(sentences.tense=='all'))&(sentences.type==type)&(sentences.is_custom==True)].sample()
            self.word = self.info.sentence.iloc[0]
            self.word = self.word.strip().capitalize()
            case = self.info.word_case.iloc[0]
            #print(f'custon_word_parsed: {custom_word_parsed}, case {case}')
            word = custom_word_parsed.inflect({case}).word

            if len(custom_word_parsed.word.split(' ')) == 1:
            #self.word = self.parsed.inflect({'datv'}).word
                custom_word_parsed = declensify(morph, custom_word_parsed, [case]).word
            else:
                custom_word_parsed = declensify_text(morph, custom_word_parsed.word, [case])
                #print(self.word)
            if needs_capitalizing(morph, word):
                word = word.capitalize()
            self.word = self.word.replace('<word>', word)
        else:
            self.info = sentences[((sentences.tense==tense)|(sentences.tense=='all'))&(sentences.type==type)&(sentences.is_custom==False)].sample()
            self.word = self.info.sentence.iloc[0]
            self.word = self.word.strip().capitalize()
        
        #print(self.word)
    