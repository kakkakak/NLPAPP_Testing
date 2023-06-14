import nltk
#nltk.download('wordnet')
from nltk.corpus import wordnet
from random import choice
from pattern.text.en import pluralize, comparative, superlative, conjugate, lexeme

'''
NOUN:
NN - Noun, singular or mass
NNS - Noun, plural
NNP - Proper noun, singular
NNPS - Proper noun, plural

VERB:
VB - Verb, base form
VBD - Verb, past tense
VBG - Verb, gerund or present participle
VBN - Verb, past participle
VBP - Verb, non-3rd person singular present
VBZ - Verb, 3rd person singular present

ADJ:
JJ - Adjective
JJR - Adjective, comparative
JJS - Adjective, superlative


ADV:
RB - Adverb
RBR - Adverb, comparative
RBS - Adverb, superlative
'''


def get_sys_word(word, word_pos):
    pattern_stopiteration_workaround()
    sys_arr = []
    word_lemma = wordnet.morphy(word)
    if word_pos.startswith("NN"):
        sys_arr = wordnet.synsets(word_lemma, pos=wordnet.NOUN)
    elif word_pos.startswith("VB"):
        sys_arr = wordnet.synsets(word_lemma, pos=wordnet.VERB)
    elif word_pos.startswith("JJ"):
        sys_arr = wordnet.synsets(word_lemma, pos=wordnet.ADJ)
    elif word_pos.startswith("RB"):
        sys_arr = wordnet.synsets(word_lemma, pos=wordnet.ADV)
    sys_list = []
    for sys in sys_arr:
        sys_list.extend(sys.lemma_names())
    sys_list = list(filter(lambda x: x != word_lemma and '_' not in x, sys_list))
    sys_word = sys_list[0]
    sys_word_refine = refine_sys_word(word_pos, sys_word)
    return sys_word_refine


def refine_sys_word(word_pos, sys_word):
    # NOUN:复数
    if word_pos == "NNS" or word_pos == "NNPS":
        return pluralize(sys_word)
    # VERB:VBD过去式   VBZ动词第三人称单数  VBG现在分词  VBN过去分词
    elif word_pos == "VBD":
        return conjugate(sys_word, '3sgp')
    elif word_pos == "VBZ":
        return conjugate(sys_word, '3sg')
    elif word_pos == "VBG":
        return conjugate(sys_word, 'past')
    elif word_pos == "VBN":
        return conjugate(sys_word, 'ppast')
    # ADJ:  JJR——比较级    JJS——最高级
    elif word_pos == "JJR":
        return comparative(sys_word)
    elif word_pos == "JJS":
        return superlative(sys_word)
    else:
        return sys_word


def pattern_stopiteration_workaround():
    try:
        print(lexeme('gave'))
    except:
        pass



