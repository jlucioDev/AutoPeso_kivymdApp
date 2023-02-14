from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen

class RootScreenView(MDScreen):
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = MDApp.get_running_app()