#from views.login.login_screen import LoginScreenView
from views.menu.menu_screen import MenuScreenView
from views.pagamento.pagamento_screen import PagamentoScreenView
from views.root.root_screen import RootScreenView
from views.venda.venda_screen import VendaScreenView
from views.relatorio.relatorio_screen import RelatorioScreenView
from views.splash.splash_screen import SplashScreenView
from views.configuracao.config_screen import ConfigScreenView
from views.configuracao.configuracao_data.config_screen_data import ConfigScreenDataView
from views.configuracao.configuracao_caixa.config_screen_caixa import ConfigScreenCaixaView
from views.configuracao.configuracao_comunicacao.config_screen_comunicacao import ConfigScreenComunicacaoView
from views.venda.components.card_weight import CardWeight
from views.venda.components.item_venda import ItemVenda
from views.menu.components.circularCard import CircularCard

screens = {
    "RootScreen": RootScreenView,
    "SplashScreen": SplashScreenView,
    "MenuScreen": MenuScreenView,
    "VendaScreen": VendaScreenView,
    "PagamentoScreen": PagamentoScreenView,
    "ConfigScreen": ConfigScreenView,
    "ConfigDataScreen": ConfigScreenDataView,
    "ConfigCaixaScreen": ConfigScreenCaixaView,
    "ConfigComunicacaoScreen": ConfigScreenComunicacaoView,
    "RelatorioScreen": RelatorioScreenView
    }