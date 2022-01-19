from threading import Timer

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen
from kivymd.toast import toast
from kivymd.uix.button import MDFlatButton, MDRaisedButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.label import MDLabel

from libs.py.class_personnalisation import CustomOneLineRightIconListItem
from libs.py.interaction_bd import interroger_bd, suppreime_mot


class ListeElements(Screen, BoxLayout):
	nbr = 0
	titre = ""
	dialog = None

	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.element: list = []
		self.is_historique = True

	def on_enter(self, *args):

		def add_list():
			for i in range(len(self.element)):
				self.ids.id_liste_element.add_widget(
					CustomOneLineRightIconListItem(
						text=self.element[i][0],
					)
				)

		self.ids.toolbar.title = ListeElements.titre
		if ListeElements.titre == "Historique des recherches":
			self.is_historique = True
			self.element = interroger_bd("mot", "historique, dictionnaire", "where historique.id_mot = "
			                                                                "dictionnaire.idmot")
			if not self.element:
				self.ecran_est_vide()
			else:
				self.element.reverse()
				add_list()

		elif ListeElements.titre == "Liste des favoris":
			self.is_historique = False
			self.element = interroger_bd("mot", "aimer, dictionnaire", "where aimer.id_mot = dictionnaire.idmot")

			if not self.element:
				self.ecran_est_vide()
			else:
				self.element.reverse()
				add_list()

	def suprimer(self, mot: str) -> None:
		"""
		Permet de supprimer un mot de la liste et de la base de donnée
		:param mot: le mot que lon veut supprimer
		:return: None
		"""
		#toast(str(mot) + " a été supprimer")
		if ListeElements.titre == "Historique des recherches":
			# toast(str(mot) + "a été retirer des favoris")
			suppreime_mot("historique", f" where id_mot = '{mot.lower()}'")
		elif ListeElements.titre == "Liste des favoris":
			# toast(str(mot) + "a été retirer des favori")
			suppreime_mot("aimer", f" where id_mot = '{mot.lower()}'")

	def vider_contenu(self) -> None:
		"""
		permet d'effacer tout les element de la liste (graphiquement)
		:return: None
		"""
		self.ids.id_liste_element.clear_widgets()

	def vider_bd(self) -> None:
		"""
		permet de vider la base de donnée
		:return:
		"""
		if ListeElements.titre == "Historique des recherches":
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

		if not self.element:
			toast(text="La liste etant déja vide, vous ne pouvez donc pas la vider", background=[0.4, 0.2, 0.2, 1], duration=4.5)
		else:
			self.dialog = MDDialog(
				title="Voulez-vous tout supprimer ?",
				text="Cette action supprimeras l'ensemble des mot contenue dans l'historique de "
				     "recherche" if self.is_historique else "Cette action supprimeras l'ensemble des mot contenue dans "
				                                            "la liste des favoris",
				opacity=0.8,
				buttons=[
					MDFlatButton(
						text="Annuler",
						on_release=self.fermer_dialog,
					             ),
					MDRaisedButton(
						text="Tout supprimer",
						on_release=self.tout_suprimer
					),
				],
			)
			self.dialog.open()

	def tout_suprimer(self, obj) -> None:
		"""
		permet de fermer le MDDialog, de vider la fenêtre et de se retourner dur l'ecran d'accueil
		:param obj: l'objet de la touche qui seras cliquer pour executer la fonction
		:return:
		"""
		self.fermer_dialog()
		self.vider_contenu()
		self.vider_bd()
		self.ecran_est_vide()
		self.element = []

	def ecran_est_vide(self) -> None:

		self.ids.id_liste_element.add_widget(
			MDLabel(
				text="L'historique de recherches est vide" if self.is_historique else "La liste des favoris est vide",
				font_style="H6",
				theme_text_color="Hint",
				halign="center",
			)
		)

	def fermer_dialog(self, obj="") -> None:
		self.dialog.dismiss()  # fermer la MDDialog
