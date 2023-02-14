from kivymd.uix.screen import MDScreen
from kivymd.app import MDApp
import os.path
from models.database import Dao
from models.urano import Urano
import threading
import time
from datetime import datetime
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton

class SplashScreenView(MDScreen):
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = MDApp.get_running_app()
        
    
    def IniciarSistema(self):
        if self.app.check == False:
            self.t1 = threading.Thread(target=self.Executar)
            self.t1.start()
            self.app.check = True
    
    def Executar(self):
        #Desabilita os botões de entrada
        self.ids.btEntrar.disabled = True
        self.ids.btConfigurar.disabled = True
        
        time.sleep(0.5)
        self.ids.lblInfo.text = "Iniciando Verificação do sistema..."
        self.ids.progress.start()
        time.sleep(1)
        
        #Ler arquivo de configuração#
        self.app.carregarConfiguracao()
        time.sleep(1)
        self.ids.lblInfo.text += "\nLendo arquivo de configuração: OK"
        
        #Recebe a dataAtual que está configurado
        dateObj = datetime.strptime(self.app.dataAtual, '%Y-%m-%d').date()
        self.ids.lblInfo.text += "\nData atual do sistema: " + self.app.formatarData(dateObj)
        self.ids.lblInfo.text += "\n" + ("#" * 30)
        
        #Verificar se o arquivo do banco de dados existe
        if not (os.path.isfile('database/database.db')):
            self.ids.lblInfo.text += "\n Erro ao conectar ao banco de dados. \n Arquivo não encontrado!"
        else:
            time.sleep(0.5)
            self.ids.lblInfo.text += "\nArquivo do Banco de dados verificado: OK"
        
        #Verificar conexão com banco de dados / Existe venda com data Atual do sistema
        self.DAO = Dao()
        try:
            self.DAO.AbrirConexao()
            time.sleep(2.5)
            self.ids.lblInfo.text += "\nConexão com Banco de dados verificado: OK"
        except:
            self.ids.lblInfo.text += "\n Erro ao abrir banco de dados"
        finally:
            self.DAO.FecharConexao()
            
        #Senão criar novo banco de dados
        #Verificar conexão com a balança
        try:
            time.sleep(0.5)
            porta = self.app.porta
            self.balanca = Urano(porta, self.app.simulado)
            self.balanca.FecharPorta()
 
            self.ids.lblInfo.text += "\nConexão com a Balança: OK"
            
            
        except:
            self.ids.lblInfo.text += "\n[color=ff0000]Erro ao conectar com a balança: NOK[/color]"
        
        if self.app.simulado == True:
            self.ids.lblInfo.text += "\n[color=00d946]🟢Simulando balança: OK[/color]"
            
        self.ids.btEntrar.disabled = False
        self.ids.btConfigurar.disabled = False
        
        ## Ler data de referencia no arquivo ini
        #self.app.alterarConfiguracao('CAIXA', 'dataatual', sel)
        self.ids.progress.stop()
        
    def msgbox_Show(self, *args):
        self.dialogQuit = MDDialog(
                title="AutoPeso",
                type="custom",
                text= "Deseja realmente sair?",
                buttons=[
                    MDFlatButton(
                        text="NÃO",
                        theme_text_color="Custom",
                        text_color=[.26,.26,.26,1],
                        on_release= lambda _: self.dialogQuit.dismiss() ,
                    ),
                    MDFlatButton(
                        text="SIM",
                        theme_text_color="Custom",
                        text_color=[.26,.26,.26,1],
                        on_release= lambda _: self.outro_metodo() ,
                    ),
                ],
            )
        self.dialogQuit.open()

            