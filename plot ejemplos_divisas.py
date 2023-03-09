import networkx as nx
import matplotlib.pyplot as plt
import os

def plot_shortest_path(path):
    #print(path)
    positions = nx.circular_layout(G)
    
    nx.draw(G, pos=positions,
                node_color='lightblue',
                edge_color='gray',
                font_size=10,
                width=1, with_labels=True, node_size=40, alpha=0.45
           )
    
    short_path=nx.DiGraph()
    for i in range(len(path)-1):
        short_path.add_edge(path[i], path[i+1])
    
    nx.draw(short_path, pos=positions,
                node_color='lightblue',
                edge_color='dodgerblue',
                font_size=10,
                width =1.5, with_labels=True, node_size=40
           )


def plot_edges(texto ="", color= '0.2'):
    ax.annotate(texto,
                ha = 'center',
                xy=layout[edge[0]], xycoords='data',
                xytext=layout[edge[1]], textcoords='data',
                arrowprops=dict(arrowstyle="->", color= color,
                                shrinkA=20, shrinkB=20,
                                patchA=None, patchB=None,
                                connectionstyle="arc3,rad=-0.2",
                                ),
                )
# Graph data
names = ['JPY', 'USD', 'GBP']
positions = [(-1,0.5), (0, 1.5), (1,0.5)]
edges = [ ('JPY', 'USD'),('JPY', 'GBP'),('USD', 'GBP'),('USD', 'JPY'),('GBP', 'USD'),('GBP', 'JPY')]

# Matplotlib figure
plt.figure('My graph problem')

# Create graph
G = nx.MultiDiGraph(format='png', directed=True)



for index, name in enumerate(names):
    G.add_node(name, pos=positions[index])


labels = {}

layout = dict((n, G._node[n]["pos"]) for n in G.nodes())
nx.draw(G, pos=layout, with_labels=True, node_size=1500, font_size=13, alpha=0.6)
ax = plt.gca()
for edge in edges:
    if edge in (('JPY', 'USD'),('GBP', 'JPY'),('USD', 'GBP')):
        plot_edges(color= 'red')
    else:
        plot_edges()

numeros ={
            '100': (-0.5,1),
            '7,14e-3': (-0.1,0.7),
            '0,01': (-1,1),
            '0,625': (0.75,1),
            '140': (0,0.4),
            '1,6': (0.1,1),
            }
for text, pos in numeros.items():

    plt.annotate(text,pos,size=7,color="black")
plt.margins(0.5)
plt.grid()
print(os.getcwd())
plt.savefig('presentacion_ejemplo_arbitraje.pdf')
#plt.show()

