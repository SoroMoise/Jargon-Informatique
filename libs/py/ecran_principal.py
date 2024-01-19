from datetime import datetime

from kivy.core.window import Window
from kivy.metrics import dp
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import Screen
from kivy.utils import platform
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget


from kivymd.uix.dialog import MDDialog
from kivymd.uix.menu import MDDropdownMenu

from libs.py.class_personnalisation import APropos, ContenRef
from libs.py.interaction_bd import ajouter_mot, purge, mot_aleatoir, interroger_bd, suppreime_mot
from libs.py.liste_elements import ListeElements
from libs.py.screenmanager import screen_manager
from libs.module.variable import menu_dictionnaire

from kivymd.toast import toast


class MainScreen(Screen, BoxLayout):
    """
    Ecrant principal( ecran de demarrage de l'APP )
    """

    definition = ""
    couleur = None
    menu = None
    numero = 0
    dialog_a_propos = None
    dialog_ref = None
    rechercher: bool = True
    width_sreen = Window.width
    height_sreen = Window.height
    le_focus = None
    my_app = ObjectProperty()
    word_definition = "mot, definition"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        MainScreen.fermer = self.ids.nav_drawer
        MainScreen.definition = self.ids.id_kv_definition
        MainScreen.mot = self.ids.id_kv_mot
        """
        Ici la couleur par défaut du btn est la couleur des son voisin (le chevron gauche), car si je considère
        que la couleur par défaut est blanc,cela peut être faut dans certain cas. Car il peut arriver que la
        couleur soit noir en fonction de theme choisi par l'utilisateur.
        """
        MainScreen.couleur = self.ids.button_aimer
        MainScreen.le_focus = self.ids.content_nav_drawer.ids.search_field.focus
        Window.bind(on_mouse_down=self.on_mouse)
        MainScreen.definition.bind(on_ref_press=self.on_clic_ref)

    def on_enter(self) -> None:

        if platform == "android":
            """
            Permetras de faire de actions tel que le changement de la couleur de
            la bare de navigation ou de la bare des status
            """

        if self.rechercher:
            self.recherche_aleatoir()
            self.rechercher = False
        MainScreen.aimer()

    def on_clic_ref(self, instance, ref_label: str) -> None:
        """
        Cette fonction est appelé quand on clic sur un mot souligne en bleu (un lien ou reference)
        :param ref_label:le mot sur lequel on clic
        :param instance: instance de la definition
        :return: None
        """
        font_name = self.ids.id_kv_definition.font_name
        font_size = self.ids.id_kv_definition.font_size
        try:
            ContenRef.definition = purge(
                interroger_bd("definition", "dictionnaire",
                              f'WHERE idmot = "{ref_label.lower()}"')[0][0]
            )
        except Exception as e:
            print("Exeption onClickref con ref definde : ==============>>>>>>", self, e)
            toast(
                text=f"Impossible d'afficher '{ref_label}', une erreur c'est produite", duration=4)
            return
        self.dialog_ref = MDDialog(
            title=f"[b][u]{ref_label}[/u][/b]",
            opacity=1,
            type="custom",
            padding=[0, 0, 0, 0],
            radius=[45, 45, 45, 45],
            height=self.height,
            content_cls=ContenRef(),
        )

        self.dialog_ref.width = self.width_sreen * 0.9
        self.dialog_ref.ids.title.font_name = font_name
        self.dialog_ref.ids.title.font_size = font_size+dp(10)
        self.dialog_ref.ids.title.halign = "center"
        self.dialog_ref.ids.container.padding = [
            "10dp", "10dp", "-5dp", "10dp"]
        if self.dialog_ref.ids.title.font_name != font_name or self.dialog_ref.ids.title.font_size != font_size:
            self.dialog_ref.ids.title.font_name = font_name
            self.dialog_ref.ids.title.font_size = font_size+dp(10)
            self.dialog_ref.children[0].children[3].font_name = font_name
            self.dialog_ref.children[0].children[3].font_size = font_size
            # TODO: "Optimiser le code, voir s'il faut mettre un if ou s'il faut laisser parcourrit tout les elements"
            try:
                for i in self.dialog_ref.children[0].children[2].children[0].ids.values():
                    i.font_name = font_name
                    i.font_size = font_size
            except Exception as e:
                print("Exeption on click ref in dialog ref: ==============>>>>>>", self, e)
        self.dialog_ref.open()

    def on_mouse(self, obj, x, y, clic, *args):

        self.ids.nav_drawer.enable_swiping = self.ids.nav_drawer.status != "opened" or x > self.ids.nav_drawer.width

    @classmethod
    def afficher_definition(cls, idmot: str = "", mot: str = "", definition: str = "", faire_requete: bool = False):
        """
        affiche la definition du mot sur lequel on click dans la zone de recherche
        :param definition: La definition du mot qui doit etre afficher si faire_requete est False
        :param mot: le mot qui doit etre afficher si faire_requete est False
        :param faire_requete: permet de savoir s'il faut faire une requette sur l'idmot pour trouver la definition
        ou qu'elle est dejas fourni
        :param idmot: l'id du mot sur lequel on clic
        :return: None
        """
        cls.vider_ecran()

        if not faire_requete:
            cls.mot.text = mot
            cls.definition.text = purge(definition)
            if hist_exist := interroger_bd("id_mot", "historique", f'WHERE id_mot = "{mot.lower()}"'):
                suppreime_mot("historique ", f'WHERE id_mot = "{mot.lower()}"')

            ajouter_mot("historique", mot.lower(), str(datetime.now())[:19])

        else:
            resultat = interroger_bd(
                cls.word_definition, "dictionnaire", f'WHERE idmot = "{idmot}"')[0]
            cls.afficher_definition(mot=resultat[0], definition=resultat[1])

        if MainScreen.fermer.state == "open":
            MainScreen.fermer.set_state("close")

        cls.aimer()

    @classmethod
    def mot_suivant(cls) -> None:
        cls.vider_ecran()
        mot_actuel = cls.obtenir_id_mot_actuel()
        numero: int = interroger_bd(
            "numero", "dictionnaire ", f'WHERE idmot = "{mot_actuel}"')[0][0]
        if numero < 9559:
            mot: list = interroger_bd(
                cls.word_definition, "dictionnaire", f'WHERE numero = "{numero + 1}"')[0]
            cls.mot.text = mot[0]
            cls.definition.text = purge(mot[1])
            cls.aimer()
        else:
            toast("Vous avez atteint le dernier mot", duration=2)

    @classmethod
    def vider_ecran(cls) -> None:
        try:
            cls.mot.clear_widgets()
            cls.definition.clear_widgets()
        except Exception as e:
            print("Exeption vider_ecran : ==============>>>>>>", cls, e)

    @classmethod
    def obtenir_id_mot_actuel(cls) -> str:
        """
        permet d'obtenir l'identifiant du mot actuellement afficher a l'ecran
        """
        return cls.mot.text.lower()

    @classmethod
    def aimer(cls, button_aimer: bool = False) -> None:
        """
        cette fonction est appeler quand on clieque sur le coeur pour liker ou disliker
        Elle est aussi appelé quand on fait une recherche aleatoir ou une recherche manuel, elle permet de verifier
        qu'un mot est aimer ou pas et de changer la couleur du coeur en consequence
        :param button_aimer: si cette valeur est a True c'est que le boutton coeur est cliquer et une action specifique
        est faite
        """
        idmot = cls.obtenir_id_mot_actuel()
        try:
            existe: list = interroger_bd(
                "id_mot", "aimer ", f'WHERE id_mot = "{idmot}"')[0][0]
        except Exception as e:
            print("Exeption exist lis interoge : ==============>>>>>>", cls, e)
            existe = []

        if existe == idmot:
            if button_aimer:
                suppreime_mot("aimer ", f'WHERE id_mot = "{idmot}"')

                cls.couleur.text_color = screen_manager.get_screen(
                    "main_screen").ids.chevron_left.text_color
            else:
                cls.couleur.text_color = [1, 0, 0, .7]
        elif button_aimer:
            ajouter_mot("aimer", idmot, str(datetime.now())[:19])
            cls.couleur.text_color = [1, 0, 0, .7]
        else:
            cls.couleur.text_color = screen_manager.get_screen(
                "main_screen").ids.chevron_left.text_color

    @classmethod
    def recherche_aleatoir(cls) -> None:
        """
        cette fonction permet de faire une recherche aleatoire
        """
        cls.vider_ecran()
        mot_def = mot_aleatoir()
        cls.mot.text = mot_def[0]
        cls.definition.text = purge(mot_def[1])
        cls.aimer()

    @classmethod
    def recherche(cls):
        """cette fonction s'execute lorsqu'on clique sur la touche de recherche"""
        try:
            if cls.fermer.state == "close":
                cls.fermer.set_state("open")

            else:
                MainScreen.fermer.set_state("close")
        except ReferenceError:
            toast("Une erreur c'est produit, veillez réessayer !")

    @classmethod
    def focus(cls) -> None:
        """
        Permet d'activer le champ de saisie automatiquement lors de l'ouverture de la MDNavigationDrawer

        :return: None
        """
        if cls.fermer.state == "close":
            cls.le_focus = True

    @classmethod
    def mot_precedent(cls) -> None:
        cls.vider_ecran()
        mot_actuel = cls.obtenir_id_mot_actuel()
        numero: int = interroger_bd(
            "numero", "dictionnaire ", f'WHERE idmot = "{mot_actuel}"')[0][0]
        if numero > 1:
            mot: list = interroger_bd(
                cls.word_definition, "dictionnaire", f'WHERE numero = "{numero - 1}"')[0]
            cls.mot.text = mot[0]
            cls.definition.text = purge(mot[1])
            cls.aimer()
        else:
            toast("Vous avez atteint le prémier mot", duration=2)

    @staticmethod
    def capture_ecran() -> None:
        """
        Permet de faire une capture d'ecran de l'ecran principale

        :return: None

        MainScreen().children[0].children[0].children[0].children[0].export_to_png(nom)
        MainScreen().children[0].children[0].export_to_png(nom1)
        self.get_root_window().export_to_png(nom)
        nom = f"capture_{str(str(datetime.now())[:19])}.png"
        nom1 = f"capture_( 1 ){str(str(datetime.now())[:19])}.png"
        MainScreen.numero += 1
        """
        pass

    def affiche_menu(self, button):
        """Cette fonction est appelé quant on clic sur le 'dot-vertical' en haut a gauche pour afficher le menu"""
        if not self.menu:
            menu_items = [
                {
                    "viewclass": "OneLineListItem",
                    "text": f"{menu_dictionnaire[i]}",
                            "height": dp(45),
                            "halign": "center",
                            "on_release": lambda x=f"{i}": self.clic_menu(x),
                } for i in menu_dictionnaire
                # TODO : Ajouter des icons par la suite
            ]
            self.menu = MDDropdownMenu(
                items=menu_items,
                position="center",
                width_mult=4,
                opening_time=0.1,
            )
            self.menu.caller = button
        self.menu.open()

    def clic_menu(self, text_item: str):
        if self.menu:
          self.menu.dismiss()

        if text_item == "info":
            self.a_propos()

        elif text_item == "aide":
            toast("Désoler, la documentation n'as pas encore été ecrite, faite regulièrement vos mise a jour car elle "
                  "serat bientôt disponible")

        elif text_item == "historique":
            ListeElements.titre = "Historique des recherches"
            ListeElements.is_historique = True
            self.my_app.changer_ecran("liste_elements")

        elif text_item == "aimer":
            ListeElements.titre = "Liste des favoris"
            ListeElements.is_historique = False
            self.my_app.changer_ecran("liste_elements")

        elif text_item == "mode":
            self.my_app.theme_cls.theme_style = "Dark" if self.my_app.theme_cls.theme_style == "Light" else "Light"

        elif text_item == "param":
            self.my_app.changer_ecran("parametres")

        elif text_item == "capture":
            MainScreen.capture_ecran()

        elif text_item == "quiter":
            exit()

    def a_propos(self):
        font_name = self.ids.id_kv_definition.font_name
        font_size = self.ids.id_kv_definition.font_size
        if not self.dialog_a_propos:
            self.dialog_a_propos = MDDialog(
                title="A propos",
                type="custom",
                padding=[0, 0, 0, 0],
                radius=[15, 15, 15, 15],
                height=self.height,
                content_cls=APropos(),
            )

            self.dialog_a_propos.width = self.width_sreen * 0.9
            self.dialog_a_propos.ids.title.font_name = font_name
            self.dialog_a_propos.ids.title.halign = "center"
            self.dialog_a_propos.ids.container.padding = [
                "10dp", "10dp", "-5dp", "10dp"]
        if self.dialog_a_propos.ids.title.font_name != font_name or self.dialog_a_propos.ids.title.font_size != font_size:
            self.dialog_a_propos.ids.title.font_name = font_name
            self.dialog_a_propos.children[0].children[3].font_name = font_name
            self.dialog_a_propos.children[0].children[3].font_size = self.ids.id_kv_definition.font_size
            # TODO : Optimiser le code, voir s'il faut mettre un if ou s'il faut laisser parcourrit tout les elements
            try:
                for i in self.dialog_a_propos.children[0].children[2].children[0].ids.values():
                    i.font_name = font_name
                    i.font_size = font_size
            except Exception as e:
                print("Exeption for in dialog props : ==============>>>>>>", self, e)

        self.dialog_a_propos.open()
