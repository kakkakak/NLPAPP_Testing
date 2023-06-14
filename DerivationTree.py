import TemplateCreate.CreateTemplate as ct
from SentenceGenerate.GenerateSentence import GenerateSentence
from treelib import Tree
import argparse


def get_derivation_tree(sent, parameter):
    #parameter sys or mlm
    (word_pos, adjuncts) = ct.create_template(sent)
    if not adjuncts:
        print("未提取出修饰语！")
        return -1
    print("修饰语集合: ", adjuncts)
    derivation_tree = GenerateSentence(word_pos, adjuncts, parameter).generate_sentence()
    return derivation_tree


def save_from_tree(write_file, sent_id, derivation_tree):
    f = open(write_file, mode='a', encoding='utf-8')
    f.write("sent_id = {}\n".format(sent_id))
    f.write(derivation_tree['root'].data+'\n')
    step_list = []
    if derivation_tree.is_branch('root'):
        step_list.append(derivation_tree.is_branch('root'))
    step_index = 0
    while step_list:
        f.write("add [{}]\n".format(step_index))
        next_step_list = []
        for group_list in step_list:
            for node in group_list:
                f.write(derivation_tree[node].data+'\n')
                if derivation_tree.is_branch(node):
                    next_step_list.append(derivation_tree.is_branch(node))
            f.write('\n')
        step_list = next_step_list
        step_index += 1
    f.write('FIN\n')
    f.close()


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--file-name',
                        default='ssm')
    parser.add_argument('--Mtype',
                        default='mlm')
    return parser.parse_args()


def main():
    args = parse_args()
    file_name = args.file_name
    mtype = args.Mtype
    seed_file = './Data/Seeds/' + file_name + '.txt'
    tree_file = './Data/DerivationTree/' + file_name + '_pred' + '.txt'
    f = open(seed_file, mode='r', encoding='utf-8')
    line = f.readline()
    while line:
        id_sent = line.split('\t')
        print("sent_id = {}".format(id_sent[0]))
        derivation_tree = get_derivation_tree(id_sent[1], mtype)
        if derivation_tree != -1:
            save_from_tree(tree_file, id_sent[0], derivation_tree)
        print('\n')
        line = f.readline()
    f.close()


if __name__ == '__main__':
    main()











