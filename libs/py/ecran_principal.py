from datetime import datetime

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen
from kivymd.toast import toast
from kivymd.uix.dialog import MDDialog

from libs.py.class_personnalisation import ContentNavigationDrawer, definitions, APropos
from libs.py.interaction_bd import ajouter_mot, purge, mot_aleatoir, interroger_bd, suppreime_mot


class MainScreen(Screen, BoxLayout):
	"""
	Ecrant principal( ecran de demarrage de l'APP )
	"""
	mot = ""
	definition = ""
	fermer = ""
	couleur = ""
	numero = 0
	dialog_a_propos = None

	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.rechercher: bool = True
		MainScreen.fermer = self.ids.nav_drawer
		MainScreen.definition = self.ids.id_kv_definition
		MainScreen.mot = self.ids.id_kv_mot
		MainScreen.couleur = self.ids.button_aimer

	def obtenir_id_mot_actuel(self) -> str:  # permet d'obtenir l'identifiant du mot actuellement afficher a l'ecran
		if MainScreen.mot.text[:16] == "Mot de l'heur : ":
			return MainScreen.mot.text[16:].lower()
		else:
			return MainScreen.mot.text.lower()

	def aimer(self, button_aimer: bool = False) -> None:
		"""
		# cette fonction est appeler quand on clieque sur le coeur pour liker ou disliker
		#Elle est aussi appelé quand on fait une recherche aleatoir ou une recherche manuel, elle permet de verifier
		qu'un mot est aimer ou pas et de changer la couleur du coeur en consequence
		:param button_aimer: si cette valeur est a True c'est que le boutton coeur est cliquer et une action specifique
		est faite
		"""
		idmot = self.obtenir_id_mot_actuel()
		try:  # Si on n'a pas de reponse alors existe est vide et on ne peut donc pas le manipules en tant que liste
			existe = interroger_bd("id_mot", "aimer ", f"WHERE id_mot = '{idmot}'")[0][0]
		except:
			existe = ""

		if existe == idmot:  # si le mot existe
			if button_aimer:
				suppreime_mot("aimer ", f"WHERE id_mot = '{idmot}'")
				MainScreen.couleur.text_color = [1, 1, 1, 1]
			else:
				MainScreen.couleur.text_color = [1, 0, 0, 1]
		elif button_aimer:
			ajouter_mot("aimer", idmot, str(datetime.today())[:19])
			MainScreen.couleur.text_color = [1, 0, 0, 1]
		else:
			MainScreen.couleur.text_color = [1, 1, 1, 1]

	def afficher_definition(self, idmot: str = "", mot: str = "", definition: str = "", faire_requete: bool = False):
		"""
		affiche la definition du mot sur lequel on click dans la zone de recherche
		:param definition: La definition du mot qui doit etre afficher si faire_requete est False
		:param mot: le mot qui doit etre afficher si faire_requete est False
		:param faire_requete: permet de savoir s'il faut faire une requette sur l'idmot pour trouver la definition
		ou qu'elle est dejas donné
		:param idmot: l'id du mot sur lequel on clic
		:return: None
		"""

		self.vider_ecran()

		if not faire_requete:
			MainScreen.mot.text = mot
			MainScreen.definition.text = purge(definition)
			hist_exist = interroger_bd("id_mot", "historique", f"WHERE id_mot = '{mot.lower()}'")

			if hist_exist:
				suppreime_mot("historique ", f"WHERE id_mot = '{mot.lower()}'")

			ajouter_mot("historique", mot.lower(), str(datetime.today())[:19])

		else:

			resultat = interroger_bd("mot, definition", "dictionnaire", f"WHERE idmot = '{idmot}'")[0]
			self.afficher_definition(mot=resultat[0], definition=resultat[1])

		if MainScreen.fermer.state == "open":
			MainScreen.fermer.set_state("close")

		self.aimer()

	def vider_ecran(self) -> None:
		MainScreen.mot.clear_widgets()
		MainScreen.definition.clear_widgets()

	def recherche_aleatoir(self) -> None:  # cette fonction permet de faire une recherche aleatoire
		self.vider_ecran()
		mot = mot_aleatoir()
		MainScreen.mot.text = mot[0]
		MainScreen.definition.text = purge(mot[1])
		self.aimer()

	def mot_suivant(self) -> None:
		self.vider_ecran()
		mot_actuel = self.obtenir_id_mot_actuel()
		numero: int = interroger_bd("numero", "dictionnaire ", f"WHERE idmot = '{mot_actuel}'")[0][0]
		if numero < 9559:
			mot: list = interroger_bd("mot, definition", "dictionnaire", f"WHERE numero = '{numero + 1}'")[0]
			MainScreen.mot.text = mot[0]
			MainScreen.definition.text = purge(mot[1])
			self.aimer()
		else:
			toast("Vous êtes au dernier mot", duration=2)

	def mot_precedent(self) -> None:
		self.vider_ecran()
		mot_actuel = self.obtenir_id_mot_actuel()
		numero: int = interroger_bd("numero", "dictionnaire ", f"WHERE idmot = '{mot_actuel}'")[0][0]
		if numero > 1:
			mot: list = interroger_bd("mot, definition", "dictionnaire", f"WHERE numero = '{numero - 1}'")[0]
			MainScreen.mot.text = mot[0]
			MainScreen.definition.text = purge(mot[1])
			self.aimer()
		else:
			toast("Vous êtes au prémier mot", duration=2)

	def recherche(self):  # cette fonction s'execute lorsqu'on clique sur la touche de recherche
		print("recher")
		if MainScreen.fermer.state == "close":
			MainScreen.fermer.set_state("open")
		else:
			MainScreen.fermer.set_state("close")

	def on_enter(self) -> None:
		if self.rechercher:
			self.recherche_aleatoir()
			self.rechercher = False

	def capture_ecran(self) -> None:
		"""
		Permet de faire une capture d'ecran de l'ecran principale

		:return: None
		"""
		nom = "capture_" + str(str(datetime.today())[:19]) + ".png"
		nom1 = "capture_( 1 )" + str(str(datetime.today())[:19]) + ".png"
		MainScreen.numero += 1
		print(MainScreen().children[0].children[0].children[0].children[0])
		#MainScreen().children[0].children[0].children[0].children[0].export_to_png(nom)
		#MainScreen().children[0].children[0].export_to_png(nom1)
		#self.get_root_window().export_to_png(nom)

	def a_propos(self):  # cette fonction s'execute lorsqu'on clique sur un élément du menue
		if not self.dialog_a_propos:
			self.dialog_a_propos = MDDialog(
				title="A propos",
				opacity=0.8,
				#width_offset=30,
				type="custom",
				content_cls=APropos(),
			)
		self.dialog_a_propos.open()

	def appel(self):
		print("Je suis dans l'écran principal")
