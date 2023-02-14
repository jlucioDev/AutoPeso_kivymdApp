from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from models.relatorio import Relatorio
from datetime import datetime

class RelatorioScreenView(MDScreen):
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = MDApp.get_running_app()
        
    def on_enter(self):
        self.carregar_dados(self.app.dataAtual)
        
    def carregar_dados(self, data):
        data2 = datetime.strptime(data, '%Y-%m-%d')
        self.ids.lblData.text= f"Relatório de vendas do dia: [b]{self.app.formatarData(data2)}[/b]"
        self.ids.lblDinheiro.text= "R$ 0,00"
        self.ids.lblDebito.text= "R$ 0,00"
        self.ids.lblCredito.text= "R$ 0,00"
        self.ids.lblPix.text= "R$ 0,00"
        
        r = Relatorio()
        dt =  r.getRelatorio(data)
        total = 0.00
        if len(dt) != 0:
            for row in dt:
                if row[0] == 'Dinheiro':
                    self.ids.lblDinheiro.text = 'R$ {:0,.2f}'.format(float(row[1]))
                    pass
                if row[0] == 'Débito':
                    self.ids.lblDebito.text = 'R$ {:0,.2f}'.format(float(row[1]))
                    pass
                if row[0] == 'Crédito':
                    self.ids.lblCredito.text = 'R$ {:0,.2f}'.format(float(row[1]))
                    pass
                if row[0] == 'Pix':
                    self.ids.lblPix.text = 'R$ {:0,.2f}'.format(float(row[1]))
                    pass
                total += float(row[1])
        
        self.ids.lblTotal.text = 'R$ {:0,.2f}'.format(total)
        
        self.ids.lblAtualizado.text = f"Dados atualizados em {datetime.today()}"
        