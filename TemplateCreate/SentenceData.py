from stanfordcorenlp import StanfordCoreNLP
from nltk.tree import *
import networkx as nx

nlp = StanfordCoreNLP(r'Tools\stanford-corenlp-4.5.4')


class SentenceData:
    def __init__(self, sentence):
        # corenlp
        self.Words = nlp.word_tokenize(sentence)
        self.WordsPos = nlp.pos_tag(sentence)
        self.ConstituencyTree = nlp.parse(sentence)
        self.DependencyTree = nlp.dependency_parse(sentence)
        # preprocess
        self.NewConstituencyTree = self.__preprocess_constituency_tree()
        self.NewDependencyTree = self.__preprocess_dependency_tree()
        # components
        self.SBAR = []
        self.PP = []
        self.ADV = []
        self.ADJ = []

    def get_word(self, word_id):
        return self.WordsPos[word_id-1][0]

    def get_pos(self, word_id):
        return self.WordsPos[word_id - 1][1]

    '''
    Constituency Tree：
    '''
    def __preprocess_constituency_tree(self):
        # 预处理将corenlp得到的句法树存储在nltk.tree结构中（叶子节点为 word|id ）
        new_tree = ""
        word_id = 0
        mark_before = ""
        for mark in self.ConstituencyTree:
            if mark == ')' and mark_before != ")":
                word_id = word_id+1
                new_tree += "|"
                new_tree += str(word_id)
            new_tree += mark
            mark_before = mark
        tree = Tree.fromstring(new_tree.replace('\xa0', ''))
        return tree

    @staticmethod
    def get_leaf(leaf, tag):
        # tag=word ——获取叶子结点的单词      tag=id ——获取叶子节点在整个句子中的序号id
        if tag == "word":
            return str(leaf.split("|")[0])
        elif tag == "id":
            return int(leaf.split("|")[1])

    '''
    Dependency Tree:
    '''
    def __preprocess_dependency_tree(self):
        tree = nx.DiGraph()
        tree.add_node(0)
        for index, word_pos in enumerate(self.WordsPos):
            tree.add_node(index + 1, word=word_pos[0])
        for dep in self.DependencyTree:
            tree.add_edge(dep[1], dep[2], label=dep[0])
        return tree

    def father_dependency(self, component):
        # component:成分短语
        for dep in self.DependencyTree:
            if dep[1] not in component and dep[2] in component:
                return dep

    def with_obj(self, verb_id):
        for dep in self.DependencyTree:
            if dep[1] == verb_id and dep[0] == "obj":
                return True
        return False

    '''
    Show:
    '''
    def show_component(self, component_list):
        for component in component_list:
            component_str = ""
            for word_id in component:
                component_str += str(self.get_word(word_id)) + "|" + str(word_id) + "  "
            return component_str

