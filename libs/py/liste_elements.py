from threading import Timer

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen
from kivy.utils import platform

# try:
# 	print("je fait le try")
# 	# from kivmob import KivMob, TestIds
# 	from kvdroid import toast  # toast pour android fait en java
# except Exception as e:
# 	print("l'erreur est : ", e)
# 	from kivymd.toast import toast  # toast pour desktop fait avec kivymd'''
from kivymd.toast import toast
from kivymd.uix.button import MDFlatButton, MDRaisedButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.label import MDLabel

from libs.py.interaction_bd import interroger_bd, suppreime_mot


class ListeElements(Screen, BoxLayout):
	nbr = 0
	titre = ""
	
	dialog = None
	element: list = []
	is_historique = None
	
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
	
	def on_enter(self, *args):
		
		self.ids.toolbar.title = ListeElements.titre
		self.ids.id_liste_element.data = []
		if ListeElements.is_historique:
			ListeElements.element = interroger_bd("mot", "historique, dictionnaire",
			                                      "where historique.id_mot = dictionnaire.idmot")
		# ListeElements.is_historique = True
		
		else:
			# ListeElements.is_historique = False
			ListeElements.element = interroger_bd("mot", "aimer, dictionnaire",
			                                      "where aimer.id_mot = dictionnaire.idmot")
		
		if not ListeElements.element:
			self.ecran_est_vide()
		else:
			ListeElements.element.reverse()
			self.add_list()
	
	def add_list(self):
		if ListeElements.element:
			for mot in ListeElements.element:
				self.ids.id_liste_element.data.append(
					{
						"viewclass": "CustomOneLineRightIconListItem",
						"text": mot[0],
						"callback": lambda x: x,
					}
				)
		else:
			self.ecran_est_vide()
	
	def suprimer(self, mot: str) -> None:
		"""
		Permet de supprimer un mot de la liste et de la base de donnée
		:param mot: le mot que lon veut supprimer
		:return: None
		"""
		# toast(str(mot) + " a été supprimer")
		if ListeElements.is_historique:
			# toast(str(mot) + "a été retirer des favoris")
			suppreime_mot("historique", f" where id_mot = '{mot.lower()}'")
			ListeElements.element = interroger_bd("mot", "historique, dictionnaire",
												"where historique.id_mot = dictionnaire.idmot")
			ListeElements.is_historique = True
		else:
			# toast(str(mot) + "a été retirer des favori")
			suppreime_mot("aimer", f" where id_mot = '{mot.lower()}'")
			ListeElements.element = interroger_bd("mot", "aimer, dictionnaire",
												"where aimer.id_mot = dictionnaire.idmot")
		
		ListeElements.element.reverse()
		self.ids.id_liste_element.data = []
		self.add_list()
	
	def vider_contenu(self) -> None:
		"""
		permet d'effacer tout les element de la liste (graphiquement)
		:return: None
		"""
		self.ids.id_liste_element.data = []
		
		self.ids.id_ecran_vid.clear_widgets()
	
	@classmethod
	def vider_bd(cls) -> None:
		"""
		permet de vider la base de donnée
		:return:
		"""
		if cls.titre == "Historique des recherches":
			toast("L'historique des recherche a été vidé")
			suppreime_mot("historique")
		elif ListeElements.titre == "Liste des favoris":
			toast("La liste des favories a été vidé")
			suppreime_mot("aimer")
	
	def retour(self) -> None:
		Timer(0.2, function=self._retour).start()
	
	def _retour(self):
		self.vider_contenu()
		self.ids.toolbar.title = ""
	
	def dialog_tout_supprimer(self) -> None:
		
		if not ListeElements.element:
			toast("La liste etant déja vide, vous ne pouvez donc pas la vider")
		else:
			if not ListeElements.dialog:
				ListeElements.dialog = MDDialog(
					title="Voulez-vous tout supprimer ?",
					text="Cette action supprimeras l'ensemble des mot contenue dans l'historique de "
					     "recherche" if ListeElements.is_historique else "Cette action supprimeras l'ensemble des mot contenue dans "
					                                                     "la liste des favoris",
					opacity=0.7,
					buttons=[
						MDFlatButton(
							text="Annuler",
							on_release=ListeElements.fermer_dialog,
						),
						MDRaisedButton(
							text="Tout supprimer",
							on_release=self.tout_suprimer
						),
					],
				)
			ListeElements.dialog.open()
	
	def tout_suprimer(self, autr="") -> None:
		"""
		permet de fermer le MDDialog, de vider la fenêtre et de se retourner dur l'ecran d'accueil
		:param autr:
		:param obj: l'objet de la touche qui seras cliquer pour executer la fonction
		:return:
		"""
		ListeElements.fermer_dialog()
		self.vider_contenu()
		ListeElements.vider_bd()
		self.ecran_est_vide()
		self.ids.id_liste_element.data = []
		ListeElements.element = ""
	
	# self.add_list()
	
	def ecran_est_vide(self) -> None:
		self.ids.id_ecran_vid.size_hint = (1, 1)
		self.ids.id_liste_element.size_hint = (1, 0)
		
		self.ids.id_ecran_vid.add_widget(
			MDLabel(
				text="L'historique de recherches est vide" if ListeElements.is_historique else "La liste des favoris est vide",
				font_style="H6",
				theme_text_color="Hint",
				halign="center",
			)
		)
	
	@classmethod
	def fermer_dialog(cls, obj="") -> None:
		cls.dialog.dismiss()  # fermer la MDDialog


"""sudo apt-get install zlib1g-dev libsqlite3-dev tk-dev
sudo apt-get install libssl-dev openssl
sudo apt-get install libffi-dev"""
