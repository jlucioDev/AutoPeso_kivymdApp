from models.database import Dao

class Caixa():
    
    def __init__(self):
        self.data = ""
        self.valorEntrada = 0.00
        self.valorDinheiro = 0.00
        self.valorDebito = 0.00
        self.valorCredito = 0.00
        self.valorPix = 0.00
        self.DAO = Dao()
        
    def NovoCaixa():
        pass