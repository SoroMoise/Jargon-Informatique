#!/usr/bin/python3
# coding : utf-8

# bibliothèque propre au language python
from sys import exit

# bibliothèque kivy
from threading import Timer

from kivy.core.window import Window
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
# from kivy.uix.recycleview import RecycleView
from kivy.uix.screenmanager import ScreenManager  # , WipeTransition  # , NoTransition
# from kivy.uix.scrollview import ScrollView
# bibliothèque kivymd
from kivymd.app import MDApp
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.screen import Screen
# from kivymd.uix.toolbar import MDToolbar


# ------------------------ Nouvaux import personnalisé ------------------------#
from kivymd.toast import toast

from libs.py.ecran_principal import MainScreen
from libs.py.liste_elements import ListeElements

# from kivymd.uix.button import MDIconButton

# from kivy.uix.scrollview import ScrollView
# from kivy.uix.textinput import TextInput
# from kivymd.uix.navigationdrawer import MDNavigationDrawer
# from kivymd.uix.textfield import MDTextField
# from kivymd.toast import toast
# from kivymd.uix.card import MDCard, MDSeparator
# from kivymd.uix.label import MDLabel

# from kivymd.uix.dialog import MDDialog
# from kivymd.uix.filemanager import MDFileManager
# from kivymd.uix.card import MDCard, MDSeparator


TODO: "Faire en sorte qu'il y ait un retour à la ligne après chaque sens, car un mot peut en avoir plusieur"
TODO: "Faire en sorte qu'un message soit afficher si aucun mot n'est trouver"


class MainApp(MDApp, BoxLayout, Screen):
	dialog_a_propos = None
	menu = None

	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.screen_manager = ScreenManager()
		self.width_sreen = Window.width
		self.height_sreen = Window.height

	def build(self):
		Builder.load_file("libs/kv/ecran_principal.kv")
		Builder.load_file("libs/kv/class_personnalisation.kv")
		Builder.load_file("libs/kv/liste_elements.kv")
		self.screen_manager.add_widget(MainScreen(name="main_screen"))
		self.screen_manager.add_widget(ListeElements(name="liste_elements"))

		return self.screen_manager

	def on_start(self):
		print("je suis on start")

	def on_stop(self):
		print("je suis on stop")

	def on_pause(self):
		print("je fait on pause")
		return True

	def on_resume(self):
		print("on resume")

	def affiche_menu(self, button):
		if not self.menu:
			self.menu_dictionnaire = {"info": "A propos", "aide": "Aide", "historique": "Historique des recherches",
			                          "aimer": "Liste des favoris", "quiter": "Quiter"}
			self.menu_items = [
				{
					"viewclass": "OneLineListItem",
					"text": f"{self.menu_dictionnaire[i]}",
					"height": dp(45),
					"halign": "center",
					"on_release": lambda x=f"{i}": self.clic_menu(x),
				} for i in self.menu_dictionnaire
				# Ajouter des icons par la suite
			]
			self.menu = MDDropdownMenu(
				items=self.menu_items,
				width_mult=4,
			)
			self.menu.caller = button
		self.menu.open()

	def clic_menu(self, text_item: str):  # Executer qand on clique sur un element du menu
		self.menu.dismiss()  # Permet de fermer le menu
		if text_item == "aide":
			toast("Désoler, la documentation n'as pas encore été faite", background=[0.4, 0.2, 0.2, 1], duration=4.5)
			Timer(interval=4.5, function=toast,
			      args=["faite regulièrement vos mise a jour car \n elle serat bientôt disponible", [0.4, 0.2, 0.2, 1],
			            4.5]).start()
		elif text_item in {"historique", "aimer"}:
			ListeElements.titre = self.menu_dictionnaire[text_item]
			self.changer_ecran("liste_elements")
		elif text_item == "info":
			MainScreen().a_propos()
		elif text_item == "quiter":
			exit()
		elif text_item == "capture":
			MainScreen().capture_ecran()

	def changer_ecran(self, nom_ecran: str = "main_screen", direction: str = "left"):
		"""
		Permet de changer d'ecran, c'est à dire quiter d'un ecran
		vers un autre
		:param: nom_ecran
		"""
		self.screen_manager.transition.direction = direction
		self.screen_manager.current = nom_ecran


if __name__ == '__main__':
	MainApp().run()
