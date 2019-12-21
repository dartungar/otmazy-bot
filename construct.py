# one function to rule them all
# one function to find them
# one to arrange them all
# and in the sentence bind them
from words_stupid import Subject, Predicate, PredicateSpice, Noun, NounSpice, Object, Adverbial, Beginning, EndingSentence
from helpers import declensify, get_rules, needs_capitalizing
import random


def constructor(words, morph, tense='futr', context='default', 
                min_seriousness=None,
                max_seriousness=None,
                subject_is_myself=True, 
                subj_datv=False, 
                has_predicate_spice=True, 
                to_be=False, 
                has_beginning=False, 
                has_ending=False):
    
    word_list = []

    # subject
    subject = Subject(words=words, morph=morph, subject_is_myself=subject_is_myself, datv=subj_datv, min_seriousness=min_seriousness, max_seriousness=max_seriousness)

    word_list.append(subject.word)

    # predicate spice
    # TODO: этой поебени сильно нужен реворк! возможно, в таблицу соответствий
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
    
    word_list.append(predicate_spice)
    

    # predicate
    predicate = Predicate(words=words, morph=morph, tense=tense, aspc=pred_aspc, min_seriousness=min_seriousness, max_seriousness=max_seriousness)

    # TODO: переработать блок сказуемого чтобы не было нужды в этой хуйне
    rules = get_rules(words, predicate)


    # склоняем сказуемое, если нет спайса
    if not predicate_spice:
        if pred_aspc == 'perf' or tense == 'past':
            predicate.parsed = declensify(morph, predicate.parsed, tags=[subject.person, subject.plural, subject.gender], tense=tense)
        else:
            predicate.parsed = declensify(morph, predicate.parsed, tags=[subject.person, subject.plural, subject.gender])
        predicate.word = predicate.parsed.word

    word_list.append(predicate.word)
    #print(predicate.parsed)

    word1 = ''
    word1_predlog = ''
    #word1_spice = ''
    if rules.word1.iloc[0]:
        word1 = Noun(words=words, morph=morph, noun_type=rules.word1_type.iloc[0], case=rules.word1_case.iloc[0], min_seriousness=min_seriousness, max_seriousness=max_seriousness)
        #print(word1.word)

        if rules.word1_predlog.iloc[0]:
            word1_predlog = rules.word1_predlog.iloc[0]
            word_list.append(word1_predlog)
        # has_word1_spice = random.randint(0, 1)
        # if has_word1_spice:
        #     word1_spice = NounSpice(words, morph, word1.parsed)
        #     if word1_spice.word:
        #         word1_spice = declensify(morph, word1_spice.parsed, tags=['ablt', word1.plural, word1.gender]).word
        word_list.append(word1.word)

    word2 = ''
    word2_predlog = ''
    #word2_spice = ''
    if rules.word2.iloc[0]:
        # word2
        word2 = Noun(words=words, morph=morph, noun_type=rules.word2_type.iloc[0], case=rules.word2_case.iloc[0], min_seriousness=min_seriousness, max_seriousness=max_seriousness)

        # predlog
        if rules.word2_predlog.iloc[0]:
            word2_predlog = rules.word2_predlog.iloc[0]
            word_list.append(word2_predlog)

        # has_word2_spice = random.randint(0, 1)
        # if has_word2_spice:
        #     word2_spice = NounSpice(words, morph, word2.parsed)
        #     # TODO: проверить, актуально для второго слова такие теги
        #     if word2_spice.word:
        #         word2_spice = declensify(morph, word2_spice.parsed, tags=['ablt', word2.plural, word2.gender]).word
        word_list.append(word2.word)


    # beginning
    beginning = ''
    if has_beginning:
        beginning = Beginning(words=words, morph=morph, min_seriousness=min_seriousness, max_seriousness=max_seriousness).word
        #beginning = declensify_text(morph, beginning, subject, tense, context)
        word_list.insert(0, beginning)

    word_list.append('.')
    
    # новый ending!
    end_sentence = ''
    cwp = None
    if has_ending:
        has_cwp = random.randint(0, 1)
        if has_cwp:
            if subject.is_myself == False:
                cwp = subject.parsed
            elif word1:
                cwp = word1.parsed
            else:
                cwp = word2.parsed
        end_sentence = EndingSentence(words=words, morph=morph, tense=tense, type='ending', custom_word_parsed=cwp, min_seriousness=min_seriousness, max_seriousness=max_seriousness)
        #print(end_sentence.word)
        word_list.append(end_sentence.word.capitalize())
        word_list.append('.')

    word_list[0] = word_list[0].capitalize()

    return word_list

