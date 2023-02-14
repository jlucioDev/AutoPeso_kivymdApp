from kivy.properties import StringProperty
from kivymd.uix.card import MDCard


class CardWeight(MDCard):
    icon = StringProperty("play-circle-outline")
    text = StringProperty()