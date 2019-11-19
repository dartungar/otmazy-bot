# one function to rule them all
# one function to find them
# one to arrange them all
# and in the sentence bind them
from words_stupid import declensify, Subject, Predicate, PredicateSpice, Noun, Object, Adverbial, Predlog, Beginning, Ending
from helpers import *


def constructor(words, morph, tense='pres', context='default', subject_is_myself=True, object_type=None, has_beginning=False, has_ending=False):
    
    # subject
    subject = Subject(words=words, subject_is_myself=subject_is_myself)

    # predicate spice
    # TODO: рандом с весом на to_be
    predicate_spice = PredicateSpice(words=words, morph=morph, tense=tense, subj=subject, to_be=False)

    # predicate
    pred_noun_type = get_predicate_noun_type(object_type=object_type)
    predicate = Predicate(words=words, morph=morph, tense=tense, noun_type=pred_noun_type)


    # object
    obj = ''
    # если есть объект
    if object_type:
        obj_type = object_type

        if predicate.case_obj:
            obj_case = predicate.case_obj
        else:
            obj_case = 'accs'

        obj = Object(words=words, morph=morph, noun_type=obj_type, case=obj_case)


    # adverbial
    adv_type = get_adverbial_type(object_type=object_type, predicate_noun_type=pred_noun_type)
    adv_case = get_adverbial_case(object_type=object_type, adverbial_type=adv_type)
    adverbial = Adverbial(words=words, morph=morph, noun_type=adv_type, case=adv_case)

    # predlog
    # TODO: предлоги разве только в одном месте?
    # пока обойдемся предлогом к обстоятельству
    # predlog_type = None
    # predlog_case = None
    predlog = Predlog(words=words, morph=morph, predlog_type=adv_type, case=adv_case)

    # beginning
    beginning = ''
    if has_beginning:
        beginning = Beginning(words=words, morph=morph).word

    # ending
    ending = ''
    if has_ending:
        ending = Ending(words=words, morph=morph).word
    
    # TODO: Динамический конструктор. как минимум предлоги, beginning & ending стоит динамически вставлять
    text = f'{beginning} {subject} {predicate_spice} {predicate} {obj} {predlog} {adverbial} {ending}'

    return text

