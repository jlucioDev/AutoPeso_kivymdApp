from models.database import Dao

class Pagamento:
    
    def __init__(self, _venda ):
        self.venda = _venda
        self.recebidos = []
        self.DAO = Dao()
    
    def Receba(self, itPgto):
        self.recebidos.append(itPgto)
    
    def ConfirmaPagamento(self):
        res = False
        tot = 0.00
        for r in self.recebidos:
            tot += float(r['valor'].replace(',', '.').replace('R$ ', ''))
        
        if tot == self.venda.ValorTotal:
            res = True
        else:
            print("TotalRecebidos: ", tot)
            print("TotalVenda: ", self.venda.ValorTotal)

        return res
    
    def SalvarPagamento(self):
        res = False
        try:
            # SALVAR VENDAS
            self.venda.SalvarVenda()  

            #Salvar Pagamentos
            sql = '''INSERT INTO pagamentos (
                            codigo_venda,
                            tipo_pgto,
                            valor_pgto
                        )
                        VALUES (?,?,?);'''
            
                     
            for r in self.recebidos:
                v = r['valor'].replace(',', '.').replace('R$ ', '')
                if float(v) > 0.00:
                    parms = (self.venda.codigoVenda, r['tipo'], v)
                    self.DAO.addSQL(sql, parms)
              
            self.DAO.executarCommit()
            res = True
            print("Salvo novo Pagamento")
        except:
            print("Erro ao salvar novo pagamento")
        finally:
            return res
            