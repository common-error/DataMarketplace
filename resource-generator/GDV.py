from itertools import count
import networkx as nx,random
import json
from random import choice
from networkx.readwrite import json_graph
from os.path import exists
import pyparsing as pp
import re

DEFAULTFILE = 'GDV.json'

class UnaryOperation(object):
    def __init__(self, tokens):
        self.op, self.operands = tokens[0]
        st = str(tokens[0][1])
        self.label = st[st.index("[")+1:st.index("]")]

class BinaryOperation(object):
    def __init__(self, tokens):
        self.op = tokens[0][1]
        self.operands = tokens[0][0::2]

class SearchNot(UnaryOperation):
    def __repr__(self):
        return 'set().union(*[set(el) for el in nx.get_node_attributes(self.labels[{0}],"resources").values() if len(el) > 0]) - {1}'.format(self.label,self.operands)

class SearchAnd(BinaryOperation):
    def __repr__(self):
        return '(' + ' & '.join(['{}'.format(oper) for oper in self.operands]) + ')'

class SearchOr(BinaryOperation):
    def __repr__(self):
        return '(' + ' | '.join(['{}'.format(oper) for oper in self.operands]) +')'

class SearchTerm(object):
    def __init__(self, tokens):
        self.term = tokens[0]

    def __repr__(self):
        'instead of just the  term, we represent it as TAGS[term]'
        return 'set(self.labels[\'{0}\'].nodes()[{2}]["resources"])'.format(self.term[0],self.term[1],self.term[2])

class GDV():

    def __init__(self):
        operator = pp.Regex("=").setName("operator")
        number = pp.Regex(r"[+-]?\d+(:?\.\d*)?(:?[eE][+-]?\d+)?")
        identifier = pp.Word(pp.alphas, pp.alphanums + "_")
        comparison_term = identifier | number 
        condition = pp.Group(comparison_term + operator + comparison_term)
        condition.setParseAction(SearchTerm)
        and_ = pp.CaselessLiteral("and")
        or_ = pp.CaselessLiteral("or")
        not_ = pp.CaselessLiteral("not")

        self.expr = pp.infix_notation(condition,[
                            (not_, 1, pp.opAssoc.RIGHT, SearchNot),
                            (and_, 2, pp.opAssoc.LEFT,SearchAnd),
                            (or_, 2, pp.opAssoc.LEFT, SearchOr),
                            ])





    def generate(self,_numLabels,_maxNodesXlabel,_seed=0):
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
        
    def load(self,_file=DEFAULTFILE):
        if(exists(_file)):
            self.labels = {}
            with open(_file,'r') as f:
                data = json.load(f)
                keys = list(data.keys())
                for key in keys:
                    self.labels[key] = json_graph.node_link_graph(data[key])
        else:
            print("file not found!")
    
    def _randomIdx(self, _len):
        return random.sample(range(_len),random.randint(0,_len))


    def search(self,_exprString):
        #return self.labels[_label].nodes()[_value]['resources']

        #return set().union(*[set(nx.get_node_attributes(self.labels['label0'],'resources')[el]) for el in list(nx.descendants(self.labels['label0'], 2)) if len(nx.get_node_attributes(self.labels['label0'],'resources')[el]) > 0])
        
        tokens = self.expr.parseString(_exprString)[0]
        return eval(str(tokens))
        
                


gdv = GDV()
#gdv.populate(50)
gdv.load()
print(gdv.search(input("Query: ")))
