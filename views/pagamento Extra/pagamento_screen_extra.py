from kivymd.uix.screen import MDScreen
from kivymd.app import MDApp
from kivymd.uix.list import TwoLineAvatarIconListItem, IconLeftWidget
from models.pagamento import Pagamento
from models.venda import Venda
from kivymd.uix.snackbar import Snackbar
from kivymd.uix.relativelayout import MDRelativeLayout
from kivy.properties import StringProperty

class PagamentoExtraScreenView(MDScreen):
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = MDApp.get_running_app()
        
        
    def IncluirPagamento(self):
        
        self.Formatar_Numero_Geral()
        # 1 - RECEBE OS VALORS DE PAGAMENTOS
        print("-- Valor de txtDinheiro: ", self.ids.txtDinheiro.text)
        print("-- Valor de txtDinheiro.Troco: ", self.ids.txtDinheiro.troco)
        print("-- Valor de txtDinheiro.text_troco: ", self.ids.txtDinheiro.text_troco)
        
        lstPgto = []
        lstPgto.append({"tipo": "Dinheiro", "valor": self.ids.txtDinheiro.text if (self.ids.txtDinheiro.troco == False) else str(float(self.ids.txtDinheiro.text.replace(',','.')) - float(self.ids.txtDinheiro.text_troco.replace(',','.'))) })
        lstPgto.append({"tipo": "Débito", "valor": self.ids.txtDebito.text})
        lstPgto.append({"tipo": "Crédito", "valor": self.ids.txtCredito.text})
        lstPgto.append({"tipo": "Pix", "valor": self.ids.txtPix.text})
        
        self.pg.recebidos = lstPgto.copy()      
        # 2 - CONFIRMA PAGAMENTOS
        if self.pg.ConfirmaPagamento():
            self.pg.SalvarPagamento()
            #Mostrar Confirmação e voltar para Vendas
            # create content and add to the popup
            #self.show_alert_dialog()
            self.Show_Message_OK()
            obj = self.app.getScreen('venda')
            obj.venda = Venda()
            self.app.setScreen('venda', 'right')
            self.LimparTela()
        else:
            self.Show_Message_Erro()
            
    
    def Show_Message_Erro(self):
        Snackbar(
            text="[color=#DCD9D9]Erro ao savar pagamento.\n Verifique os valores![/color]",
            snackbar_x="50dp",
            snackbar_y="10dp",
            size_hint_x=.7,
            bg_color=(0.8, 0, 0, 1)
        ).open()
    
    def Show_Message_OK(self):
        Snackbar(
            text="[color=#DCD9D9]Pagamento concluído com sucesso!.[/color]",
            snackbar_x="50dp",
            snackbar_y="10dp",
            size_hint_x=.7,
            bg_color=(0, 0.8, 0.1, 1)
        ).open()
            
    def LimparTela(self):
        self.ids.lstItens.clear_widgets()
        for txt in self.ids.ContainerTxt.children:
            txt.text = "0,00"
            txt.on_click("arrow-left")
            
    
    #Formata o número após a valiação do texto
    def on_clicado(self, controle):
        for txt in self.ids.ContainerTxt.children:
            if txt.hint_text == controle:
                if controle == 'DINHEIRO' and txt.iconBt == "arrow-left" and txt.troco == True:
                    txt.troco = False
                txt.text = str("0,00") if txt.iconBt == "arrow-left" else self.ids.lblValorTotal.text
                
        
    def Formatar_Numero_Geral(self):
            
        for txt in self.ids.ContainerTxt.children:
            #Verifica se o valor do txt é decimal
            r = float(txt.text.replace(',', '.')) - int(float(txt.text.replace(',', '.')))
            if ( r == 0.0):
                txt.text = str(int(float(txt.text.replace(',', '.')))) + str(",00") 
                    
    def Formatar_Numero(self, controle = ''):
        #Verificar se é o txtDinheiro#
        if controle == 'DINHEIRO':
            if float(self.ids.txtDinheiro.text.replace(',', '.')) > float(self.ids.lblValorTotal.text):
                troco = float(self.ids.txtDinheiro.text.replace(',', '.')) - float(self.ids.lblValorTotal.text)
                self.ids.txtDinheiro.setTroco(troco)
                return
            
        for txt in self.ids.ContainerTxt.children:
            txt.troco = False
            txt.text_troco = "0,00"
            if txt.hint_text == controle:
                #Verifica se o valor do txt é decimal
                r = float(txt.text.replace(',', '.')) - int(float(txt.text.replace(',', '.')))
                if ( r == 0.0):
                    txt.text = str(int(float(txt.text.replace(',', '.')))) + str(",00")   
            
    # Volta para a tela de Venda
    ## Método executado ao entrar na tela
    def CarregaItensVenda(self): 
        obj = self.app.getScreen('venda')
        obj.dataAtual = self.app.dataAtual
        self.pg = Pagamento(obj.venda)
        
        self.LimparTela()
         
        cont = 0
        for i in obj.venda.itens:
            self.ConstroiItemNaLista(i, cont)
            cont+=1
            
        self.ids.lblValorTotal.text = str(round(obj.venda.ValorTotal,2))
    
    def ConstroiItemNaLista(self, i, num):
        #constroi o widget referente ao item
        
        il = IconLeftWidget()
        il.icon = 'silverware'
        
        it = TwoLineAvatarIconListItem()
        it.add_widget(il)
        
        it.text = f"{num+1}  'Item: Prato Self Service Kg'          -          [b][color=#059B9A]{i['valor_prato']}[/color][/b]"
        it.secondary_text = f"Peso: {i['peso']}kg    ValorKg: {i['valor_kg']}"
        
        self.ids.lstItens.add_widget(it)
        
    
        