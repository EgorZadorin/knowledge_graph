import pdfplumber as pp
import networkx as nx
import matplotlib.pyplot as plt

path_pdf = 'Lib/Curricula.pdf'

if __name__ == "__main__":
    with pp.open(path_pdf) as pdf:
        print(pdf.pages)
        print()
        page = pdf.pages[2]
        table = page.extract_table()
        print(table)
        print()
        text = page.extract_text()
        print(text)
        print()

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

    G = nx.Graph()
    G.add_edges_from(data)
    nx.set_node_attributes(G, attrs)
    node_size = [a["weight"] * 600 for n, a in G.nodes(data=True)]
    fig, ax = plt.subplots(figsize=(10, 10))
    nx.draw(G, with_labels=True, node_size=node_size, ax=ax)

    plt.show()
