import pdfplumber as pp
import networkx as nx
import matplotlib.pyplot as plt

path_pdf = 'Lib/Curricula.pdf'


def graph():
    data = [
        ["смотреть", "подолгу"], ["смотреть", "детьми"],
        ["подолгу", "спать"], ["подолгу", "сидеть"],
        ["спать", "сладко"], ["спать", "крепко"],
        ["детьми", "воспитывать"], ["детьми", "ухаживать"]
    ]
    weights = {
        'смотреть': 2, 'подолгу': 1.5, 'детьми': 1.5, 'спать': 1, 'сидеть': 1, 'сладко': 1,
        'крепко': 1, 'воспитывать': 1, 'ухаживать': 1
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
        for i in range(len(pdf.pages)):
            page = pdf.pages[i]
            page_content = '\n'.join(page.extract_text().split('\n')[:-1])
            content = content + page_content
    pdf.close()
    print(content)

    graph()
    plt.show()
