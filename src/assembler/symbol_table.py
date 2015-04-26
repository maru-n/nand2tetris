class SymbolTable(object):
    """docstring for SymbolTable"""
    def __init__(self):
        super(SymbolTable, self).__init__()
        self.__table = {}

    def add_entry(self, symbol, address):
        self.__table[symbol] = address
        return

    def contains(self, symbol):
        return symbol in self.__table

    def get_address(self, symbol):
        if self.contains(symbol):
            return self.__table[symbol]
        else:
            return None

    def __str__(self):
        return str(self.__table)
