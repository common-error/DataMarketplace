from itertools import count
import networkx as nx,random
import json
import matplotlib.pyplot as plt
from random import choice
from networkx.readwrite import json_graph

class GDV():

    def __init__ (self,_numLabels,_maxNodesXlabel,_seed=0):
        self.labels = {}
        for idx,label in enumerate(range(_numLabels)):
            numNodes = random.randint(2,_maxNodesXlabel)
            name = "label{}".format(idx)
            self.labels[name] = nx.random_tree(n=numNodes, seed=_seed)
            node_list = list(self.labels[name].nodes())
            count_dict = { k:{'resources':[]} for k in node_list}
            nx.set_node_attributes(self.labels[name], count_dict)

    def populate(self,_numResources):
        for res in range(_numResources):
            keys = list(self.labels.keys())
            random_idx = [keys[idx] for idx in self._randomIdx(len(keys))]
            
            for idx in random_idx:
                random_node = random.choice(list(self.labels[idx].nodes()))
                resources = self.labels[idx].nodes()[random_node]['resources']
                resources.append(res)
                self.labels[idx].nodes()[random_node]['resources'] = resources

        

    def show(self):
        #[print(nx.forest_str(tree)) for tree in self.labels.values()]
        [print(json.dumps(json_graph.node_link_data(tree),indent=2)) for tree in self.labels.values()]
    
    def save(self):
        keys = list(self.labels.keys())
        out = json.dumps({ key:json_graph.node_link_data(self.labels[key]) for key in keys})
        with open('GDV.json', 'w') as f:
            f.write(out)
    
    def _randomIdx(self, _len):
        return random.sample(range(_len),random.randint(0,_len))
            


gdv = GDV(2,30)
gdv.populate(50)
gdv.save()