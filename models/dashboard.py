from models.database import Dao
from datetime import datetime


class Dashboard():

    def __init__(self, data = str(datetime.today().date())):
        self.DAO = Dao()
        self.VendasTotal = 0.00
        self.VendasQtde = 0
        self.VendasKg = 0.00
        self.DataAtual = data
    
    def getTotais(self):
        #Pega o total de vendas em reais
        sql = ''' SELECT sum(valor_venda) FROM vendas WHERE date(data_venda) = (?) '''
        parms = (self.DataAtual,)
        #parms = ('2022-06-17',)
        
        c = self.DAO.executar(sql, parms)
        self.VendasTotal = c[0][0] if c[0][0] != None else 0
        
        #Pega o total de vendas em quantidades de pratos
        sql = '''SELECT count(codigo_venda) FROM vendas WHERE date(data_venda) = (?) '''
        c = self.DAO.executar(sql, parms)
        self.VendasQtde = c[0][0] if c[0][0] != None else 0
        
        #Pega o total de vendas em kilos
        sql = '''SELECT sum(peso_prato)
                FROM itens_vendas
                INNER JOIN vendas on itens_vendas.codigo_venda = vendas.codigo_venda
                WHERE date(data_venda) = (?)'''
        c = self.DAO.executar(sql, parms)
        self.VendasKg = c[0][0] if c[0][0] != None else 0
        