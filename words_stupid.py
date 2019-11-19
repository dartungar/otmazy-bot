# "глупые" классы - принимают готовые параметры для подбора слова
import random

def declensify(morph, word_parsed, subj):
    for grm in ['1per', '2per', '3per', 'sing', 'plur', 'masc', 'femn']:
        if grm in subj.tag:
            word_modified = word_parsed.inflect({grm})
            if word_modified:
                word = word_modified
            else:
                raise Exception(f'Error: Could not inflect on word "{word.word}" !')
    return word


# существительное
class Subject():
    def __init__(self, words, subject_is_myself=True):
        # TODO: другие существительные (тёща, жена, итд) из таблицы + зависимость от времени (в дательном падеже прошлое время - нельзя?..)
        # + зависимость от контекста
        # TODO: если субъект не ты, то добавлять что-то типа "надо помочь", "не могу отказаться", "придется помочь" и т.д.
        # возможно это уже совсем другой шаблон

        subjects = words['subj'].fillna(value=0)

        self.is_myself = subject_is_myself
        self.info = subjects[subjects.is_myself==subject_is_myself].sample()
        self.word = self.info.iloc[0, 0]


        

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
        # я собираюсь, тёща хочет
        elif 'nomn' in subj.tag:
            self.word = morph.parse(random.choice(['собираться', 'планировать', 'хотеть', 'обещать']))[0]
            # TODO: избавиться от необходимости передавать подлежащее
            if tense=='pres' and 'anim' in subj.tag:
                self.word = self.word.inflect({'3per'})
            else:
                self.word = declensify(morph, self.word, subj)
            self.word = self.word.inflect({tense})
        else:
            raise Exception('Invalid Case for Predicate Spice!')




class Predicate():
    def __init__(self, words, morph, tense='pres', noun_type=None, case=None):
        # тип
        verbs = words['verb'].fillna(value=0)
            
        self.info = verbs[verbs.noun_type == noun_type].sample()
        # спайс
        self.word = morph.parse(self.info.iloc[0, 0])[0].normal_form
        # TODO: более изящное решение через БД
        self.case_obj = self.info.iloc[0, 3]


        # принимает падеж? TODO: разобраться, надо ли оно мне
        pass


# класс-родитель для всех существительных
class Noun():
    def __init__(self, words, morph, noun_type=None, case=None):
        nouns = words['noun'].fillna(value='')
        self.info = nouns[nouns.type==noun_type].sample()
        n = morph.parse(self.info.iloc[0, 0])[0]
        self.word = n.inflect({case}).word



# склоняем по умолчанию или с obj_case от predicate
class Object(Noun):
    pass
        
        


# TODO SHIT GETS REAL
# or not. можно сделать тупую функцию, а всю логику добавить в конструктор
class Adverbial(Noun):
    pass

        


class Predlog():
    def __init__(self, words, morph, predlog_type=None, case=None):
        predlogs = words['predlog'].fillna(value='')
        self.info = predlogs[(predlogs.noun_type==predlog_type) & (predlogs.noun_case==case)].sample()
        self.word = self.info.iloc[0, 0]
        


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
        