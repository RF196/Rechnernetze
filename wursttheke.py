class Wursttheke:
   def __init__(self, wurstsorten: str, preis: float):
        self.wurstsorten = wurstsorten
        self.preis = preis


wurst_theke = Wursttheke("salami", 300)

def plus(a, b):
    return a + b


a = plus(3,7)
print(a)