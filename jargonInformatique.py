#!/usr/bin/python3
# coding : utf-8

# bibliothèque propre au language python
from sqlite3 import connect
from string import ascii_lowercase, digits
from random import choice

# bibliothèque kivy
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, NoTransition
from kivy.uix.scrollview import ScrollView
#from kivy.uix.textinput import TextInput

# bibliothèque kivymd
from kivymd.app import MDApp
from kivymd.uix.list import OneLineListItem
from kivymd.uix.navigationdrawer import MDNavigationDrawer
#from kivymd.uix.textfield import MDTextField
#from kivymd.toast import toast
#from kivymd.uix.button import MDIconButton
#from kivymd.uix.card import MDCard, MDSeparator
#from kivymd.uix.label import MDLabel
#from kivymd.uix.dialog import MDDialog
#from kivymd.uix.filemanager import MDFileManager
from kivymd.uix.screen import Screen
#from kivymd.uix.card import MDCard, MDSeparator


#cree une connection a la base de donnee

definitions = {}


def get(valeur, condition=""):
	connection = connect("base_de_donner/dictionnairetest.sqlite")
	# cursseur permetent de se deplacer dans la base de donnee
	curseur = connection.cursor()
	# permet de faire une requêtte à la Base de Donnée
	curseur.execute("SELECT " + valeur + " FROM dictionnaire " + condition)
	return curseur.fetchall()  # renvoie tout les rerultats de la requette


def purge(mot):
	# Permet d'extraire la date
	if mot[-3:] == "). ":
		mot = mot[:-14]

	# Permet de supprimer les elements de la liste
	for j in ["&nbsp;", "€", "<ul>", "</ul>", "<li>", "</li>", "<att>", "</att>"]:
		mot_temp = mot.split(j)
		mot = ""
		for i in mot_temp:
			mot += i

	return mot


def mot_aleatoir():
	"""
	Cette fonction permet de générer un mot et sa définition en fonction des règles suivantes:
	1: On choisie dans un premier temps un caractère aleatoire parmis 'ascii_lowercase+digits (abc...z+012...9)'
	2: En suite on choisi aleatoirement un mot dans notre base de donnée parmis les 150 premier mot commencant par
		le caractère choisi précédemment
	:return: retourne le mot et sa definition qui est bien sur choisie de façons aleatoire selon les regles precedents
	"""
	mot = str("Mot de l'heur : " + choice(get("mot", f"WHERE idmot like \
								'{choice(ascii_lowercase + digits)}%' LIMIT 150"))[0])
	definition = purge(get("definition", f"WHERE mot = '{mot[16:]}'")[0][0])

	return mot, definition


class ItemsScreen(BoxLayout):
	pass


class ResultatScreen(Screen, BoxLayout):
	pass


class EcranSaisie(Screen, BoxLayout):
	focus = StringProperty()


class MainScreen(Screen, BoxLayout):
	"""
	Ecrant principal( ecran de demarrage de l'APP )
	"""
	mot = ""
	definition = ""
	fermer = ""

	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		MainScreen.fermer = self.ids.nav_drawer
		MainScreen.definition = self.ids.id_kv_definition
		MainScreen.mot = self.ids.id_kv_mot

		# J'ais appliqué un retour a la ligne car selon la 'PEP8: E501' une ligne ne doit pas exceder 120 caractères
		MainApp().recherche_aleatoir()


class CustomOneLineListItem(OneLineListItem):
	text = StringProperty()


class ContentNavigationDrawer(Screen, BoxLayout):

	focus = ""

	def __init__(self, **kwargs):
		super().__init__(**kwargs)

		#ContentNavigationDrawer.focus = self.ids.search_field

	def voir_list_most(self, text="", recherche=False):
		"""
		affiche la liste des mots disponible en fonction de la saisie
		:param text: c'est le mot en question à rechercher
		:param recherche: l'indicateur qui dit si on a saisie un mot ou pas
		:return:
		"""
		les_mots = get("idmot, mot, definition", f"WHERE idmot like '{text}%' LIMIT 150")
		mots = {}
		for _ in les_mots:
			mots[_[0]] = _[1]
			definitions[_[1]] = _[2]

		def ajouter_element(le_mot):
			self.ids.rv.data.append(
				{
					"viewclass": "CustomOneLineListItem",
					"text": le_mot,
					"callback": lambda x: x,
				}
			)

		self.ids.rv.data = []

		for mot in mots:
			if recherche:
				if text in mot:
					ajouter_element(mots[mot])
			else:
				ajouter_element(mots[mot])

		TODO: "Faire en sorte qu'un mmessage soit afficher si aucun mot n'est trouver"


class MainApp(MDApp, BoxLayout, Screen):

	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.screen_manager = ScreenManager()
		Window.bind(on_keyboard=self.events)

	def build(self):
		Builder.load_file("jargonkv.kv")
		self.screen_manager.add_widget(MainScreen(name="main_screen"))
		self.screen_manager.add_widget(EcranSaisie(name="ecran_saisie"))
		self.screen_manager.add_widget(ResultatScreen(name="resultat_screen"))

		return self.screen_manager

	def on_start(self):
		print("on_start")

	def on_stop(self):
		print("on_stop")

	@staticmethod
	def menu():
		print("je click sur menue")

	def events(self, keyboard, instance, keycode, text, modifiers):
		"""Called when buttons are pressed on the mobile device.

		# cette fonction est appeler a chaque touche de clavier
		# On pourais l'utiliser pour d'eventuelle racourci clavier
		# print("Un evenement ...")"""

	def changer_ecran(self, nom_ecran: str, direction: str = "left"):
		"""
		Permet de changer d'ecran, c'est à dire quiter d'un ecran
		vers un autre
		"""
		#self.screen_manager.transition.direction = NoTransition()
		self.screen_manager.current = nom_ecran

	def vider_ecran(self):
		MainScreen.mot.clear_widgets()
		MainScreen.definition.clear_widgets()

	def afficher_definition(self, idmot=""):
		"""
		affiche la definition du mot sur lequel on click dans la zone de recherche
		:param idmot: l'id du mot sur lequel on clic
		:return:
		"""
		MainScreen.fermer.set_state("close")
		self.vider_ecran()
		MainScreen.mot.text = idmot
		MainScreen.definition.text = purge(definitions[idmot])

	def text_field(self):
		print("je suis dans text field")
		#ContentNavigationDrawer.focus.focus = True
		ContentNavigationDrawer().voir_list_most()

	def recherche_aleatoir(self):
		self.vider_ecran()
		mot = mot_aleatoir()
		MainScreen.mot.text = mot[0]
		MainScreen.definition.text = purge(mot[1])


if __name__ == '__main__':
	MainApp().run()
	print("Fermeture du programme ...")
