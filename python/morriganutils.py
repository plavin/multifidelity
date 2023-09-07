import sst
#import networkx as nx
#import matplotlib
#import matplotlib.pyplot as plt
#matplotlib.use("Agg")

component_count = {}
#build = False
#graph = nx.Graph()

#def build_graph():
#    build = True

#def get_graph(filename='graph.png'):
#    f = plt.figure()
#    nx.draw(graph, ax=f.add_subplot(111))
#    f.savefig(filename)

#def anon(component):
#    if component in component_count:
#        num = component_count[component]
#        component_count[component] = num + 1
#    else:
#        num = 0
#        component_count[component] = 1
#
#    name = "anon_" + component + "_" + str(num)
#    return sst.Component(name, component)

def mk(comp, params):
      comp.addParams(params)
      return comp

def clean(string):
      return string.replace('[','').replace(']','').replace(':','')

def mklink(e1, e2):
      e10 = clean(e1[0].getFullName())
      e20 = clean(e2[0].getFullName())
      e11 = clean(e1[1])
      e21 = clean(e2[1])
      linkname = f'link_{e10}__{e11}__{e20}__{e21}'
      link = sst.Link(linkname)
      link.connect(e1, e2)
      return link

