
import math


class converter():

    #Number of gas unit for the simplest transaction (e.g. transfering eth between two wallets)
    gasTransactionUnit = 21000

    """
    _ethEUR is the given value of one eth in EUR
    _gasPrice is how many Gwei you are willing to pay per gas Unit
    """
    def __init__(self, _ethEUR,_gasPrice = 54.65733):
        self.ethEUR = _ethEUR
        self.gasPrice = _gasPrice
    
    def EURperGas(self,_usedGas):
        eur = _usedGas*(self.gasPrice)*10**-9*self.ethEUR

        return math.ceil(eur)

    def min(self,_arr):
        c = []
        for idx,el in enumerate(_arr):
            if idx < len(_arr)-1:
                c.append(_arr[idx+1]-el)
        
        return c


c = converter(3117.467)

gasUnit_forDeploy = 1529555
gasUnit_addOneRes = 49272
gasUnit_Ten= 347220
one = [78130,
63118,
63130,
63130,
63118,
63130,
63130,
63130,
63130,
63130,
63118,
63130,
63130,
63130,
63118,
63130,
63118,
63106,
63130,
63130,
63118,
63118,
63118,
63130,
63130,
63130,
63118,
63130,
63130,
63130,
63118,
63130,
63118,
63118,
63130,
63130,
63118,
63094,
63130,
63118,
63130,
63118,
63130,
63130,
63130,
63118,
63130,
63130,
63130,
63130,
63130,
63130,
63130,
63130,
63130,
63118,
63118,
63130,
63130,
63130,
63130,
63118,
63130,
63130,
63130,
63130,
63130,
63118,
63130,
63130,
63130,
63130,
63130,
63118,
63130,
63130,
63118,
63130,
63118,
63130,
63130,
63130,
63118,
63130,
63130,
63130,
63130,
63118,
63130,
63130,
63130,
63130,
63130,
63130,
63130,
63118,
63130,
63130,
63130,
63130]
ten = [
311311,
296275,
296287,
296239,
296311,
296311,
296311,
296299,
296311,
296323,
]
fifty = [
1347620,
1332752
]


#print(round(sum(res),3))

#print(c.min(one))

#print(c.EURperGas(1529555))

res = []
for idx,el in enumerate(fifty):
    res.append(c.EURperGas(el))

print("{},{}".format(sum(res),sum(fifty)))


res = []
for idx,el in enumerate(ten):
    res.append(c.EURperGas(el))
print("{},{}".format(sum(res),sum(ten)))


res = []
for idx,el in enumerate(one):
    res.append(c.EURperGas(el))
print("{},{}".format(sum(res),sum(one)))