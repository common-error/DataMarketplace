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

class BinaryOperation(object):
    def __init__(self, tokens):
        self.op = tokens[0][1]
        self.operands = tokens[0][0::2]

class SearchNot(UnaryOperation):
    def __repr__(self):
        
        return 'set().union(*[res for label in self.labels.values() for res in nx.get_node_attributes(label,"resources").values() if len(res) > 0 ]) - {0}'.format(self.operands)

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
        if self.term[1] == "=":
            return 'set(self.labels[\'{0}\'].nodes()[{2}]["resources"])'.format(self.term[0],self.term[1],self.term[2])
        elif self.term[1] == '>':
            return "set().union(*[set(self.labels[\'{0}\'].nodes()[node]['resources']) for node in list(nx.descendants(self.labels[\'{0}\'],{2})) if len(self.labels[\'{0}\'].nodes()[node]['resources'])>0])".format(self.term[0],self.term[1],self.term[2])
        elif self.term[1] == '>=':
            return "set().union(*[set(self.labels[\'{0}\'].nodes()[node]['resources']) for node in list(nx.descendants(self.labels[\'{0}\'],{2})) if len(self.labels[\'{0}\'].nodes()[node]['resources'])>0] + self.labels[\'{0}\'].nodes()[{2}]['resources'])".format(self.term[0],self.term[1],self.term[2])

class GDV():

    def __init__(self):
        operator = pp.Regex(">=|>|=").setName("operator")
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




    """
    Procedure that can generate n (_numLabels) trees with a random number of nodes (max = _maxNodesXlabel)
    """
    def generate(self,_numLabels,_maxNodesXlabel,_seed=0):
        self.labels = {}
        for idx,label in enumerate(range(_numLabels)):
            numNodes = random.randint(2,_maxNodesXlabel)
            name = "label{}".format(idx)
            self.labels[name] = nx.random_tree(n=numNodes, seed=_seed)
            self.labels[name] = nx.DiGraph([(u,v) for (u,v) in self.labels[name].edges() if u<v])
            node_list = list(self.labels[name].nodes())
            count_dict = { k:{'resources':[]} for k in node_list}
            nx.set_node_attributes(self.labels[name], count_dict)

    """
    The procedure pseudo-randomly assigns labels to a resource, adding for each label the resource in question in a node. A label may not even be chosen
    """
    def populate(self,_numResources):
        for res in range(_numResources):
            keys = list(self.labels.keys())
            randomSet = []
            while(len(randomSet)==0):
                randomSet = self._randomIdx(len(keys))

            random_idx = [keys[idx] for idx in randomSet]
            
            for idx in random_idx:
                random_node = random.choice(list(self.labels[idx].nodes()))
                resources = self.labels[idx].nodes()[random_node]['resources']
                resources.append(res)
                self.labels[idx].nodes()[random_node]['resources'] = resources

        

    def show(self):
        [print("{}\n{}".format(key,nx.forest_str(self.labels[key]))) for key in self.labels.keys()]
        #[print(json.dumps(json_graph.node_link_data(tree),indent=2)) for tree in self.labels.values()]
    
    """
    This procedure save all the graphs describing the labels
    """
    def save(self):
        keys = list(self.labels.keys())
        out = json.dumps({ key:json_graph.node_link_data(self.labels[key]) for key in keys})
        with open('GDV.json', 'w') as f:
            f.write(out)

    """
    This procedure exports in json format all resources with randomly chosen labels
    """
    def exportResources(self):
        resources = []
        data = { 
            "data" : []
        }
        for label in self.labels.values():
            tmp = set().union(*[set(el) for el in nx.get_node_attributes(label,"resources").values() if len(el) > 0])
            resources.append(tmp)
       
        resources = set().union(*resources)

        for res in resources:
            resData = {
                "id" : str(res),
                "data" : str(bytes("risorsa "+str(res),"utf-8")),
                "metadata" : self._getMetadata(res)
            }
            data['data'].append(resData)

        with open('resources.json', 'w') as f:
            json.dump(data, f)
    
    def _getMetadata(self,_res):
        metadata = {}

        for label in self.labels.keys():
            tmpRes = [x for x,y in self.labels[str(label)].nodes(data=True) if _res in y['resources']]
            if len(tmpRes) > 0:
                tmpRes = str(tmpRes[0])
                metadata[str(label)] = tmpRes


        return metadata


        
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
        
        tokens = self.expr.parseString(_exprString)[0]
        return eval(str(tokens),{"self":self,"nx":nx})
        
                


gdv = GDV()

gdv.generate(20,200)
gdv.populate(10000)
gdv.save()

gdv.exportResources()
"""
gdv.load()
print(gdv.search(input("Query: ")))

#gdv.show()
"""
"""
##TESTING
print("Testing -> \t label0=0 \t\t\t{}".format(gdv.search("label0=0") == {20}))
print("Testing -> \t label0=2 or label1=10 \t\t{}".format(gdv.search("label0=2 or label1=10") == {11, 13, 15}))
print("Testing -> \t label0=2 and label1=10 \t{}".format(gdv.search("label0=2 and label1=10") == {11}))
print("Testing -> \t not (label0=2 or label1=10) \t{}".format(gdv.search("not (label0=2 or label1=10)") == {0, 1, 3, 4, 5, 6, 8, 9, 14, 16, 18, 20, 25, 26, 28}))
print("Testing -> \t label1>2 \t\t\t{}".format(gdv.search("label1>2") == {25, 3}))
print("Testing -> \t label1>=2 \t\t\t{}".format(gdv.search("label1>=2") == {25, 3}))
"""