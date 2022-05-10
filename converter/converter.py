
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
one = [81635,
73108,
79581,
86054,
92528,
99002,
105476,
111951,
118426,
124901,
131389,
137865,
144341,
150818,
157294,
163772,
170249,
176727,
183205,
189684,
196162,
202641,
209121,
215601,
222081,
228561,
235042,
241523,
248004,
254485,
260967,
267450,
273932,
280415,
286898,
293382,
299866,
306350,
312834,
319319,
325804,
332290,
338775,
345261,
351748,
358234,
364721,
371209,
377696,
384184,
390672,
397161,
403650,
410139,
416629,
423119,
429609,
436099,
442590,
449081,
455572,
462064,
468556,
475049,
481541,
488034,
494528,
501021,
507515,
514010,
520504,
526999,
533494,
539990,
546486,
552982,
559478,
565975,
572472,
578970,
585467,
591965,
598464,
604963,
611462,
617961,
624461,
630961,
637461,
643961,
650462,
656964,
663465,
669967,
676469,
682972,
689474,
695978,
702481,
708985,
715501]
ten = [
320627,
370508,
435301,
500125,
564980,
629868,
694787,
759737,
824720,
889733,
954899
]
fifty = [
1383366,
1693029,
2018962
]


#print(round(sum(res),3))

#print(c.min(one))

#print(c.EURperGas(1529555))

res = []
for idx,el in enumerate(fifty):
    res.append(c.EURperGas(el))

print(sum(res))


res = []
for idx,el in enumerate(ten):
    res.append(c.EURperGas(el))
print(sum(res))


res = []
for idx,el in enumerate(one):
    res.append(c.EURperGas(el))
print(sum(res))