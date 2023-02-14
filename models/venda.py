from models.database import Dao
from datetime import datetime 
import math

class Venda():
    
    def __init__(self):
        self.ValorTotal = 0.00
        self.itens = []
        self.DAO = Dao()
        self.codigoVenda = 0
        self.dataAtual = datetime.today().strftime('%Y-%m-%d')
        
    def Arrendondar(self, num):
        #Pega a parte inteira
        intPart = int(num)
        #Pega a parte decimal
        decPart = num % 1
        
        #Arrendonda para mais se estiver entre 0.3 e 0.4
        if decPart < 0.5 and decPart > 0.2:
            decPart = 0.5
        #Arrendonda para menos se for igual a 0.6  
        elif decPart > 0.5 and decPart < 0.7:
            decPart = 0.5
        #Arrendonda para mais se estiver entre a 0.7 e 0.99
        elif decPart > 0.6:
            decPart = 1
        #Arrendonda para menos se estiver entre 0.1 e 0.2
        elif decPart < 0.3:
            decPart = 0.0
        
        return(intPart + decPart)    
        
    
    def CalculaTotal_Venda(self):
        self.ValorTotal = 0.00
        if len(self.itens) > 0:
            for i in self.itens:
                self.ValorTotal += self.Arrendondar(float(i['valor_prato']))
        
    def AddItenVenda(self, peso, valor_prato, valor_kg):
        item = {'peso': peso, 
                'valor_prato': float(valor_prato.replace("R$ ", "").replace(',', '.')),
                'valor_kg': valor_kg }
        
        self.itens.append(item)
        return item

    def SalvarVenda(self):
        self.CalculaTotal_Venda()
        
        #formatar parametros e executar o insert
        #hoje = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
        
        parms = (self.dataAtual , round(self.ValorTotal , 2))
        sql = "INSERT INTO vendas ('data_venda', 'valor_venda') VALUES (?, ?)"
        self.DAO.executar(sql, parms)
        
        self.codigoVenda = self.DAO.getID()
        
        for it in self.itens:
            parms = (self.codigoVenda, it['peso'], it['valor_prato'], it['valor_kg'])
            sql = """INSERT INTO itens_vendas (
                             codigo_venda,
                             peso_prato,
                             valor_prato,
                             valor_kilo
                         )
                         VALUES (?,?,?,?);"""
            self.DAO.addSQL(sql, parms)

        self.DAO.executarCommit()
       
        
    def AlterarVenda(self):
        pass
    
    def AtualizarVenda(self):
        pass
    
    def ExcluirVenda(self):
        pass