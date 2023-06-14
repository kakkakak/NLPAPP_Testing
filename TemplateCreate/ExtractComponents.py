import nltk
import networkx as nx


def find_SBAR(data, tree, depth):
    if (tree.label() == "SBAR") and depth > 1:
        path = []
        for leaf in tree.leaves():
            path.append(data.get_leaf(leaf, "id"))
        if path not in data.SBAR:
            data.SBAR.append(path)
    for subtree in tree:
        if type(subtree) == nltk.tree.Tree:
            find_SBAR(data, subtree, depth+1)


def extract_from_constituency_tree(data):
    tree = data.NewConstituencyTree
    find_SBAR(data, tree, 0)
    print("从句:{}".format(data.show_component(data.SBAR)))


def path_from_core(data, core):
    path = list(nx.dfs_preorder_nodes(data.NewDependencyTree, source=core))
    path.sort()
    return path


def find_components(data):
    for dep in data.DependencyTree:
        path = path_from_core(data, dep[2])
        if (dep[0] == "obl" or dep[0] == "nmod") and data.get_pos(path[0]) == "IN":
            data.PP.append(path)
        elif (dep[0] == "advmod" and data.get_pos(dep[2]) != "WRB") or dep[0] == "obl:tmod":
            data.ADV.append(path)
        elif dep[0] == "amod":
            data.ADJ.append(path)
        elif (dep[0] == "advcl" or dep[0] == "acl") and path not in data.SBAR:
            if data.get_pos(path[0]) == "IN":
                data.PP.append(path)
            elif dep[0] == "advcl":
                data.ADV.append(path)
            elif dep[0] == "acl":
                data.ADJ.append(path)


def extract_from_dependency_tree(data):
    find_components(data)
    print("介词短语:{}".format(data.show_component(data.PP)))
    print("形容词:{}".format(data.show_component(data.ADJ)))
    print("副词:{}".format(data.show_component(data.ADV)))


def extract_components(data):
    extract_from_constituency_tree(data)
    extract_from_dependency_tree(data)



