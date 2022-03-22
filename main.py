#!/usr/bin/python3
# coding : utf-8


# bibliothèque propre au language python
from sys import exit

from kivy.core.window import Window
from kivy.effects.scroll import ScrollEffect
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
# from kivy.uix.recycleview import RecycleView
from kivy.uix.screenmanager import ScreenManager  # , WipeTransition  # , NoTransition
from kivy.utils import platform
# from kivy.uix.scrollview import ScrollView
# bibliothèque kivymd
from kivymd.app import MDApp
from kivymd.uix.button import MDIconButton
from kivymd.uix.menu import MDDropdownMenu

# bibliothèque kivy
# from kivymd.uix.toolbar import MDToolbar


# ------------------------ Nouvaux import personnalisé ------------------------#
# Permet d'importer le bon toast en fonction du OS
from kivymd.uix.textfield import MDTextFieldRect

try:
	print("je fait le try")
	# from kivmob import KivMob, TestIds
	from kvdroid import toast  # toast pour android fait en java
except Exception as e:
	print("l'erreur est : ", e)
	from kivymd.toast import toast  # toast pour desktop fait avec kivymd'''

from libs.py.ecran_principal import MainScreen
from libs.py.liste_elements import ListeElements

# from kivymd.uix.button import MDIconButton

# from kivy.uix.scrollview import ScrollView
# from kivy.uix.textinput import TextInput
# from kivymd.uix.navigationdrawer import MDNavigationDrawer
# from kivymd.uix.textfield import MDTextField
# from kivymd.toast import toast
# from kivymd.uix.card import MDCard, MDSeparator

# from kivymd.uix.dialog import MDDialog
# from kivymd.uix.filemanager import MDFileManager
# from kivymd.uix.card import MDCard, MDSeparator

TODO: "Faire en sorte qu'il y ait un retour à la ligne après chaque sens, car un mot peut en avoir plusieur"
TODO: "Faire en sorte qu'un message soit afficher si aucun mot n'est trouver"


class MainApp(MDApp, BoxLayout):
	dialog_a_propos = None
	menu = None
	menu_items = None
	menu_dictionnaire = None
	width_sreen = Window.width
	height_sreen = Window.height
	screen_manager = ScreenManager()

	# ads = KivMob(TestIds.APP)  # C'est ici que serras notre id de pub

	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		# self.menu_items = None
		# self.menu_dictionnaire = None
		# self.screen_manager = ScreenManager()
		self.ripple_color = [0, 0, 1, .1]
		self.effet = ScrollEffect  # l'effet de croll
		Window.bind(on_keyboard=self.on_key_press)


	def build(self):
		Builder.load_file("libs/kv/ecran_principal.kv")
		Builder.load_file("libs/kv/class_personnalisation.kv")
		Builder.load_file("libs/kv/liste_elements.kv")
		# Builder.load_file("libs/kv/ecran_demarrage.kv")
		MainApp.screen_manager.add_widget(MainScreen(name="main_screen"))
		MainApp.screen_manager.add_widget(ListeElements(name="liste_elements"))

		# self.ads.new_banner(TestIds.BANNER, False)
		# self.ads.show_banner()

		return MainApp.screen_manager

	def on_key_press(self, window, key, *args):
		if key == 27 and MainApp.screen_manager.current == "liste_elements":
			self.root_window.children[0].children[0].retour()
			self.changer_ecran(direction="right")
			return True
		if key == 275:  # mot suivant
			MainScreen.mot_suivant()
		if key == 276:  # mot precedent
			MainScreen.mot_precedent()
		return False

	def on_start(self):
		pass

	def on_stop(self):
		print("je suis on stop")

	def on_pause(self):
		print("je fait on pause")
		return True

	def on_resume(self):
		print("on resume")

	@classmethod
	def affiche_menu(cls, button):
		if not cls.menu:
			cls.menu_dictionnaire = {"info": "A propos", "aide": "Aide", "historique": "Historique des recherches",
			                          "aimer": "Liste des favoris", "quiter": "Quiter"}
			cls.menu_items = [
				{
					"viewclass": "OneLineListItem",
					"text": f"{cls.menu_dictionnaire[i]}",
					"height": dp(45),
					"halign": "center",
					"on_release": lambda x=f"{i}": cls.clic_menu(x),
				} for i in cls.menu_dictionnaire
				# Ajouter des icons par la suite
			]
			cls.menu = MDDropdownMenu(
				items=cls.menu_items,
				width_mult=4,
			)
			cls.menu.caller = button
		cls.menu.open()

	@classmethod
	def clic_menu(cls, text_item: str):  # Executer qand on clique sur un element du menu

		cls.menu.dismiss()  # Permet de fermer le menu

		if text_item == "aide":
			toast("Désoler, la documentation n'as pas encore été ecrite, faite regulièrement vos mise a jour car elle "
			      "serat bientôt disponible")
		# Timer(interval=4.5, function=toast,args=["faite regulièrement vos mise a jour car elle serat bientôt
		# disponible"]).start()

		elif text_item in {"historique", "aimer"}:
			ListeElements.titre = cls.menu_dictionnaire[text_item]
			cls.changer_ecran("liste_elements")

		elif text_item == "info":
			MainScreen.a_propos()

		elif text_item == "quiter":
			exit()

		elif text_item == "capture":
			MainScreen.capture_ecran()

	@classmethod
	def changer_ecran(cls, nom_ecran: str = "main_screen", direction: str = "left"):
		"""
		Permet de changer d'ecran, c'est à dire quiter d'un ecran
		vers un autre
		:param: nom_ecran
		:param: direction
		"""
		cls.screen_manager.transition.direction = direction
		cls.screen_manager.current = nom_ecran


if __name__ == '__main__':
	MainApp().run()
