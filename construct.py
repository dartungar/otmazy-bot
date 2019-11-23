# one function to rule them all
# one function to find them
# one to arrange them all
# and in the sentence bind them
from words_stupid import Subject, Predicate, PredicateSpice, Noun, Object, Adverbial, Predlog, Beginning, Ending
from helpers import *


def constructor(words, morph, tense='pres', context='default', subject_is_myself=True, has_predicate_spice=True, object_type=None, adv_type=None, has_beginning=False, has_ending=False):
    
    # subject
    subject = Subject(words=words, morph=morph, subject_is_myself=subject_is_myself)

    # predicate spice
    # TODO: рандом с весом на to_be
    predicate_spice = ''
    pred_aspc = 'impf'
    if has_predicate_spice or 'datv' in subject.parsed.tag:
        predicate_spice = PredicateSpice(words=words, morph=morph, tense=tense, subj=subject, to_be=False).word
        pred_aspc = 'perf'

    # predicate
    pred_noun_type = get_predicate_noun_type(object_type=object_type)
    predicate = Predicate(words=words, morph=morph, tense=tense, noun_type=pred_noun_type, aspc=pred_aspc)
    #predicate = declensify(morph, predicate.parsed, subject.parsed)

    # object
    if predicate.case_obj:
        obj_case = predicate.case_obj
    else:
        obj_case = 'accs'

    # склоняем сказуемое, если нет спайса
    if not predicate_spice:
        if pred_aspc == 'perf':
            predicate = declensify(morph, predicate.parsed, subject.parsed, tense=tense)
        else:
            predicate = declensify(morph, predicate.parsed, subject.parsed)
 



    obj = Object(words=words, morph=morph, noun_type=object_type, case=obj_case)

    predlog_obj = Predlog(words=words, morph=morph, predlog_type=object_type, case=obj_case)



    # adverbial
    if adv_type:
        adv_type = adv_type
    else:
        adv_type = get_adverbial_type(object_type=object_type, predicate_noun_type=pred_noun_type)
    adv_case = get_adverbial_case(object_type=object_type, adverbial_type=adv_type)
    adverbial = Adverbial(words=words, morph=morph, noun_type=adv_type, case=adv_case)

    # predlog
    # TODO: предлоги разве только в одном месте?
    # пока обойдемся предлогом к обстоятельству
    # predlog_type = None
    # predlog_case = None
    predlog_adv = Predlog(words=words, morph=morph, predlog_type=adv_type, case=adv_case)

    # beginning
    beginning = ''
    if has_beginning:
        beginning = Beginning(words=words, morph=morph).word

    # ending
    ending = ''
    if has_ending:
        ending = Ending(words=words, morph=morph, tense=tense).word
    
    # TODO: Динамический конструктор. как минимум предлоги, beginning & ending стоит динамически вставлять
    text = f'{beginning} {subject.word} {predicate_spice} {predicate.word} {predlog_obj.word} {obj.word} {predlog_adv.word} {adverbial.word} {ending}'

    return text

