from kivymd.uix.screen import MDScreen
from kivymd.app import MDApp
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty

class ConfigScreenCaixaView(MDScreen):
    
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = MDApp.get_running_app()
    
    def show_alert_valor(self, *args):
        self.dialogValor = MDDialog(
                title="Configurações",
                type="custom",
                text= "Alterar Valor do kg",
                content_cls=ContentValor(texto= self.app.ValorKg),
                buttons=[
                    MDFlatButton(
                        text="CANCELAR",
                        theme_text_color="Custom",
                        text_color=[.26,.26,.26,1],
                        on_release= lambda _: self.dialogValor.dismiss() ,
                    ),
                    MDFlatButton(
                        text="SALVAR",
                        theme_text_color="Custom",
                        text_color=[.26,.26,.26,1],
                        on_release= lambda _: self.dialogValor_salve() ,
                    ),
                ],
            )
        self.dialogValor.open() 
    
    def dialogValor_salve(self):
        valor = self.dialogValor.content_cls.ids.txtValor.text
        if valor != '':
            self.app.alterarConfiguracao('CAIXA', 'valorKg', valor)
            self.dialogValor.dismiss()
    
class ContentValor(BoxLayout):
    texto = StringProperty()