from random import choice
from string import ascii_lowercase, digits

from libs.py.interaction_bd import interroger_bd

from kivy.properties import StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen
from kivymd.uix.card import MDCardSwipe
from kivymd.uix.list import OneLineListItem, OneLineRightIconListItem

definitions = {}


class APropos(BoxLayout):

	def __init__(self, **kwargs):
		super().__init__(**kwargs)

	a_propos = "Jargon Informatique est une application qui vous permettras de naviguer d'une manière conviviale " \
	           "dans un dictionnaire informatique très fournie (plus de 10000 mots). Le dictionnaire contient tout " \
	           "les termes importante du jargon informatique. La base de donnée des mots+explication a été fait " \
	           "par Roland Trique et est distribuè sous licence GNU Free Documentation Licence version 1.1 " \
	           "disponible ici : https://www.gnu.org/licenses/old-licenses/fdl-1.1.html. L'application Jargon " \
	           "Informatique est distrubué sous la licence GNU Public Licence version3 disponible ici : " \
	           "https://www.gnu.org/licenses/gpl-3.0.fr.html. Vous avez donc le doit de le distribuer et de " \
	           "l'utiliser gratuitement. Vous pouvez aussi consulter et ameliorer son code source."


class ContentNavigationDrawer(Screen, BoxLayout):

	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.lettre = choice(ascii_lowercase + digits)
		self.choix = True
		self.mots = {}

	def mot_definition(self, text):
		resultat = interroger_bd("idmot, mot, definition", "dictionnaire ", f"WHERE idmot like '{text}%' LIMIT 150")
		for i in resultat:
			self.mots[i[0]] = i[1]
			#definitions[i[1]] = i[2]

	def voir_list_mots(self, text="", recherche=False, button_recherche=False) -> None:
		"""
		affiche la liste des mots disponible en fonction de la saisie
		:param button_recherche: determine si la navigation drawer a été ouverte a parti de l'icon de recherche
		:param text: c'est le mot en question à rechercher
		:param recherche: l'indicateur qui dit si on a saisie un mot ou pas
		:return: None
		"""

		def ajouter_element(le_mot):
			self.ids.rv.data.append(
				{
					"viewclass": "CustomOneLineListItem",
					"text": le_mot,
					"callback": lambda x: x,
				}
			)

		def afficher(le_mot):
			self.mots = {}
			self.mot_definition(le_mot)
			for element in self.mots:
				ajouter_element(self.mots[element])

		if button_recherche:
			if self.choix:
				self.ids.rv.data = []
				afficher(self.lettre)

		if recherche:
			self.ids.rv.data = []
			self.choix = False
			afficher(text)


class CustomOneLineListItem(OneLineListItem, BoxLayout):
	text = StringProperty()


class CustomOneLineRightIconListItem(BoxLayout):
	text = StringProperty()
