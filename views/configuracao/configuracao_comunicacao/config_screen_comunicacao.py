from kivymd.uix.screen import MDScreen
from kivymd.app import MDApp
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivymd.uix.textfield import MDTextField
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty

class ConfigScreenComunicacaoView(MDScreen):
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = MDApp.get_running_app()
    
    def on_enter(self):
        self.ids.btSimulado.ativado = self.app.simulado
        
    def show_alert_porta(self, *args):
        self.dialogPorta = MDDialog(
                title="Configurações",
                type="custom",
                text= "Alterar porta de comunicação",
                content_cls=Content(texto= self.app.porta),
                buttons=[
                    MDFlatButton(
                        text="CANCELAR",
                        theme_text_color="Custom",
                        text_color=[.26,.26,.26,1],
                        on_release= lambda _: self.dialogPorta.dismiss() ,
                    ),
                    MDFlatButton(
                        text="SALVAR",
                        theme_text_color="Custom",
                        text_color=[.26,.26,.26,1],
                        on_release= lambda _: self.dialogPorta_salve() ,
                    ),
                ],
            )
        self.dialogPorta.open()
    
    def dialogPorta_salve(self):
        porta = self.dialogPorta.content_cls.ids.txtComPort.text
        if porta != '':
            self.app.alterarConfiguracao('BALANCA', 'porta', porta)
            self.ids.lblPorta.secondary_text = porta
            self.dialogPorta.dismiss()
            
    def alterar_simulado(self, valor):
        
        self.app.alterarConfiguracao('BALANCA', 'simular', valor)
        self.app.simulado = bool(valor)
    
class Content(BoxLayout):
    texto = StringProperty()