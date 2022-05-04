



class converter():

    #Number of gas unit for the simplest transaction (e.g. transfering eth between two wallets)
    gasTransactionUnit = 21000

    """
    _ethEUR is the given value of one eth in EUR
    _gasPrice is how many Gwei you are willing to pay per gas Unit
    """
    def __init__(self, _ethEUR,_gasPrice = 55):
        self.ethEUR = _ethEUR
        self.gasPrice = _gasPrice
    
    def EURperGas(self,_transactionCost):
        eur = _transactionCost*(self.gasPrice)*10**-9*self.ethEUR

        return "{} euro".format(round(eur,4))


c = converter(2665)

gasUnit_forDeploy = 1529555
gasUnit_addOneRes = 49272
gasUnit_Ten= 347220


print("Deploy contract price: {}".format(c.EURperGas(gasUnit_Ten)))