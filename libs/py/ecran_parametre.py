from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen

from kivy.properties import (
    ColorProperty,
    StringProperty,
    ObjectProperty,
)

from kivymd.uix.card import MDCard
from kivymd.uix.menu import MDDropdownMenu

from libs.module.variable import my_fonts
from libs.py.screenmanager import screen_manager


class MonButtonTheme(MDCard):
    md_bg_color = ColorProperty(
        [0.12941176470588237, 0.5882352941176471, 0.9529411764705882, 1.0]
    )  # couleur par défaut
    text = StringProperty("Bleu")  # text par défaut
    text_color = ColorProperty()
    elevation = 2


class CardText(MDCard):
    pass


class MyMDDropdownMenu(MDDropdownMenu):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.status: str = "close"

    def opening(self):
        """
        desolé je n'est pas trouver autre nom parlant qui ne serais pas en conflit avec d'autre class
        """
        self.status = "open"
        self.open()

    def dismiss(self):
        self.status = "close"
        self.on_dismiss()


class EcranParam(Screen, BoxLayout):
    my_sep_height = 2
    apps = ObjectProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.my_menu_polices: MDDropdownMenu
        self.my_menu_taille = None
        Window.bind(on_keyboard=self.on_key_press)

    def menu_police(self, obj: ObjectProperty = None):
        if not self.my_menu_polices:
            menu_style = [
                {
                    "text": f"{i}",
                    "viewclass": "OneLineListItem",
                    "_lbl_primary.markup": "False",
                    "on_release": lambda x=f"{i}": self.apps.changer_police(x),
                }
                for i in my_fonts
            ]

            self.my_menu_polices = MyMDDropdownMenu(
                # TODO: ameliorer le menu en ajoutant (header, radius, ajuster la taille ...)
                caller=obj,
                items=menu_style,
                position="center",
                max_height=600,
                width_mult=5,
            )
        self.my_menu_polices.opening()

    def menu_taille(self, obj: ObjectProperty = None):
        if not self.my_menu_taille:
            tailles = [5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70]
            menu_style = [
                {
                    "text": f"[font={self.apps.my_font}]{i}[/font]",
                    "viewclass": "OneLineListItem",
                    "_lbl_primary.markup": "False",
                    "on_release": lambda x=f"{i}": self.apps.changer_taille(x),
                }
                for i in tailles
            ]

            self.my_menu_taille = MyMDDropdownMenu(
                # TODO: ameliorer le menu en ajoutant (header, radius, ajuster la taille ...)
                caller=obj,
                items=menu_style,
                position="center",
                max_height=600,
                width_mult=5,
                opening_time=0.1,
            )
        self.my_menu_taille.opening()

    def on_key_press(self, window, key, *args):
        """
        Permet de fermer les menus 'self.my_menu_taille ou self.my_menu_taille'
        s'ils sont ouvert et de ne pas faire de retour sur l'ecran principal
        """
        if key == 27 and screen_manager.current == "parametres":
            try:
                if self.my_menu_polices.status == "open":
                    self.my_menu_polices.dismiss()
                    return True
            except Exception as e:
                print("Exeption : ==============>>>>>>", self, e)

            try:
                if self.my_menu_taille.status == "open":
                    self.my_menu_taille.dismiss()
                    return True
            except Exception as e:
                print("Exeption : ==============>>>>>>", self, e)

    def charger_app(self):
        """
        Cette fonction est faite uniquement pour pouvoir utiliser des fonction qui se trouve dans le fichier main.py
        dans ce fichier.
        On peut les appeler dans les fichier kv a partir de app, mais on ne peut les appeler dans les fichier py.
        Du coup, je charge la propriété app du .kv dans le .py pour pouvoir l'utiliser.
        """
        self.apps.theme_cls.theme_style = (
            "Dark" if self.apps.theme_cls.theme_style == "Light" else "Light"
        )
