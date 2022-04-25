import pdfplumber
import pandas as pd
import pyparsing as pp
import networkx as nx
import matplotlib.pyplot as plt
import random

path_pdf = 'Lib/Curriculum.pdf'


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

    g_root = ["Модель навыков\nкибербезопасности"]

    g_categories = ["Безопасность\nсистем"]

    g_domains = ["Криптография\n(КР)"]

    g_modules = [
        "Математические\nосновы КР", "Модели\nКР защиты",
        "Симметричное\nшифрование и\nаутентификация", "Асимметричная\nкриптография",
        "Криптографические\nпротоколы"
    ]

    g_skills = [
        "Знание\nматематических\nоснов\nкриптографии", "Знание алгоритмов\nна основе\nэллиптических\nкривых",
        "Владение принципами\nпостроения и применения\nмоделей нарушителя",
        "Владение методами\nкриптографической защиты данных\nсимметричными механизмами",
        "Владение методами\nассиметричного шифрования\n и электронной подписи",
        "Знание основных типов\nкриптографических протоколов"
    ]

    data = [
        [g_root[0], g_categories[0]],
        [g_categories[0], g_domains[0]],
        [g_domains[0], g_modules[0]],
        [g_domains[0], g_modules[1]],
        [g_domains[0], g_modules[2]],
        [g_domains[0], g_modules[3]],
        [g_domains[0], g_modules[4]],
        [g_modules[0], g_skills[0]],
        [g_modules[0], g_skills[1]],
        [g_modules[1], g_skills[2]],
        [g_modules[2], g_skills[3]],
        [g_modules[3], g_skills[4]],
        [g_modules[4], g_skills[5]],
    ]

    modules_weights = [12, 8, 6, 6, 8]

    weights = {
        g_root[0]: 25, g_categories[0]: 20, g_domains[0]: 15
    }
    weights.update({g_modules[k]: modules_weights[k] for k in range(len(g_modules))})
    weights.update({g_skills[m]: 6 for m in range(len(g_skills))})

    attrs = {key: {"weight": val} for key, val in weights.items()}
    g = nx.Graph()
    g.add_edges_from(data)
    pos = hierarchy_pos(g, g_root[0])
    nx.set_node_attributes(g, attrs)
    node_size = [a["weight"] * 600 for n, a in g.nodes(data=True)]
    fig, ax = plt.subplots(figsize=(20, 20))
    nx.draw(g, pos=pos, edgecolors='lightgrey', node_color='lightyellow', with_labels=True, node_size=node_size, ax=ax)


if __name__ == "__main__":

    # Открываем pdf-документ “Curriculum” с помощью pdfplumber,
    # копируем содержание страниц 4-7 в строку “content” для выделения категорий и доменов, закрываем документ

    content = ''
    with pdfplumber.open(path_pdf) as pdf:
        for i in range(4, 7):  # (len(pdf.pages)):
            page = pdf.pages[i]
            page_content = '\n'.join(page.extract_text().split('\n')[:-1])
            content = content + page_content
    pdf.close()

    # С помощью синтаксического анализа текста на основе формальной грамматики и регулярных выражений
    # выделяем названия категорий и подкатегорий и записываем их в строковые массивы "categories" и "domains"
    # для хранения категорий и доменов соответственно

    categories = []
    domains = []

    rus_alphas = 'йцукенгшщзхъфывапролджэячсмитьбюЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮ'
    rus_alphas_big = 'ЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮ'

    category_name = pp.Word(pp.alphas + rus_alphas + ' ' + ',' + '-')
    end_of_cat = pp.Regex(r"[\(-a-z»]")
    parse_cat = 'Категория «' + category_name + end_of_cat
    for tokens in parse_cat.searchString(content):
        categories.append(tokens[1])
        # print(tokens)

    domain_name = pp.Word(rus_alphas + ' ' + ',' + pp.nums)
    end_of_dom = pp.Word(rus_alphas_big)
    dash = pp.Word('-' + '–')
    parse_dom = pp.Regex(r"[1-9]+\.[1-9]+\.") + domain_name + dash + end_of_dom
    for tokens in parse_dom.searchString(content):
        domains.append(tokens[1])
        # print(tokens)

    content = ''
    with pdfplumber.open(path_pdf) as pdf:
        page = pdf.pages[60]
        tables = page.extract_tables()
        for table in tables:
            df = pd.DataFrame(table)
            print(df)

    pdf.close()

    keyword_skill = pp.Word("Навыки-цели")
    # до "/"

    print(categories, "\n", len(categories))
    print(domains, "\n", len(domains))

    """
    Категории свода знаний специальности кибербезопасность categories = []

    Подкатегории-домены для каждой категории domains = []

    Модули доменов modules = []

    Темы-результаты модулей results = []

    Навыки-цели skills = []

    Рисуем граф graph()
    
    plt.show()
    """

    graph()

    plt.show()
