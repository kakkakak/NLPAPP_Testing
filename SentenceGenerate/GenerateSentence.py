from nltk.corpus import stopwords
import string
from SentenceGenerate.UseMLM import get_mlm_word
from SentenceGenerate.UseWordNet import get_sys_word
from treelib import Tree, Node


punc = string.punctuation


class GenerateSentence:
    def __init__(self, word_pos, adjuncts, parameter):
        self.__WordsPos = word_pos
        self.__Adjuncts = adjuncts
        self.__DerivationTree = Tree()
        self.__Parameter = parameter  # sys   mlm

    def generate_sentence(self):
        derivation_dict = self.__get_seed()
        s = self.__sentence_dict_to_string(derivation_dict)
        root_node = Node(identifier='root', data=s)
        self.__DerivationTree.add_node(root_node)
        self.__find_substitute(derivation_dict, 1, root_node)
        return self.__DerivationTree

    def __find_substitute(self, derivation_dict, index, parent_node):
        if index > len(self.__Adjuncts):
            return
        adjunct = self.__Adjuncts[index - 1]
        for word_id in adjunct:
            derivation_dict.update({word_id: self.__get_word(word_id)})
        substitute_list = self.__identify_substitute(adjunct)  # 找到当前修饰语的替换单词列表
        if self.__Parameter == 0:
            substitute_list.clear()
        if not substitute_list:
            # add original adjunct
            s = self.__sentence_dict_to_string(derivation_dict)
            node = Node(data=s)
            self.__DerivationTree.add_node(node, parent=parent_node)
            self.__find_substitute(derivation_dict, index + 1, node)
        else:
            with_original = 0
            time_original = 0
            for substitute_id in substitute_list:
                derivation_dict_new = derivation_dict.copy()
                original_word = derivation_dict_new[substitute_id]
                # substitute_word_list = []
                if self.__Parameter == 'sys':
                    word = self.__get_word(substitute_id)
                    pos = self.__get_pos(substitute_id)
                    substitute_word = get_sys_word(word, pos)
                elif self.__Parameter == 'mlm':
                    derivation_dict_new.update({substitute_id: "[MASK]"})
                    masked_str = self.__sentence_dict_to_string(derivation_dict_new)
                    (with_original, substitute_word) = get_mlm_word(masked_str, original_word)
                else:
                    raise Exception('Wrong Parameter!')
                if with_original == 1 and time_original == 0:
                    derivation_dict_new[substitute_id] = original_word
                    s = self.__sentence_dict_to_string(derivation_dict_new)
                    node = Node(data=s)
                    self.__DerivationTree.add_node(node, parent=parent_node)
                    self.__find_substitute(derivation_dict_new.copy(), index + 1, node)
                    time_original = 1
                derivation_dict_new[substitute_id] = substitute_word
                s = self.__sentence_dict_to_string(derivation_dict_new)
                node = Node(data=s)
                self.__DerivationTree.add_node(node, parent=parent_node)
                self.__find_substitute(derivation_dict_new.copy(), index + 1, node)

    def __get_seed(self):
        seed = {}
        for index, word_pos in enumerate(self.__WordsPos):
            word_id = index + 1
            if self.__is_in_adjunct(word_id) == 0:
                seed.update({word_id: self.__get_word(word_id)})
        return seed

    def __is_in_adjunct(self, word_id):
        for adjunct in self.__Adjuncts:
            if word_id in adjunct:
                return 1
        return 0

    def __identify_substitute(self, slot):
        # noun verb adj adv (not in stopwords)
        substitute_list = []
        for word_id in slot:
            if self.__get_word(word_id) in stopwords.words('english'):
                continue
            elif self.__get_pos(word_id).startswith("NN"):
                substitute_list.append(word_id)
            elif self.__get_pos(word_id).startswith("VB"):
                substitute_list.append(word_id)
            elif self.__get_pos(word_id).startswith("JJ"):
                substitute_list.append(word_id)
            elif self.__get_pos(word_id).startswith("RB"):
                substitute_list.append(word_id)
        return substitute_list

    def __sentence_dict_to_string(self, derivation_dict):
        derivation_str = ""
        flag1 = 0
        flag2 = 0
        sentence = sorted(derivation_dict.keys())
        # 删除开始的‘,’
        while derivation_dict[sentence[0]] == ',':
            sentence.pop(0)
        for index, word_id in enumerate(sentence):
            word = derivation_dict[word_id]
            if word == ',' and index < len(sentence) - 1 and derivation_dict[sentence[index + 1]] in [',', '?', '.',
                                                                                                      '!', '...']:
                continue
            if word == '\'':
                flag1 += 1
            if word == '\"':
                flag2 += 1
            if self.__add_blank(word, word_id, flag1, flag2, index):
                derivation_str += " "
            derivation_str += word
        derivation_str = "".join(derivation_str[:1].upper() + derivation_str[1:])
        return derivation_str

    def __add_blank(self, word, word_id, flag1, flag2, index):
        if index == 0:
            return False
        if word == "n't":  # 分词会拆开n't缩写
            return False
        if word.startswith('\''):
            return False
        if word == '\'' and flag1 % 2 == 1:
            return True
        if word == '\"' and flag2 % 2 == 1:
            return True
        if word in punc:
            return False
        if self.__get_word(word_id - 1) in ['/', '-', '(']:
            return False
        if self.__get_word(word_id - 1) == '\'' and flag1 % 2 == 1:
            return False
        if self.__get_word(word_id - 1) == '\"' and flag2 % 2 == 1:
            return False
        return True

    def __get_word(self, word_id):
        return self.__WordsPos[word_id - 1][0]

    def __get_pos(self, word_id):
        return self.__WordsPos[word_id - 1][1]
