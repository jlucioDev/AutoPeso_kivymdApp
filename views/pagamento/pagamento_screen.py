from ast import Pass
from asyncio import events
from kivymd.uix.screen import MDScreen
from kivymd.app import MDApp
from kivymd.uix.list import TwoLineAvatarIconListItem, IconLeftWidget
from models.pagamento import Pagamento
from models.venda import Venda
from kivymd.uix.snackbar import Snackbar
from kivymd.uix.relativelayout import MDRelativeLayout
from kivy.properties import StringProperty

class PagamentoScreenView(MDScreen):
    
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
        lstPgto.append({"tipo": "Dinheiro", "valor": self.ids.txtDinheiro.text if (self.ids.txtDinheiro.troco == False) else str(self.FormatF(self.ids.txtDinheiro.text) - self.FormatF(self.ids.txtDinheiro.text_troco))})
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
                txt.text = str("0,00") if txt.iconBt == "arrow-left" else self.FormatS(self.ids.lblValorTotal.text)
                
        
    def Formatar_Numero_Geral(self):
            
        for txt in self.ids.ContainerTxt.children:
            #Verifica se o valor do txt é decimal
        
            r = self.FormatF(txt.text) - int(self.FormatF(txt.text))
            if ( r == 0.0):
                txt.text = str(int(self.FormatF(txt.text))) + str(",00") 
                    
    def Formatar_Numero(self, controle = ''):
        #Verificar se é o txtDinheiro#
        if controle == 'DINHEIRO':
            if self.FormatF(self.ids.txtDinheiro.text) > self.FormatF(self.ids.lblValorTotal.text):
                troco = self.FormatF(self.ids.txtDinheiro.text) - self.FormatF(self.ids.lblValorTotal.text)
                self.ids.txtDinheiro.text = self.FormatS(self.ids.txtDinheiro.text)
                self.ids.txtDinheiro.setTroco(troco)
                return
            
        for txt in self.ids.ContainerTxt.children:
            txt.troco = False
            txt.text_troco = "0,00"
            if txt.hint_text == controle:
                #Verifica se o valor do txt é decimal
                r = self.FormatF(txt.text) - int(self.FormatF(txt.text))
                if ( r == 0.0):
                    txt.text = str(int(self.FormatF(txt.text))) + str(",00")   
            
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
            
        self.ids.lblValorTotal.text = self.FormatS(obj.venda.ValorTotal)
    
    def ConstroiItemNaLista(self, i, num):
        #constroi o widget referente ao item
        
        il = IconLeftWidget()
        il.icon = 'silverware'
        
        it = TwoLineAvatarIconListItem()
        it.add_widget(il)
        
        it.text = f"{num+1}  'Item: Prato Self Service Kg'          -          [b][color=#059B9A]{'R$ {:0,.2f}'.format(float(i['valor_prato']))}[/color][/b]"
        it.secondary_text = f"Peso: {i['peso']}kg    ValorKg: {'R$ {:0,.2f}'.format(float(i['valor_kg']))}"
        
        self.ids.lstItens.add_widget(it)
    
    def FormatF(self, valor):
        res = ''
        if type(valor) == str:
            res = float(valor.replace('R$ ', '').replace(',', '.'))
        else:
            res = float(valor)
        return res
    
    def FormatS(self, valor):
        return 'R$ {:0,.2f}'.format(self.FormatF(valor))
    
class ClickableTextFieldRound(MDRelativeLayout):
    text = StringProperty()
    hint_text = StringProperty()
    iconBt = StringProperty("arrow-left")
    text_troco = StringProperty(0)
    
    def __init__(self, **kwargs):
        # make sure we aren't overriding any important functionality
        super(ClickableTextFieldRound, self).__init__(**kwargs)
        self.register_event_type('on_texto')
        self.register_event_type('on_clicked')
        self.troco = False
        
    def on_texto(self):
        pass
        
    def on_clicked(self, msg):
        pass

    def on_validate_text(self):
        self.text = self.ids.text_field.text
        
        if self.ids.text_field.text != "0,00":
            self.ids.btIcon.icon = "cash"
                #self.ids.text_field.line_color_focus= [0, 1, 0, 1]
            self.ids.text_field.line_color_normal= [0, 1, 0, 1]
            self.ids.btIcon.theme_icon_color= "Custom"
            self.ids.btIcon.icon_color = [0, 1, 0, 1]
            self.ids.text_field.color = [0,1,0,1]
        else:
            self.ids.btIcon.icon = "arrow-left"
            self.ids.text_field.line_color_normal= [0.16, 0.16, 0.16, 1]
            self.ids.btIcon.theme_icon_color= "Custom"
            self.ids.btIcon.icon_color = [0.16, 0.16, 0.16, 1]
            self.ids.text_field.color = [0.16, 0.16, 0.16, 1]
            
        self.dispatch('on_texto')
        
    def setTroco(self, troco):
        self.ids.text_field.helper_text= f"Troco: {'R$ {:0,.2f}'.format(troco)}"
        #self.ids.text_field.helper_text_mode= "persistent"
        self.ids.text_field.helper_text_mode= "on_error"
        self.ids.text_field.error = True
        self.troco = True
        self.text_troco = str(troco)
        
        
    def on_click(self, icone):
        self.ids.text_field.text = self.text
        self.iconBt = icone
        if self.iconBt != "arrow-left":
            #self.ids.text_field.line_color_focus= [0, 1, 0, 1]
            self.ids.text_field.line_color_normal= [0, 1, 0, 1]
            self.ids.btIcon.theme_icon_color= "Custom"
            self.ids.btIcon.icon_color = [0, 1, 0, 1]
            self.ids.text_field.color = [0,1,0,1]
        else:
            self.ids.text_field.line_color_normal= [0.26, 0.26, 0.26, 1]
            self.ids.btIcon.theme_icon_color= "Custom"
            self.ids.btIcon.icon_color = [0.26, 0.26, 0.26, 1]
            self.ids.text_field.color = [0.26, 0.26, 0.26, 1]
        self.dispatch('on_clicked', 'msg')
    
        