from kivymd.uix.screen import MDScreen
from kivymd.app import MDApp
from kivymd.uix.list import IRightBodyTouch, TwoLineListItem
from kivymd.uix.selectioncontrol import MDSwitch
from kivymd.uix.pickers import MDDatePicker
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty, BooleanProperty
from datetime import datetime

class ConfigScreenDataView(MDScreen):
    
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = MDApp.get_running_app()
        
    def on_enter(self):
        dateObj = datetime.strptime(self.app.dataAtual, '%Y-%m-%d').date()
        self.ids.btData.secondary_text = self.app.formatarData(dateObj)
    
    #Click ok
    def on_save(self, instance, value, date_range):
        self.ids.btData.secondary_text = self.app.formatarData(value) 
        self.app.alterarConfiguracao('CAIXA', 'dataatual', str(value))
        
    def show_date_picker(self):
        self.date_dialog = MDDatePicker()
        #     year= date(mydate).year, 
        #     month = date(mydate).month, 
        #     day= date(mydate).day)
        self.date_dialog.bind(on_save= self.on_save)
        self.date_dialog.open()
    

class Content(BoxLayout):
    texto = StringProperty()

class ListItemWithSwitch(TwoLineListItem):
    ativado = BooleanProperty(False)
    
    def on_ativado(self, instance, value):
        self.ativado = value
    
class RightSwitch(IRightBodyTouch, MDSwitch):
    pass