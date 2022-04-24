import pdfplumber as pp
import networkx as nx
import matplotlib.pyplot as plt

path_pdf = 'Lib/Curricula.pdf'


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

    for i in range(len(categories)):
        for j in range(len(domains)):
            data[(i+1)*j] = [categories[i], domains[j]]

    weights = {
        categories[0]: 16,
        domains[0]: 8, domains[1]: 8, domains[2]: 8, domains[3]: 8
    }
    attrs = {key: {"weight": val} for key, val in weights.items()}
    g = nx.Graph()
    g.add_edges_from(data)
    nx.set_node_attributes(g, attrs)
    node_size = [a["weight"] * 600 for n, a in g.nodes(data=True)]
    fig, ax = plt.subplots(figsize=(10, 10))
    nx.draw(g, with_labels=True, node_size=node_size, ax=ax)


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
