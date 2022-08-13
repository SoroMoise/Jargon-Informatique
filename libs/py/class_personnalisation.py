from os import path
from random import choice
from string import ascii_lowercase, digits

# from kivymd.uix.navigationdrawer import MDNavigationDrawer
from time import time

# from kivy.uix.recycleboxlayout import RecycleBoxLayout
# from kivy.uix.recycleview import RecycleView

from kivymd.toast import toast
from kivymd.uix.card import MDSeparator

from libs.py.interaction_bd import interroger_bd
# from kivy.utils import escape_markup

from kivy.properties import StringProperty, NumericProperty, ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen
from kivy.core.window import Window
# from kivymd.uix.card import MDCardSwipe
from kivymd.uix.list import OneLineListItem  # , OneLineRightIconListItem

definitions = {}


class MySep(MDSeparator):
	"""le separateur se trouvant dans A propos"""
	pass


class APropos(BoxLayout):
	width_sreen = Window.width
	height_sreen = Window.height
	
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
	
	a_propos = "Jargon Informatique est une application qui vous permettras de naviguer d'une manière conviviale " \
	           "dans un dictionnaire informatique très fournie (plus de 10000 mots). Le dictionnaire contient tout " \
	           "les termes importante du jargon informatique. La base de donnée des mots+explication a été fait " \
	           "par Roland Trique et est distribuè sous licence GNU Free Documentation Licence version 1.1 " \
	           "disponible ici : [color=3333aa]https://www.gnu.org/licenses/old-licenses/fdl-1.1.html[/color]. " \
	           "L'application Jargon Informatique est distrubué sous la licence GNU Public Licence version3 disponible " \
	           "ici : [color=3333aa]https://www.gnu.org/licenses/gpl-3.0.fr.html[/color]. Vous avez donc le doit de le " \
	           "distribuer et de l'utiliser gratuitement. Vous pouvez aussi consulter et ameliorer son code source."


def lettre():
	"""
	retourn une lettre choisis aléatoirement
	"""
	return choice(ascii_lowercase + digits)


class ContentNavigationDrawer(BoxLayout):
	mots = []
	
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		# self.lettre = choice(ascii_lowercase + digits)
		
		# self.choix est a True si on n'a pas encore fait de saisie et qu'on entre pour la premiere foix dans la
		# NavigationDrewer
		self.choix = True
	
	@classmethod
	def mot_definition(cls, text):
		# TODO: Pas besoin de tout recuperer, on peut get seulment le mot au lieu de ' idmot, mot, definition(DÉJA FAIT)
		debut = interroger_bd("mot", "dictionnaire", f'WHERE idmot like "{text}%" LIMIT 150')
		tout = []
		long = len(debut)
		if long < 150:
			tout = interroger_bd("mot", "dictionnaire ", f'WHERE idmot like "%{text}%" LIMIT {150-long}')
			
			# Permet d'extraire les elements de 'debut' dans 'tout'
			for i in debut:
				if i in tout:
					tout.pop(tout.index(i))
					
		cls.mots = debut + tout
	
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
			ContentNavigationDrawer.mots = []
			self.mot_definition(le_mot)
			for value in ContentNavigationDrawer.mots:
				ajouter_element(value[0])
		
		if button_recherche:
			if self.choix:
				self.ids.rv.data = []
				afficher(choice(f"{ascii_lowercase}{digits}"))
				self.choix = False
		
		if recherche:
			# self.ids.rb.clear_widgets()
			self.ids.rv.data = []
			self.choix = False
			afficher(text)
	
	def text_validate(self):
		try:
			self.parent.parent.parent.afficher_definition(idmot=ContentNavigationDrawer.mots[0],
															faire_requete=True)
		except:
			toast("Aucun mot n'a été trouvé")


class CustomOneLineListItem(OneLineListItem, BoxLayout):
	text = StringProperty()
	my_app = ObjectProperty()
	
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.ids._lbl_primary.font_name = self.my_app.my_font


class CustomOneLineRightIconListItem(BoxLayout):
	text = StringProperty()


class ContenRef(BoxLayout):
	width_sreen = Window.width
	height_sreen = Window.height
	definition = ""
