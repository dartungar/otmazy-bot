# "глупые" классы - принимают готовые параметры для подбора слова

def declensify(morph, word_parsed, subj):
    for grm in ['1per', '2per', '3per', 'sing', 'plur', 'masc', 'femn']:
        if grm in subj.tag:
            word_modified = word_parsed.inflect({grm})
            if word_modified:
                word = word_modified
            else:
                raise Exception(f'Error: Could not inflect on word "{spice.word}" !')
    return word


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


        

# TODO: реворкнуть в выбор из БД PredicateSpice?
class PredicateSpice():
    def __init__(self, words, morph, tense='pres', subj=None, to_be=False):

        if to_be:
            tobe = morph.parse('быть')[0]
            tobe = tobe.inflect({tense})

        # мне нужно, тёща придется
        if 'datv' in subj.tag:
            if to_be:
                self.word = f"{tobe} {random.choice(['нужно', 'надо', 'необходимо'])}"
            if not to_be:
                self.word = random.choice(['нужно', 'надо', 'необходимо', 'придется', 'давно пора', 'позарез надо', 'припекло'])
        elif 'nomn' in subj.tag:
            # TODO: склонение с помощью declensify
            self.word = morph.parse(random.choice(['собираться', 'планировать', 'хотеть', 'обещать']))[0]
            if tense=='pres' and 'anim' in suj.tag:
                self.word = self.word.inflect({'3per'})
            else:
                self.word = declensify(morph, self.word, subj)
            self.word = self.word.inflect({tense})
        else:
            raise Exception('Invalid Case for Predicate Spice!')




# TODO
class Predicate():
    def __init__(self, words, morph, tense='pres', noun_type=None, case=None):
        # тип
        verbs = words['verb'].fillna(value=0)
            
        self.info = verbs[verbs.noun_type == noun_type].sample()
        # спайс
        self.word = self.info.iloc[0, 0].normal_form
        self.case_obj = self.info.iloc[0, 3]



        # принимает падеж
        pass


# TODO
class Object():
    def __init__(self, words, morph, type=None, case='accs'):
        
        
        pass


# TODO
class Adverbial():
    def __init__(self, words, morph, type=None, case=None):

        pass


# TODO
class Predlog():
    def __init__(self, words, morph, type=None, case=None):

        pass


# TODO
class Beginning():
    def __init__(self, words, morph):

        pass


# TODO
class Ending():
    def __init__(self, words, morph:

        pass