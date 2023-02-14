from datetime import datetime
from kivymd.uix.screen import MDScreen
from kivymd.app import MDApp
from models.dashboard import Dashboard


class MenuScreenView(MDScreen):
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = MDApp.get_running_app()
    
    def CarregarDados(self):
        info = Dashboard(self.app.dataAtual)
        info.getTotais()
        self.ids.cardVendasTotal.c_subtext = 'R$ {:0,.2f}'.format(info.VendasTotal)
        self.ids.cardVendasQtde.c_subtext = str(info.VendasQtde)
        self.ids.cardVendasKg.c_subtext = str(round(info.VendasKg,2))
        
    
    def AbrirVenda(self):
        self.app.getScreen('venda').iniciar()
        self.app.setScreen('venda')
    
    def AbrirRelatorios(self):
        #obj = self.app.getScreen('relatorio')
        #obj.carregar_dados(self.app.dataAtual)
        self.app.setScreen('relatorio')
    
    
        
    
    
    
    