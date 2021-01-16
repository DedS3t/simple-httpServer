

class requestObj:

    def __init__(self,params,method):
        self.params=params
        self.method=method

    def __str__(self):
        return self.method+" : "+str(self.params)