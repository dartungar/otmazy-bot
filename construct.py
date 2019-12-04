# one function to rule them all
# one function to find them
# one to arrange them all
# and in the sentence bind them
from words_stupid import Subject, Predicate, PredicateSpice, Noun, Object, Adverbial, Predlog, Beginning, Ending
from helpers import *


def constructor(words, morph, tense='futr', context='default', subject_is_myself=True, has_predicate_spice=True, to_be=False, has_object=False, has_adverbial=True, has_beginning=False, has_ending=False):
    
    # subject
    subject = Subject(words=words, morph=morph, subject_is_myself=subject_is_myself)

    # predicate spice
    # TODO: рандом с весом на to_be
    predicate_spice = ''
    pred_aspc = 'impf'
    if (has_predicate_spice or 'datv' in subject.parsed.tag) and not to_be:
        predicate_spice = PredicateSpice(words=words, morph=morph, tense=tense, subj=subject, to_be=to_be).word
        pred_aspc = 'perf'
    elif has_predicate_spice and to_be:
        predicate_spice = PredicateSpice(words=words, morph=morph, tense=tense, subj=subject, to_be=to_be).word
    elif (tense == 'futr' or tense == 'past') and not predicate_spice:
        pred_aspc = 'perf'
    
    # predicate
    predicate = Predicate(words=words, morph=morph, tense=tense, has_object=has_object, aspc=pred_aspc)

    # TODO: переработать блок сказуемого чтобы не было нужды в этой хуйне
    


    # object TODO: проверить актуальна ли такая механика
    if predicate.case_object:
        obj_case = predicate.case_object
    else:
        obj_case = 'accs'


    # склоняем сказуемое, если нет спайса
    if not predicate_spice:
        if pred_aspc == 'perf':
            predicate.parsed = declensify(morph, predicate.parsed, subject, tense=tense)
        else:
            predicate.parsed = declensify(morph, predicate.parsed, subject)
        predicate.word = predicate.parsed.word

    #print(predicate.parsed)

    obj = ''
    predlog_obj = ''
    if has_object:
        obj_type = get_noun_type(words=words, verb_type=predicate.type, noun_kind='obj')
        obj = Object(words=words, morph=morph, noun_type=obj_type, case=obj_case)

        predlog_obj = Predlog(words=words, morph=morph, predlog_type=obj.type, case=obj_case)


    if has_adverbial:
        # adverbial
        adv_type = get_noun_type(words=words, verb_type=predicate.type, noun_kind='adv')
        adv_case = get_adverbial_case(object_type=obj.type if has_object else None, adverbial_type=adv_type, predicate_noun_type=obj_type if has_object else None)
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
        #beginning = declensify_text(morph, beginning, subject, tense, context)

    # ending
    ending = ''
    if has_ending:
        ending = Ending(words=words, morph=morph, tense=tense).word
        #ending = declensify_text(morph, ending, subject.parsed, tense, context)  


    text = f"{beginning} {subject.word} {predicate_spice} {predicate.word} {predlog_obj.word if predlog_obj else ''} {obj.word if obj else ''} {predlog_adv.word if predlog_adv else ''} { adverbial.word if adverbial else ''} {ending if ending else ''}"

    # text = ' '.join([beginning,
    #                 subject.word,
    #                 predicate_spice,
    #                 predicate.word,
    #                 predlog_obj.word if predlog_obj else '',
    #                 obj.word if obj else '',
    #                 predlog_adv.word if predlog_adv else '',
    #                 adverbial.word if adverbial else '',
    #                 ending if ending else ''])

    return text

