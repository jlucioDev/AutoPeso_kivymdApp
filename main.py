from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, SlideTransition
from views.screens import screens
from kivy.core.window import Window
from views.splash.splash_screen import SplashScreenView
import configparser
import datetime
from kivy.config import Config

#Para desabilitar o multitouch (Evitar que apareça bolas vermelhas caso clique com o botão direito)
Config.set('input', 'mouse', 'mouse,multitouch_on_demand')


colors = {
    "Teal": {
        "50": "e4f8f9",
        "100": "bdedf0",
        "200": "97e2e8",
        "300": "79d5de",
        "400": "6dcbd6",
        "500": "6ac2cf",
        "600": "63b2bc",
        "700": "5b9ca3",
        "800": "54888c",
        "900": "486363",
        "A100": "bdedf0",
        "A200": "97e2e8",
        "A400": "6dcbd6",
        "A700": "5b9ca3",
    },
    "Blue": {
        "50": "e3f3f8",
        "100": "b9e1ee",
        "200": "91cee3",
        "300": "72bad6",
        "400": "62acce",
        "500": "589fc6",
        "600": "5191b8",
        "700": "059b9a",
        "800": "095169",
        "900": "0D0636",
        "A100": "b9e1ee",
        "A200": "91cee3",
        "A400": "62acce",
        "A700": "0d0636",
    },
    "Red": {
        "50": "FFEBEE",
        "100": "FFCDD2",
        "200": "EF9A9A",
        "300": "E57373",
        "400": "EF5350",
        "500": "F44336",
        "600": "E53935",
        "700": "D32F2F",
        "800": "C62828",
        "900": "B71C1C",
        "A100": "FF8A80",
        "A200": "FF5252",
        "A400": "FF1744",
        "A700": "D50000",
    },
    "Green": {
        "600": "9FD86B",
        "700": "53BA83"
    },
    "Light": {
        "StatusBar": "E0E0E0",
        "AppBar": "F5F5F5",
        "Background": "FAFAFA",
        "CardsDialogs": "FFFFFF",
        "FlatButtonDown": "cccccc",
    },
    "Dark": {
        "StatusBar": "000000",
        "AppBar": "212121",
        "Background": "303030",
        "CardsDialogs": "424242",
        "FlatButtonDown": "999999",
    }
}

######## MAIN APP ######## 
class MyTesteApp(MDApp):
    
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.load_all_kv_files(self.directory)
        self.sm = ScreenManager(transition=SlideTransition())
        self.porta = ''
        self.dataAtual = ''
        self.dataSistema = datetime.date.today()
        self.ValorKg = '0.00'
        self.check = False
        self.simulado = False
        
    def build(self):
    #def build(self) -> ScreenManager:
        self.theme_cls.colors = colors
        self.theme_cls.primary_palette = "Blue"  # "Purple", "Red"
        self.theme_cls.primary_hue = "900"  # "500"
        self.title = " AUTOPESO - Versão 1.0 (Beta)"
        self.icon = "assets/icons/icone.ico"
            
        Window.size = (800,650)
        self.change_Screen()
        #t = threading.Thread(target = self.generate_application_screens)
        #t.start()
        self.generate_application_screens()
        return self.sm
    
        
    def stop(self, *largs):
        self.root_window.close()  # Fix app exit on Android.
        return super(MyTesteApp, self).stop(*largs)
    
    
    def change_Screen(self):
        splash = SplashScreenView()
        self.sm.add_widget(splash)
        self.sm.current = 'splash'
     
    def generate_application_screens(self):
        
        for name_screen in screens.keys():
            view = screens[name_screen]()
            self.sm.add_widget(view)

    def getColor(self, tab_text, value_color):
        return colors[tab_text][value_color]
    
    def setScreen(self, nome, direction = 'left'):
        self.sm.transition.direction = direction
        self.sm.current = nome
    
    def getScreen(self, nome):
        return self.sm.get_screen(nome)
    
    ### Configuração ####
    def carregarConfiguracao(self):
        self.configuracao = configparser.ConfigParser()
        self.configuracao.read("config/config.ini")
        self.porta = self.configuracao["BALANCA"]["porta"]
        self.simulado = self.convertToBool(self.configuracao["BALANCA"]["simular"])
        self.dataAtual = self.configuracao["CAIXA"]["dataAtual"]
        self.ValorKg = self.configuracao["CAIXA"]["valorKg"]
    
    def alterarConfiguracao(self, title, item, value):
        self.configuracao.set(title, item, str(value))
        with open("config/config.ini", "w") as configfile:
            self.configuracao.write(configfile)
        self.carregarConfiguracao()
    
    #### DATA ####
    def formatarData(self, dValue):
        mes = {
            1: 'janeiro',
            2: 'fevereiro',
            3: 'março',
            4: 'abril',
            5: 'maio',
            6: 'junho',
            7: 'julho',
            8: 'agosto',
            9: 'setembro',
            10: 'outubro',
            11: 'novembro',
            12: 'dezembro'        
        }
        return str(dValue.day) + " de " + mes[dValue.month] + " de " + str(dValue.year)

    def convertToBool(self, str):
        res = False
        if str == 'True':
            res = True
        return res
    
if __name__ == "__main__":        
    MyTesteApp().run()
