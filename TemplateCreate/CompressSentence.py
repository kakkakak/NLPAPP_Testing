class AdjunctsPriority:
    def __init__(self, data, component_dict):
        self.__data = data
        self.__component_dict = component_dict
        self.__adjuncts_priority = self.get_adjuncts_priority()

    def get_priority(self, component):
        return self.__adjuncts_priority[tuple(component)]

    def get_adjuncts_priority(self):
        adjuncts_priority = {}
        for attri, attri_list in self.__component_dict.items():
            for component in attri_list:
                priority = self.adjunct_priority(component, attri)
                adjuncts_priority.update({tuple(component): priority})
        return adjuncts_priority

    def adjunct_priority(self, component, attri):
        """
        :param component: 成分
        :param attri: 成分属性
        :return: 0——不是修饰语 1——是修饰语 2~暂时不是"""
        if attri == "SBAR":
            return self.is_adjunct_SBAR(component)
        elif attri == "PP":
            return self.is_adjunct_PP(component)
        elif attri == "ADV":
            return self.is_adjunct_ADV(component)
        elif attri == "ADJ":
            return self.is_adjunct_ADJ(component)

    def is_adjunct_SBAR(self, component):
        father_dep = self.__data.father_dependency(component)
        if father_dep[0] == "csubj":  # 主语从句
            return 0
        elif father_dep[0] == "ccomp" and self.__data.get_pos(father_dep[1]).startswith("VB"):  # 宾语/表语从句
            return 0
        elif self.SBAR_no_adjunct(component[0]):
            return 0
        return 1

    def SBAR_no_adjunct(self, word_id):
        word = self.__data.get_word(word_id)
        f = open("Tools/SBAR_no_adjunct.txt", mode='r', encoding='utf-8')
        line = f.readline()
        pre_words_list = []
        flag = 0
        while line:
            if line[0] == "[" and flag == 0:
                last_word = line[1:-2]
                if word == last_word:
                    flag = 1
            elif line[0] == "[" and flag == 1:
                break
            elif line[0] != "[" and flag == 1:
                pre_words = line.split(' ')
                pre_words_list.append(list(reversed(pre_words)))
            line = f.readline()
        f.close()
        if flag == 0:
            return False
        for pre_words_reverse in pre_words_list:
            len_pre_words = len(pre_words_reverse)
            if word_id < len_pre_words:
                return False
            for index, word in enumerate(pre_words_reverse):
                if self.__data.get_word(word_id - index - 1) != word:
                    return False
        return True

    def is_v_pp_phrase(self, verb_id, pp_start_id):
        if verb_id > pp_start_id:
            return False
        if self.__data.get_pos(verb_id) == "VBN":
            return False
        if self.__data.with_obj(verb_id):
            return False
        if verb_id + 1 == pp_start_id:
            return True
        index = verb_id + 1
        while index < pp_start_id:
            if self.__data.get_pos(index) != 'RP':
                return False
            index += 1
        return True

    def is_adjunct_PP(self, component):
        component_start_id = component[0]
        father_dep = self.__data.father_dependency(component)
        father_id = father_dep[1]
        father_pos = self.__data.get_pos(father_id)
        # 动介词不是修饰语：首先与动词相依存；判断是否是动介词
        if father_pos.startswith("VB") and self.is_v_pp_phrase(father_id, component_start_id):
            return 0
        # 与形容词具有依存关系的介词短语不是
        if father_pos.startswith("JJ"):
            return 2
        # 前面是'-'的介词短语不是
        if component_start_id > 1 and self.__data.get_word(component_start_id - 1) == '-':
            return 0
        # of引导的介词短语不是
        if self.__data.get_word(component_start_id) == "of":
            return 3
        return 1

    def is_adjunct_ADJ(self, component):
        if len(component) <= 3:
            return 0
        return 1

    def is_adjunct_ADV(self, component):
        if len(component) <= 3:
            return 4
        return 1


def create_component_dict(data):
    component_dict = {}
    component_dict.update({"SBAR": data.SBAR.copy()})
    component_dict.update({"PP": data.PP.copy()})
    component_dict.update({"ADV": data.ADV.copy()})
    component_dict.update({"ADJ": data.ADJ.copy()})
    return component_dict


def find_adjuncts_1(data, component_dict, priority):
    component_list = []  # (adjunct, attri)
    adjuncts_nsplit = []
    for attri, attri_list in component_dict.items():
        for component in attri_list:
            component_list.append(component)
    for component in component_list:
        if priority.get_priority(component) == 1:
            adjuncts_nsplit.append(component)    # adjuncts保存当前修饰语（未切分）
    return adjuncts_nsplit


def find_adjuncts_2(data, len_, priority):
    adjuncts_nsplit = []
    pp_list = data.PP.copy()
    pp_list.sort(key=lambda i: len(i), reverse=False)
    for component in pp_list:
        if priority.get_priority(component) == 2:
            adjuncts_nsplit.append(component)
    for component in pp_list:
        if priority.get_priority(component) == 3:
            adjuncts_nsplit.append(component)
    for component in data.ADV:
        if priority.get_priority(component) == 4:
            adjuncts_nsplit.append(component)
    return adjuncts_nsplit[0:min(len(adjuncts_nsplit), 2-len_)]


def split_adjuncts(adjuncts_nsplit):
    adjuncts = []
    if not adjuncts_nsplit:
        return
    adjuncts_nsplit.sort(key=lambda i: len(i), reverse=False)
    while adjuncts_nsplit:
        adjunct_min = adjuncts_nsplit.pop(0)
        adjuncts.append(adjunct_min)
        tmp_nsplit = adjuncts_nsplit.copy()
        for adjunct in tmp_nsplit:
            # 如果adjunct_min属于当前adjunct,切分,从adjunct_nsplit删除原来的并加入剩余切割部分
            if set(adjunct).issuperset(set(adjunct_min)):
                adjunct_left = list(set(adjunct).symmetric_difference(set(adjunct_min)))
                adjuncts_nsplit.remove(adjunct)
                if adjunct_left not in adjuncts_nsplit:
                    adjuncts_nsplit.append(adjunct_left)
        adjuncts_nsplit.sort(key=lambda i: len(i), reverse=False)
    adjuncts.sort(key=lambda i: i[0], reverse=False)
    return adjuncts


def compress_sentence(data):
    component_dict = create_component_dict(data)
    Priority = AdjunctsPriority(data, component_dict)
    adjuncts_nsplit = find_adjuncts_1(data, component_dict, Priority)
    len_ = len(adjuncts_nsplit)
    if len_ < 2:
        adjuncts_nsplit.extend(find_adjuncts_2(data, len_, Priority))
    adjuncts = split_adjuncts(adjuncts_nsplit)
    return adjuncts












