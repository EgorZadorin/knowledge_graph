import pdfplumber as pp
import networkx as nx
import matplotlib.pyplot as plt
import random

path_pdf = 'Lib/Curricula.pdf'


def _hierarchy_pos(g, root, width=1., vert_gap=0.2, vert_loc=0.0, xcenter=0.5, pos=None, parent=None):
    """
    see hierarchy_pos docstring for most arguments

    pos: a dict saying where all nodes go if they have been assigned
    parent: parent of this branch. - only affects it if non-directed
    """

    if pos is None:
        pos = {root: (xcenter, vert_loc)}
    else:
        pos[root] = (xcenter, vert_loc)
    children = list(g.neighbors(root))
    if not isinstance(g, nx.DiGraph) and parent is not None:
        children.remove(parent)
    if len(children) != 0:
        dx = width / len(children)
        nextx = xcenter - width / 2 - dx / 2
        for child in children:
            nextx += dx
            pos = _hierarchy_pos(g, child, width=dx, vert_gap=vert_gap,
                                 vert_loc=vert_loc - vert_gap, xcenter=nextx,
                                 pos=pos, parent=root)
    return pos


def hierarchy_pos(g, root=None, width=1., vert_gap=0.2, vert_loc=0, xcenter=0.5):
    """
    From Joel's answer at https://stackoverflow.com/a/29597209/2966723.
    Licensed under Creative Commons Attribution-Share Alike

    If the graph is a tree this will return the positions to plot this in a
    hierarchical layout.

    G: the graph (must be a tree)

    root: the root node of current branch
    - if the tree is directed and this is not given,
      the root will be found and used
    - if the tree is directed and this is given, then
      the positions will be just for the descendants of this node.
    - if the tree is undirected and not given,
      then a random choice will be used.

    width: horizontal space allocated for this branch - avoids overlap with other branches

    vert_gap: gap between levels of hierarchy

    vert_loc: vertical location of root

    xcenter: horizontal location of root
    """

    if not nx.is_tree(g):
        raise TypeError('cannot use hierarchy_pos on a graph that is not a tree')

    if root is None:
        if isinstance(g, nx.DiGraph):
            root = next(iter(nx.topological_sort(g)))  # allows back compatibility with nx version 1.11
        else:
            root = random.choice(list(g.nodes))

    return _hierarchy_pos(g, root, width, vert_gap, vert_loc, xcenter)


def graph():

    categories = ["Человеческие, организационные и нормативные аспекты"]

    domains = [
        "Управление рисками и непрерывностью бизнеса", "Юридические и нормативные аспекты ИБ",
        "Человеческие факторы в ИБ", "ИБ онлайн-деятельности"
    ]

    data = [
        [categories[0], domains[0]],
        [categories[0], domains[1]],
        [categories[0], domains[2]],
        [categories[0], domains[3]],
    ]

    weights = {
        categories[0]: 16,
        domains[0]: 8, domains[1]: 8, domains[2]: 8, domains[3]: 8
    }
    attrs = {key: {"weight": val} for key, val in weights.items()}
    g = nx.Graph()
    g.add_edges_from(data)
    pos = hierarchy_pos(g, categories[0])
    nx.set_node_attributes(g, attrs)
    node_size = [a["weight"] * 600 for n, a in g.nodes(data=True)]
    fig, ax = plt.subplots(figsize=(10, 10))
    nx.draw(g, pos=pos, with_labels=True, node_size=node_size, ax=ax)


if __name__ == "__main__":
    content = ''
    with pp.open(path_pdf) as pdf:
        for i in range(5, 7):  # (len(pdf.pages)):
            page = pdf.pages[i]
            page_content = '\n'.join(page.extract_text().split('\n')[:-1])
            content = content + page_content
    pdf.close()
    print(content)

    # Категории свода знаний специальности кибербезопасность categories = []

    # Подкатегории-домены для каждой категории domains = []

    # Модули доменов modules = []

    # Темы-результаты модулей results = []

    # Навыки-цели skills = []

    graph()
    plt.show()
