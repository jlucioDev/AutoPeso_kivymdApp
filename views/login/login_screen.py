from kivymd.uix.screen import MDScreen
from kivymd.app import MDApp
from kivy.core.window import Window

class LoginScreenView(MDScreen):
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = MDApp.get_running_app()
    
    
    def On_Valid_Login(self):
        #Buscar os usuários em um banco de dados
        
        #verificar usuário
        
        #Verificar senha
        Window.maximize()
        self.app.root.current = "menu"
        