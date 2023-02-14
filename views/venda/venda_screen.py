from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from models.urano import Urano
from models.venda import Venda
import threading

#from components.item_venda import ItemVenda
from kivymd.uix.list import TwoLineAvatarIconListItem, IconRightWidget, IconLeftWidget

class VendaScreenView(MDScreen):
   
    
        
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = MDApp.get_running_app()
    
    def iniciar(self):
        self.balanca = Urano(self.app.porta, self.app.simulado)
        self.balanca.FecharPorta()
        self.venda = Venda()
        self.venda.dataAtual = self.app.dataAtual
        
    def on_enter(self, *args):
       
        self.CarregaItensVenda() ####### Alterar se for usar o hot reload ##########
        return super().on_enter(*args)
    
        
    def CarregaItensVenda(self):
        self.LimparTela()
        self.venda.dataAtual = self.app.dataAtual
        cont = 0
        for i in self.venda.itens:
            self.ConstroiItemNaLista(i, cont)
            cont+=1
            
        self.ids.lblValorTotal.text = str(round(self.venda.ValorTotal,2))
    
    def LimparTela(self):
        self.ids.lblPeso.text = 'Coloque o prato na balança...'
        self.ids.lblValorKg.text = str(self.app.ValorKg)
        self.ids.lblValorItem.text = '0.00'
        self.ids.lblValorTotal.text = '0.00'
        self.ids.lstItens.clear_widgets()        
        self.ids.btIncluir.disabled = True
        self.ids.btPagamento.disabled = True
    
    def Read_Peso(self):

            c = '0.00'
            self.ids.lblPeso.text = 'Aguarde....'
            c = self.balanca.capturaPeso()
            
            if type(c) is str and len(c) > 0:
                self.ids.lblPeso.text = str(c)
                    
                total = str(self.Arrendondar(float(self.app.ValorKg.replace(',', '.')) * float(c)))
                #self.ids.lblValorItem.text = total
                self.ids.lblValorItem.text = 'R$ {:0,.2f}'.format(float(total))
                if float(total) == 0.0:
                    self.ids.btIncluir.disabled = True
                else:
                    self.ids.btIncluir.disabled = False
                      
    def LerPeso(self):
        t = threading.Thread(target = self.Read_Peso)
        t.start()
        
    def Adicionar(self):
        
        #Adicionar o item de venda
        it = self.venda.AddItenVenda(self.ids.lblPeso.text,
                                self.ids.lblValorItem.text,
                                self.ids.lblValorKg.text)
        
        self.venda.CalculaTotal_Venda()

        self.ConstroiItemNaLista(it, len(self.venda.itens)-1)
        
        self.ids.lblValorTotal.text = 'R$ {:0,.2f}'.format(float(self.venda.ValorTotal))
    
        #Reinicia Dados da pesagem
        self.ids.lblPeso.text = 'Coloque o prato na balança...'
        self.ids.lblValorItem.text = '0.00'
        self.ids.btIncluir.disabled = True
        self.ids.btPagamento.disabled = False
        
    def ConstroiItemNaLista(self, i, num):
        #constroi o widget referente ao item
        
        ir = IconRightWidget(on_release = lambda x: self.RemoverItem(num))
        ir.icon = 'minus'
        
        il = IconLeftWidget()
        il.icon = 'silverware'
        
        it = TwoLineAvatarIconListItem()
        it.add_widget(ir)
        it.add_widget(il)
        
        it.text = f"{num+1}  'Item: Prato Self Service Kg'          -          [b][color=#059B9A]{'R$ {:0,.2f}'.format(float(i['valor_prato']))}[/color][/b]"
        it.secondary_text = f"Peso: {i['peso']}kg    ValorKg: {'R$ {:0,.2f}'.format(float(i['valor_kg']))}"
        
        self.ids.lstItens.add_widget(it)    
    
    def RemoverItem(self, it):
        print("removeu: ", it)
        
        del self.venda.itens[it]
        #Apagar Lista no kv
        #self.ids.lstItens.children.clear()
        self.ids.lstItens.clear_widgets()
        #Refazer a lista com base no array da classe Venda
        cont = 0
        
        for i in self.venda.itens:
            self.ConstroiItemNaLista(i, cont)
            cont+=1

        self.venda.CalculaTotal_Venda()
        self.ids.lblValorTotal.text = 'R$ {:0,.2f}'.format(float(self.venda.ValorTotal))
        
        if self.venda.ValorTotal == 0:
            self.ids.btPagamento.disabled = True
        else:
            self.ids.btPagamento.disabled = False
    
    def Arrendondar(self, num):
        intPart = int(num)
        decPart = num % 1
        if decPart < 0.5 and decPart > 0.2:
            decPart = 0.5
        elif decPart > 0.5 and decPart < 0.7:
            decPart = 0.5
        elif decPart > 0.6:
            decPart = 1
        elif decPart < 0.3:
            decPart = 0.0
        
        return(intPart + decPart)