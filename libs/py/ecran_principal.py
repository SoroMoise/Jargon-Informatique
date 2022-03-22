from datetime import datetime

from kivy.core.window import Window
from kivy.uix.screenmanager import Screen
from kivy.utils import platform
from kivy.uix.boxlayout import BoxLayout

from kivymd.uix.dialog import MDDialog

from libs.py.class_personnalisation import APropos
from libs.py.interaction_bd import ajouter_mot, purge, mot_aleatoir, interroger_bd, suppreime_mot
try:
	print("je fait le try")
	# from kivmob import KivMob, TestIds
	from kvdroid import toast  # toast pour android fait en java
except Exception as e:
	print("l'erreur est : ", e)
	from kivymd.toast import toast  # toast pour desktop fait avec kivymd'''


class MainScreen(Screen, BoxLayout):
	"""
	Ecrant principal( ecran de demarrage de l'APP )
	"""

	definition = ""
	fermer = ""
	couleur = ""
	menu = None
	numero = 0
	dialog_a_propos = None
	rechercher: bool = True
	width_sreen = Window.width
	le_focus = None

	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		MainScreen.fermer = self.ids.nav_drawer
		MainScreen.definition = self.ids.id_kv_definition
		MainScreen.mot = self.ids.id_kv_mot
		MainScreen.couleur = self.ids.button_aimer
		MainScreen.le_focus = self.ids.nav_drawer.children[0].children[0].children[1].children[1].focus

		Window.bind(on_mouse_down=self.on_mouse)

	def on_mouse(self, obj, x, y, clic, *args):
		if self.ids.nav_drawer.status == "opened" and x <= self.ids.nav_drawer.width:
			self.ids.nav_drawer.enable_swiping = False
		else:
			self.ids.nav_drawer.enable_swiping = True

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

	@classmethod
	def afficher_definition(cls, idmot: str = "", mot: str = "", definition: str = "", faire_requete: bool = False):
		"""
		affiche la definition du mot sur lequel on click dans la zone de recherche
		:param definition: La definition du mot qui doit etre afficher si faire_requete est False
		:param mot: le mot qui doit etre afficher si faire_requete est False
		:param faire_requete: permet de savoir s'il faut faire une requette sur l'idmot pour trouver la definition
		ou qu'elle est dejas donné
		:param idmot: l'id du mot sur lequel on clic
		:return: None
		"""

		cls.vider_ecran()

		if not faire_requete:
			cls.mot.text = mot
			cls.definition.text = purge(definition)
			hist_exist = interroger_bd("id_mot", "historique", f'WHERE id_mot = "{mot.lower()}"')

			if hist_exist:
				suppreime_mot("historique ", f'WHERE id_mot = "{mot.lower()}"')

			ajouter_mot("historique", mot.lower(), str(datetime.today())[:19])

		else:

			resultat = interroger_bd("mot, definition", "dictionnaire", f'WHERE idmot = "{idmot}"')[0]
			cls.afficher_definition(mot=resultat[0], definition=resultat[1])

		if MainScreen.fermer.state == "open":
			MainScreen.fermer.set_state("close")

		cls.aimer()

	@classmethod
	def mot_suivant(cls) -> None:
		cls.vider_ecran()
		mot_actuel = cls.obtenir_id_mot_actuel()
		numero: int = interroger_bd("numero", "dictionnaire ", f"WHERE idmot = '{mot_actuel}'")[0][0]
		if numero < 9559:
			mot: list = interroger_bd("mot, definition", "dictionnaire", f"WHERE numero = '{numero + 1}'")[0]
			cls.mot.text = mot[0]
			cls.definition.text = purge(mot[1])
			cls.aimer()
		else:
			toast("Vous êtes au dernier mot", duration=2)

	@classmethod
	def vider_ecran(cls) -> None:
		try:
			cls.mot.clear_widgets()
			cls.definition.clear_widgets()
		except Exception as e:
			print(f"L'erreur est {e}")

	@classmethod
	def obtenir_id_mot_actuel(cls) -> str:  # permet d'obtenir l'identifiant du mot actuellement afficher a l'ecran
		if cls.mot.text[:16] == "Mot de l'heur : ":
			return cls.mot.text[16:].lower()
		else:
			return cls.mot.text.lower()

	@classmethod
	def aimer(cls, button_aimer: bool = False) -> None:
		"""
		# cette fonction est appeler quand on clieque sur le coeur pour liker ou disliker
		#Elle est aussi appelé quand on fait une recherche aleatoir ou une recherche manuel, elle permet de verifier
		qu'un mot est aimer ou pas et de changer la couleur du coeur en consequence
		:param button_aimer: si cette valeur est a True c'est que le boutton coeur est cliquer et une action specifique
		est faite
		"""
		idmot = cls.obtenir_id_mot_actuel()
		try:  # Si on n'a pas de reponse alors existe est vide et on ne peut donc pas le manipules en tant que liste
			existe = interroger_bd("id_mot", "aimer ", f"WHERE id_mot = '{idmot}'")[0][0]
		except:
			existe = ""

		if existe == idmot:  # si le mot existe
			if button_aimer:
				suppreime_mot("aimer ", f"WHERE id_mot = '{idmot}'")
				cls.couleur.text_color = [1, 1, 1, 1]
			else:
				MainScreen.couleur.text_color = [1, 0, 0, 1]
		elif button_aimer:
			ajouter_mot("aimer", idmot, str(datetime.today())[:19])
			MainScreen.couleur.text_color = [1, 0, 0, 1]
		else:
			MainScreen.couleur.text_color = [1, 1, 1, 1]

	@classmethod
	def recherche_aleatoir(cls) -> None:  # cette fonction permet de faire une recherche aleatoire
		cls.vider_ecran()
		mot = mot_aleatoir()
		cls.mot.text = mot[0]
		cls.definition.text = purge(mot[1])
		cls.aimer()

	@classmethod
	def recherche(cls):  # cette fonction s'execute lorsqu'on clique sur la touche de recherche
		try:
			if cls.fermer.state == "close":
				cls.fermer.set_state("open")

			else:
				MainScreen.fermer.set_state("close")
		# self.ids.nav_drawer.enable_swiping = False
		except ReferenceError:
			toast("Une erreur c'est produit, veillez réessayer !")

	def focus(self) -> None:
		"""
		Permet de metre d'activer le champ de saisie

		:return: None
		"""
		if MainScreen.fermer.state == "close":
			self.ids.nav_drawer.children[0].children[0].children[1].children[1].focus = True

	@classmethod
	def mot_precedent(cls) -> None:
		cls.vider_ecran()
		mot_actuel = cls.obtenir_id_mot_actuel()
		numero: int = interroger_bd("numero", "dictionnaire ", f"WHERE idmot = '{mot_actuel}'")[0][0]
		if numero > 1:
			mot: list = interroger_bd("mot, definition", "dictionnaire", f"WHERE numero = '{numero - 1}'")[0]
			cls.mot.text = mot[0]
			cls.definition.text = purge(mot[1])
			cls.aimer()
		else:
			toast("Vous êtes au prémier mot", duration=2)

	@staticmethod
	def capture_ecran() -> None:
		"""
		Permet de faire une capture d'ecran de l'ecran principale

		:return: None
		"""
		nom = "capture_" + str(str(datetime.today())[:19]) + ".png"
		nom1 = "capture_( 1 )" + str(str(datetime.today())[:19]) + ".png"
		MainScreen.numero += 1
		#print(MainScreen().children[0].children[0].children[0].children[0])

	# MainScreen().children[0].children[0].children[0].children[0].export_to_png(nom)
	# MainScreen().children[0].children[0].export_to_png(nom1)
	# self.get_root_window().export_to_png(nom)

	@classmethod
	def a_propos(cls):  # cette fonction s'execute lorsqu'on clique sur un élément du menue
		# print(self.dialog_ouvert)
		if not cls.dialog_a_propos:
			cls.dialog_a_propos = MDDialog(
				title="A propos",
				opacity=0.7,
				# width_offset=30,
				type="custom",
				padding=[0, 0, 0, 0],
				radius=[45, 45, 45, 45],
				content_cls=APropos(),
			)
			cls.dialog_a_propos.width = cls.width_sreen * 0.9
			print(cls.dialog_a_propos)
			cls.dialog_a_propos.ids.title.font_style = "H4"
			cls.dialog_a_propos.ids.title.halign = "center"
		cls.dialog_a_propos.open()
