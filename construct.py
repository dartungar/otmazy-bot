# one function to rule them all
# one function to find them
# one to arrange them all
# and in the sentence bind them
from words_stupid import Subject, Predicate, PredicateSpice, Noun, NounSpice, Greeting, BeginningSpice, EndingSentence
from helpers import declensify, get_rules, needs_capitalizing, make_rules_nonsense
import random


def constructor(words, morph, tense='futr', context=None, is_nonsense=False,
                min_seriousness=None,
                max_seriousness=None,
                subject_is_myself=True, 
                subj_datv=False, 
                has_predicate_spice=True, 
                to_be=False, 
                has_beginning=False,
                has_greeting=False, 
                has_ending=False):
    

    word_list = []
    unexplained_person = None

    # subject
    subject = Subject(words=words, morph=morph, datv=subj_datv, context=context, min_seriousness=min_seriousness, max_seriousness=max_seriousness)

    if 'Name' in subject.parsed.tag:
        unexplained_person = subject
        word_list.append(subject.word.capitalize())
    else:
        word_list.append(subject.word)

    # predicate spice
    # TODO: этой поебени сильно нужен реворк! возможно, в таблицу соответствий
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
    
    word_list.append(predicate_spice)
    

    # predicate
    predicate = Predicate(words=words, morph=morph, tense=tense, aspc=pred_aspc, context=context, min_seriousness=min_seriousness, max_seriousness=max_seriousness)

    # TODO: переработать блок сказуемого чтобы не было нужды в этой хуйне
    rules = get_rules(words, predicate)
    if is_nonsense:
        rules = make_rules_nonsense(rules)


    # склоняем сказуемое, если нет спайса
    if not predicate_spice:
        if pred_aspc == 'perf' or tense == 'past':
            predicate.parsed = declensify(morph, predicate.parsed, tags=[subject.person, subject.plural, subject.gender], tense=tense)
        else:
            predicate.parsed = declensify(morph, predicate.parsed, tags=[subject.person, subject.plural, subject.gender])
        predicate.word = predicate.parsed.word

    word_list.append(predicate.word)
    #print(predicate.parsed)

          

    if rules.word1.iloc[0]:
        if rules.word1.iloc[0] == 'noun':
            word1 = Noun(words=words, morph=morph, noun_type=rules.word1_type.iloc[0], case=rules.word1_case.iloc[0], context=context, min_seriousness=min_seriousness, max_seriousness=max_seriousness)
            if 'Name' in word1.parsed.tag:
                unexplained_person = word1
        #print(word1.word)

        if rules.word1_predlog.iloc[0]:
            word1_predlog = rules.word1_predlog.iloc[0]
            word_list.append(word1_predlog)

        word_list.append(word1.word)


    if rules.word2.iloc[0]:
        # word2
        if rules.word2.iloc[0] == 'noun':
            word2 = Noun(words=words, morph=morph, noun_type=rules.word2_type.iloc[0], case=rules.word2_case.iloc[0], context=context, min_seriousness=min_seriousness, max_seriousness=max_seriousness)
            if 'Name' in word2.parsed.tag:
                unexplained_person = word2
        # predlog
        if rules.word2_predlog.iloc[0]:
            word2_predlog = rules.word2_predlog.iloc[0]
            word_list.append(word2_predlog)

        word_list.append(word2.word)


    if rules.word3.iloc[0]:
        # word3
        if rules.word3.iloc[0] == 'noun':
            word3 = Noun(words=words, morph=morph, noun_type=rules.word3_type.iloc[0], case=rules.word3_case.iloc[0], context=context, min_seriousness=min_seriousness, max_seriousness=max_seriousness)
            if 'Name' in word3.parsed.tag:
                unexplained_person = word3
        # predlog
        if rules.word3_predlog.iloc[0]:
            word3_predlog = rules.word3_predlog.iloc[0]
            word_list.append(word3_predlog)

        word_list.append(word3.word)

    # запятая в конце основного предложения
    word_list.append('.')


    # beginning spice "Тут такое дело..."
    if has_beginning:
        beginning = BeginningSpice(words=words, morph=morph, context=context, min_seriousness=min_seriousness, max_seriousness=max_seriousness).word
        #beginning = declensify_text(morph, beginning, subject, tense, context)
        if beginning.endswith('.'):
            word_list[0] = word_list[0].capitalize()
        word_list.insert(0, beginning)
        

    
    #greeting "Привет"
    if has_greeting:
        greeting = Greeting(words=words, morph=morph, context=context, min_seriousness=min_seriousness, max_seriousness=max_seriousness).word
        #beginning = declensify_text(morph, beginning, subject, tense, context)
        word_list[0] = word_list[0].capitalize()
        word_list.insert(0, greeting)     
   


    # ending sentence "Извините меня, пожалуйста"
    if has_ending:
        end_sentence = EndingSentence(words=words, morph=morph, tense=tense, type='ending', context=context, min_seriousness=min_seriousness, max_seriousness=max_seriousness)
        #print(end_sentence.word)
        word_list.append(end_sentence.word)
        word_list.append('.')


    # если вбросили какое-то имя - даем подобие объяснения
    if unexplained_person:
        explanation = EndingSentence(words=words, morph=morph, tense=tense, type='explanation', context=context, custom_word_parsed=unexplained_person.parsed, min_seriousness=min_seriousness, max_seriousness=max_seriousness)
        #print(end_sentence.word)
        word_list.append(explanation.word)
        word_list.append('.')
    # можем и просто красок добавить на тему чего-то из отмазы
    else:
        #cwp = None
        has_cwp = random.randint(0, 1)
        if has_cwp:
            if not subject.is_myself:
                cwp = subject.parsed #TODO: добавить ExplainSentence
            elif word1:
                cwp = word1.parsed
            explanation = EndingSentence(words=words, morph=morph, tense=tense, type='ending', custom_word_parsed=cwp, context=context, min_seriousness=min_seriousness, max_seriousness=max_seriousness)
            word_list.append(explanation.word)
            word_list.append('.')
            

    word_list[0] = word_list[0].capitalize()

    return word_list



