# one function to rule them all
# one function to find them
# one to arrange them all
# and in the sentence bind them
from words_stupid import Subject, Predicate, PredicateSpice, Noun, Object, Adverbial, Beginning, EndingSentence
from helpers import declensify, get_rules
import random


def constructor(words, morph, tense='futr', context='default', 
                subject_is_myself=True, 
                subj_datv=False, 
                has_predicate_spice=True, 
                to_be=False, 
                has_object=False, 
                has_adverbial=True, 
                has_beginning=False, 
                has_ending=False,
                min_seriousness=None,
                max_seriousness=None):
    
    # subject
    subject = Subject(words=words, morph=morph, subject_is_myself=subject_is_myself, datv=subj_datv, min_seriousness=min_seriousness)

    # predicate spice
    # TODO: рандом с весом на to_be
    predicate_spice = ''
    pred_aspc = 'impf'
    # фиксим несоответствие, если задали кривые вводные параметры
    if not has_predicate_spice and 'datv' in subject.parsed.tag:
        has_predicate_spice = True
    # мне нужно будет ...
    if has_predicate_spice and to_be:
        predicate_spice = PredicateSpice(words=words, morph=morph, tense=tense, subj=subject, to_be=to_be).word
    # мне нужно ... или я пообещал ...
    elif (has_predicate_spice or 'datv' in subject.parsed.tag) and not to_be:
        predicate_spice = PredicateSpice(words=words, morph=morph, tense=tense, subj=subject, to_be=to_be).word
        pred_aspc = 'perf'
    # несовершенные глаголы не могут быть в настоящем! оставляем только совершенные
    elif (tense == 'futr' or tense == 'past') and not predicate_spice:
        pred_aspc = 'perf'
    
    # predicate
    predicate = Predicate(words=words, morph=morph, tense=tense, has_object=has_object, aspc=pred_aspc, min_seriousness=min_seriousness)

    # TODO: переработать блок сказуемого чтобы не было нужды в этой хуйне
    rules = get_rules(words, predicate)


    # object FIXME: просто ставить accs - даёт баги. исправь
    # if predicate.case_object:
    #     obj_case = predicate.case_object
    # else:
    #     obj_case = 'accs'

    #print(tense)
    # склоняем сказуемое, если нет спайса
    if not predicate_spice:
        if pred_aspc == 'perf' or tense == 'past':
            predicate.parsed = declensify(morph, predicate.parsed, subject, tense=tense)
        else:
            predicate.parsed = declensify(morph, predicate.parsed, subject)
        predicate.word = predicate.parsed.word

    #print(predicate.parsed)

    obj = ''
    predlog_obj = ''
    if rules.obj_type.iloc[0]:
        obj = Object(words=words, morph=morph, noun_type=rules.obj_type.iloc[0], case=rules.obj_case.iloc[0], min_seriousness=min_seriousness)
        #print(obj.word)

        predlog_obj = rules.predlog_obj.iloc[0]


    # TODO: разобраться, что влияет на наличие обстоятельства и как я хочу этим управлять
    if has_adverbial:
        # adverbial
        adverbial = Adverbial(words=words, morph=morph, noun_type=rules.adv_type.iloc[0], case=rules.adv_case.iloc[0], min_seriousness=min_seriousness)

        # predlog
        predlog_adv = rules.predlog_adv.iloc[0]


    # beginning
    beginning = ''
    if has_beginning:
        beginning = Beginning(words=words, morph=morph, min_seriousness=min_seriousness, max_seriousness=max_seriousness).word
        #beginning = declensify_text(morph, beginning, subject, tense, context)


    # новый ending!
    has_ending_sentence = has_ending # TODO: реворк в параметр функции
    end_sentence = ''
    cwp = None
    if has_ending_sentence:
        has_cwp = random.randint(0, 1)
        if has_cwp:
            if subject.is_myself == False:
                cwp = subject.parsed
            elif obj:
                cwp = obj.parsed
            else:
                cwp = adverbial.parsed
        end_sentence = EndingSentence(words=words, morph=morph, tense=tense, type='ending', custom_word_parsed=cwp, min_seriousness=min_seriousness)
        #print(end_sentence.word)

    text = f"{beginning} {subject.word} {predicate_spice} {predicate.word} {predlog_obj if predlog_obj else ''} {obj.word if obj else ''} {predlog_adv if predlog_adv else ''} { adverbial.word if adverbial else ''}. {end_sentence.word if has_ending_sentence else ''}"

    return text

