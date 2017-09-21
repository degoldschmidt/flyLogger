class Collection(object):
    def __init__(self):
        self.df
        

    def __str__(self):
        return self.df

class Stock(object):
    def __init__(self, data):
        self.stock_id = None
        self.stock_name = None
        self.tray_name = None
        self.owner = None
        self.source = None
        self.added = None
        self.chr_1 = (None, None)
        self.chr_2 = (None, None)
        self.chr_3 = (None, None)
        self.comments = None
        self.state = None

    def __str__(self):
        return """
-----------
{} ({})
-----------
Owner:\t{}
Source:\t{}
Added:\t{}
-----------
Full genotype:
{}/{}; {}/{}; {}/{}
-----------
State: {}
-----------
Comments: {}
              """.format(
                            self.stock_name,
                            self.stock_id,
                            self.owner,
                            self.source,
                            self.added,
                            self.chr_1[0],
                            self.chr_2[0],
                            self.chr_3[0],
                            self.chr_1[1],
                            self.chr_2[1],
                            self.chr_3[1],
                            self.state,
                            self.comments
                         )
class Vial(object):
    def __init__(self):
        pass

if __name__ == "__main__":
    stock = Stock()
    print(stock)
