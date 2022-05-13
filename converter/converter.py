
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
one = [
74366,
59354,
59366,
59366,
59354,
59366,
59366,
59366,
59366,
59366,
59354,
59366,
59366,
59366,
59354,
59366,
59354,
59342,
59366,
59366,
59354,
59354,
59354,
59366,
59366,
59366,
59354,
59366,
59366,
59366,
59354,
59366,
59354,
59354,
59366,
59366,
59354,
59330,
59366,
59354,
59366,
59354,
59366,
59366,
59366,
59354,
59366,
59366,
59366,
59366,
59366,
59366,
59366,
59366,
59366,
59354,
59354,
59366,
59366,
59366,
59366,
59354,
59366,
59366,
59366,
59366,
59366,
59354,
59366,
59366,
59366,
59366,
59366,
59354,
59366,
59366,
59354,
59366,
59354,
59366,
59366,
59366,
59354,
59366,
59366,
59366,
59366,
59354,
59366,
59366,
59366,
59366,
59366,
59366,
59366,
59354,
59366,
59366,
59366,
59366]
ten = [
294895,
279859,
279871,
279823,
279895,
279895,
279895,
279883,
279895,
279907
]
fifty = [
1274872,
1260004
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