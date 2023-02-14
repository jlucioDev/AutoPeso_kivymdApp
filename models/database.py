from csv import excel
import sqlite3
import traceback
import sys
import io


class Dao():
    
    
    def __init__(self):
        self.sqls = []
        self.flagConnOpen = False
                
    def AbrirConexao(self):
        try:
            self.con = sqlite3.connect('database/database.db')
            self.cur = self.con.cursor()
            self.flagConnOpen = True
            print("Abriu conexao")
            
        except sqlite3.Error as error:
            print("Erro ao conectar ao banco de dados SQLite", error)
            self.FecharConexao()
  
    
    def FecharConexao(self):
        if self.flagConnOpen == True:
                self.con.close()
                self.flagConnOpen = False
                print("Conexão com o banco de dados foi finalizada")
                
    def executar(self, comando, parm):
        c = [[0.00]]
        try:
            if self.flagConnOpen == False:
                self.AbrirConexao()
                
            self.cur.execute(comando, parm)
            try:
                c = self.cur.fetchall()
            except:
                pass
            
            self.con.commit()
            
        except sqlite3.Error as er :
            print('SQLite error: %s' % (' '.join(er.args)))
            print("Exception class is: ", er.__class__)
            print('SQLite traceback: ')
            exc_type, exc_value, exc_tb = sys.exc_info()
            print(traceback.format_exception(exc_type, exc_value, exc_tb))
            
            self.con.rollback()
            #raise Exception("Erro ao executar comando")
        finally:
            self.FecharConexao()
            return c
            
            
    def executar2(self, comando, parms):
        lst = []
        try:
            if self.flagConnOpen == False:
                self.AbrirConexao()
                
            self.cur.execute(comando, parms)
            try:
                lst = self.cur.fetchall().copy()
            except:
                pass
            
            self.con.commit()
            
            print("Comando Executado")
            
        except sqlite3.Error as er :
            print('SQLite error: %s' % (' '.join(er.args)))
            print("Exception class is: ", er.__class__)
            print('SQLite traceback: ')
            exc_type, exc_value, exc_tb = sys.exc_info()
            print(traceback.format_exception(exc_type, exc_value, exc_tb))
            
            self.con.rollback()
            #raise Exception("Erro ao executar comando")
        
        finally:
            self.FecharConexao()
            return lst
            
    def addSQL(self, sql, parms =()):
        try:
            if self.flagConnOpen == False:
                self.AbrirConexao()
        except:
            print('A conexão já foi aberta')
            
        self.sqls.append({'sql': sql, 'parms': parms})
    
    def executarCommit(self):
        if  len(self.sqls) > 0:
            try:
                for inst in self.sqls: 
                    self.cur.execute(inst['sql'], inst['parms'])
                
                self.con.commit()
                print("Salvo")
                
            except:
                self.con.rollback()
                print("Erro!!")      
            finally:
                self.FecharConexao()

    def getID(self):
        return self.cur.lastrowid
    