'''
Объекты, представляющие части речи
'''
import random

# существительное
class Subject():
    def __init__(self, words, subject_is_myself=1):
        # TODO: другие существительные (тёща, жена, итд) из таблицы + зависимость от времени (в дательном падеже прошлое время - нельзя?..)
        # + зависимость от контекста
        # TODO: если субъект не ты, то добавлять что-то типа "надо помочь", "не могу отказаться", "придется помочь" и т.д.
        # возможно это уже совсем другой шаблон

        subjects = words['subj'].fillna(value=0)

        self.is_myself = subject_is_myself
        self.info = subjects[subjects.is_myself==subject_is_myself].sample()
        self.word = self.info.iloc[0, 0]

         


# TODO: реализовать использование альтернативных типов. рандом
# TODO: реализовать использование флага to_be "буду делать" для будущего времени (и в файле добавь)
# TODO: реализовать склонение по времени
# сказуемое
class Predicate():
    def __init__(self, words=None, morph=None, noun_type=None, subject=None, has_object=0, has_adv=0, to_be=0):

        self.has_object = has_object
        #self.has_adv = has_adv
        subj = morph.parse(subject.word)[0]
        verbs = words['verb'].fillna(value=0)

        # насильно проставляем тип
        if noun_type:
            self.info = verbs[verbs.noun_type==noun_type].sample()

        # или решаем автоматически
        else:
            if self.has_object:
                self.info = verbs[verbs.noun_type.isin(['thing', 'person', 'project'])].sample()
            # TODO: есть ещё один кейс - "поработать над чем-то где-то" / "поработаь над чем-то для чего-то или кого-то"
            else:
                self.info = verbs[verbs.noun_type.isin(['place'])].sample()

        self.word = morph.parse(self.info.iloc[0, 0])[0]
        self.noun_type = self.info.iloc[0, 1]
        self.case_obj = self.info.iloc[0, 3]

        # SPICE
        # "мне нужно"
        if 'datv' in subj.tag:
            self.word = self.word.normal_form
            # TODO: более продвинутый спайс для "мне", "ей"
            self.word = f"{random.choice(['нужно', 'надо', 'придется', 'давно пора'])} {self.word}"
        # "я cобирался", "она обещала"
        # TODO: учитывать контекст пола юзера
        else:
            self.word = self.word.normal_form
            tense = random.choice(['past']) # убрал настоящее - с ним мороки много, можно потом добавить 
            # TODO: "должен" не склоняется?.. надо что-то делать с этим. а также с "вынужден", "обязан"...это другая часть речи и надо делать под нее обработку
            # TODO: отдельная таблица для зачинов
            # TODO: склонение спайса для он-она-они не работает
            spice = random.choice(['собираться', 'планировать', 'хотеть', 'обещать'])
            spice = morph.parse(spice)[0]
            
            if tense == 'pres' and 'anim' in subj.tag:
                spice = spice.inflect({'3per'})
            else:
                for grm in ['1per', '2per', '3per', 'sing', 'plur', 'masc', 'femn']:
                    if grm in subj.tag:
                        spice_modified = spice.inflect({grm})
                        if spice_modified:
                            spice = spice_modified
                        else:
                            raise Exception(f'Error: Could not inflect on word "{spice.word}" !')
                spice = spice.inflect({tense})

            self.word = f"{spice.word} {self.word}"


# дополнение, здесь всё довольно просто
class Object():
    def __init__(self, words=None, morph=None, predicate=None):
        nouns = words['noun']
        self.type = predicate.noun_type
        self.info = nouns[nouns.type==self.type].sample()

        n = morph.parse(self.info.iloc[0, 0])[0]
        # TODO: другие падежи для дополнения
        # везти тёщу, работать над проектом, успевать к вечеринке

        self.case = 'accs'
        if predicate.case_obj:
            self.case = predicate.case_obj

        self.word = n.inflect({self.case}).word


# обстоятельство и предлог
class Adverbial():
    def __init__(self, words=None, morph=None, predicate=None, object=None):
        nouns = words['noun']
        #self.info = None #костыль
        # TODO: этот кусок можно отрефакторить в таблицу
        # TODO: ИЛИ тупо передавать тип обстоятельства, так у меня больше контроля за выходками генератора
        if object:
            if object.type == 'person':
                self.info = nouns[nouns.type.isin(['place', 'place_open', 'event', 'person'])].sample()
            if object.type == 'thing':
                self.info = nouns[nouns.type.isin(['place', 'place_open', 'person'])].sample()
            # TODO: реализовать кейсы "поработать над работой для жены", "поработать над работой с женой"
            if object.type == 'project':
                self.info = nouns[nouns.type.isin(['person', 'project', 'event'])].sample() 
        else:
            self.info = nouns[nouns.type==predicate.noun_type].sample()

        #
        # FIXME: почему-то пишет 'Adverbial' object has no attribute 'info'
        self.type = self.info.iloc[0, 1]

        n = morph.parse(self.info.iloc[0, 0])[0]

        # TODO: вместо этого блока - словарь соответствий для падежей
        if self.type == 'person':
            if object.type == 'person':
                self.case = 'datv'
            if object.type == 'thing':
                self.case = 'gent'
            if object.type == 'project':
                self.case = random.choice(['gent', 'ablt'])               
        else:
            # TODO: более продвинутое присвоение падежей
            cases = {'thing': 'ablt', 'event': 'accs', 'place': 'accs', 'place_open': 'accs', 'project': 'ablt'}
            self.case = cases[self.type]
        
        # TODO: поганый костыль для фикса ситуаций когда мы делаем проект для кого-то или чего-то
        if object and object.type == 'project':
            if self.type == 'person':
                self.case = random.choice(['albt', 'gent'])
            if self.type == 'event':
                self.case = 'datv'
            else:
                self.case = 'gent'

        n = n.inflect({self.case}) 

        self.word = n.word



# на потом, пока не надо
# идея: прилагательное - для проектов и дел, например "срочное дело", "важный проект". надо склонять
# вообще прилагательные точно так же подходят по контекстам и их реально надо склонять
# определение
class Attribute():
    pass



class Predlog():
    def __init__(self, words, noun):
        predlogs = words['predlog'].fillna(value='')
        self.info = predlogs[(predlogs.noun_type==noun.type) & (predlogs.noun_case==noun.case)].sample()
        self.word = self.info.iloc[0, 0]



# TODO: рефакторнуть все спайсы в один класс? и хранить в одной таблице?
class Beginning():
    def __init__(self, words):
        beginnings = words['beginning']
        self.info = beginnings.sample()
        self.word = self.info.iloc[0, 0]
        if self.info.iloc[0, 1]:
            self.word += ','


class Ending():
    def __init__(self, words, subject):
        endings = words['ending']
        self.info = endings.sample()
        self.word = self.info.iloc[0, 0]

        if not subject.is_myself:
            pass

