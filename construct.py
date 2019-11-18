# one function to rule them all
# one function to find them
# one to arrange them all
# and in the sentence bind them
from words_stupid import declensify, Subject, Predicate, PredicateSpice, Noun, Object, Adverbial, Predlog, Beginning, Ending



def constructor(words, morph, tense='pres', context='default', subject_is_myself=True, has_beginning=False, has_ending=False):
    
    # subject
    subject = Subject(words=words, subject_is_myself=subject_is_myself)


    #predicate spice
    # TODO: рандом с весом на to_be
    predicate_spice = PredicateSpice(words=words, morph=morph, tense=tense, subj=subject, to_be=False)

    #predicate
    # TODO: логика получения noun_type
    pred_noun_type = None
    predicate = Predicate(words=words, morph=morph, tense=tense, noun_type=pred_noun_type)

    # object
    # TODO: obj_noun_type
    # TODO: obj_case
    obj_type = None
    obj_case = None
    obj = Object(words=words, morph=morph, noun_type=obj_type, case=obj_case)

    #adverbial
    adv_type = None
    adv_case = None
    adverbial = Adverbial(words=words, morph=morph, noun_type=adv_type, case=adv_case)

    #predlog
    # TODO: предлоги разве только в одном месте?
    predlog_type = None
    predlog_case = None
    predlog = Predlog(words=words, morph=morph, predlog_type=predlog_type, case=predlog_case)

    #beginning
    beginning = ''
    if has_beginning:
        beginning = Beginning(words=words, morph=morph).word

    #ending
    ending = ''
    if has_ending:
        ending = Ending(words=words, morph=morph).word
    
    # TODO: Динамический конструктор. как минимум предлоги, beginning & ending стоит динамически вставлять
    text = f'{beginning} {subject.word} {predicate_spice.word} {predicate.word} {obj.word} {predlog.word} {adverbial.word} {ending}'

    return text

