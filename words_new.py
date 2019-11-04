'''
Объекты, представляющие части речи
'''
import random

# существительное
class Subject():
    def __init__(self):
        # TODO: более продвинутые существительные, епт! + зависимость от времени (в дательном падеже прошлое время - нельзя?..)
        self.word = random.choice(['я', 'мне']) 


# TODO: реализовать использование альтернативных типов. рандом
# TODO: реализовать использование флага to_be "буду делать" для будущего времени (и в файле добавь)
# TODO: реализовать "я должен сделать" (тоже в инфинитив ставится)
# TODO: реализовать склонение по времени
# сказуемое
class Predicate():
    def __init__(self, words=None, morph=None, subject=None, has_object=0, to_be=0):

        self.has_object = has_object
        subj = morph.parse(subject.word)[0]
        verbs = words['verb']

        if self.has_object:
            self.info = verbs[verbs.noun_type.isin(['thing', 'person'])].sample()
        else:
            self.info = verbs[verbs.noun_type.isin(['place', 'project'])].sample()

        self.word = morph.parse(self.info.iloc[0, 0])[0]
        self.noun_type = self.info.iloc[0, 3]

        # "мне нужно"
        if 'datv' in subj.tag:
            self.word = self.word.normal_form
            # TODO: более продвинутый спайс для "мне", "ей"
            self.word = f"{random.choice(['нужно', 'надо', 'придется', 'давно пора'])} {self.word}"
        # "я должен", "она должна"
        # TODO: учитывать контекст пола юзера
        # TODO: рандомный выбор времени, мб настоящее и прошлое; в соответствии с ним выбор спайса из таблицы (ее тоже надо сделать)
        else:
            self.word = self.word.normal_form
            spice = random.choice(['должен', 'собираюсь', 'хочу', 'обязался', 'планирую', 'планировал', 'хотел', 'собирался', 'обещал'])
            spice = morph.parse(spice)[0]
            for grm in ['1per', '2per', '3per', 'sing', 'plur']:
                if grm in subj.tag:
                    spice_modified = spice.inflect({grm})
                    if spice_modified:
                        spice = spice.inflect({grm})
                    else:
                        raise Exception(f'Error: Could not inflect on word "{spice.word}" !')
            
            self.word = f"{spice.word} {self.word}"


# дополнение, здесь всё довольно просто
class Object():
    def __init__(self, words=None, morph=None, predicate=None):
        nouns = words['noun']
        self.type = predicate.noun_type
        self.info = nouns[nouns.type == self.type].sample()

        n = morph.parse(self.info.iloc[0, 0])[0]
        self.word = n.inflect({'accs'}).word


# TODO
# обстоятельство и предлог
class Adverbial():
    def __init__(self, words=None, morph=None, predicate=None, object=None):
        nouns = words['noun']
        if predicate.has_object:
            if object.type == 'person':
                self.info = nouns[nouns.type.isin(['place', 'event'])].sample()
            if object.type == 'thing':
                self.info = nouns[nouns.type.isin(['place'])].sample() 
        else:
            self.info = nouns[nouns.type.isin(['place', 'event', 'project'])].sample()

        self.type = self.info.iloc[0, 3]

        n = morph.parse(self.info.iloc[0, 0])[0]

        # TODO: словарь соответствия блэт, чтобы без этих условий обойтись
        if self.type == 'person':
            n = n.inflect({'datv'})
        else:
            # TODO: добавить person в кейсе ЗА тёщей, но там надо логику в целом улучшать
            cases = {'thing': 'ablt', 'event': 'accs', 'place': 'accs', 'project': 'ablt'}
            n = n.inflect({cases[self.type]}) 

        predlogs = {'person': 'к', 'thing': 'за', 'place': 'в', 'place_open': 'на', 'event': 'на', 'project': 'над'}
        predlog = predlogs[self.type]

        self.word = f'{predlog} {n.word}'



# на потом, пока не надо
# идея: прилагательное - для проектов и дел, например "срочное дело", "важный проект". надо склонять
# определение
class Attribute():
    pass
    

class Beginning():
    def __init__(self, words):
        beginnings = words['beginning']
        self.info = beginnings.sample()
        self.word = self.info.iloc[0, 0]
        if self.info.iloc[0, 1]:
            self.word += ','
