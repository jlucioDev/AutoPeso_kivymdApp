from models.database import Dao


class Relatorio():
    
    def __init__(self):
         self.DAO = Dao()
         
    def getRelatorio(self, data):
        
        sql ="""SELECT tipo_pgto,
                        sum(valor_pgto)
                FROM vendas
                INNER JOIN pagamentos 
                on vendas.codigo_venda = pagamentos.codigo_venda
                WHERE STRFTIME('%Y-%m-%d', vendas.data_venda) = ? 
                group by tipo_pgto;"""
        parms =(data,)
        
        return self.DAO.executar2(sql, parms)