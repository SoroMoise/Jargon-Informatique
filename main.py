# bibliothèque propre au language python
import cProfile
import io
import pstats
from os import path
from time import time

from kivy.core.window import Window
from kivy.effects.scroll import ScrollEffect
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.properties import ColorProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.utils import platform, get_color_from_hex
from kivymd.app import MDApp
from kivymd.color_definitions import colors

from libs.module.statusbarcolor import change_statusbar_color
from libs.module.variable import my_fonts
from libs.py.ecran_parametre import EcranParam
from libs.py.ecran_principal import MainScreen
from libs.py.liste_elements import ListeElements
from libs.py.screenmanager import screen_manager

# TODO: Faire en sorte qu'il y ait un retour à la ligne après chaque sens, car un mot peut en avoir plusieur
# TODO: Faire en sorte qu'un message soit afficher si aucun mot n'est trouver (DÉJA FAIT)
# TODO: Il y a des mot qui sont dans la definition mais qui ne son pas dans la bese de données, et dand on clic \
#  dessus ca crée une erreur
# TODO: les parametres à sauvegarger: theme, font_size, open_clic_mode, statut_bar_color(peut etre determiner)
# TODO: J'ai utiliser des polices sans regardrer leur licences, je doit donc revoir avant une publication
#  officiel de l'app.
# font_dir = path.dirname(__file__) + "/src/font/"


def profile(fct):
	"""
	Le decorateur
	"""
	def inner(*args, **kwargs):
		pr = cProfile.Profile()
		pr.enable()
		retval = fct(*args, **kwargs)
		pr.disable()
		s = io.StringIO()
		sortby = "cumulative"
		ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
		ps.print_stats()
		print(s.getvalue())
		return retval
	return inner


class MainApp(MDApp, BoxLayout):
	dialog_a_propos = None
	menu = None
	menu_items = None
	menu_dictionnaire = None
	width_sreen = Window.width
	height_sreen = Window.height
	my_font_size = dp(20)
	my_scroll_type = ['bars', 'content']
	my_bar_width = 10
	my_bar_margin = dp(-10)
	my_user_font_size = "35dp"
	my_theme_color = ColorProperty()
	
	# ads = KivMob(TestIds.APP)  # C'est ici que serras notre id de pub
	
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		# self.menu_items = None
		# self.menu_dictionnaire = None
		# self.screen_manager = ScreenManager()
		self.title = "Jargon Informatique"
		self.my_font_style = None
		self.ripple_color = self.theme_cls.primary_dark
		self.effet = ScrollEffect  # l'effet de croll
		self.my_font = f"{path.dirname(__file__)}/src/font/{my_fonts[5]}"
		
		Window.bind(on_keyboard=self.on_key_press)
		Window.bind(on_mouse_down=self.on_mouse)
	
	def build(self):
		# TODO: "verifier s'il est possible de de charger les ecrans après le demmarage pour reduire le temps de chargement"
		self.theme_cls.primary_palette = "Blue"
		self.theme_cls.primary_hue = "600"
		self.theme_cls.material_style = "M3"
		self.theme_cls.theme_style = "Light"  # Light/Dark
		self.changer_couleur_bar_statut(self.theme_cls.primary_palette)
		# MainApp.my_theme_color = get_color_from_hex(colors[self.theme_cls.primary_palette][self.theme_cls.primary_hue])
		# print("le code couleur est ", MainApp.my_theme_color)
		self.d = time()
		Builder.load_file("libs/kv/ecran_principal.kv")
		Builder.load_file("libs/kv/class_personnalisation.kv")
		Builder.load_file("libs/kv/liste_elements.kv")
		Builder.load_file("libs/kv/ecran_parametre.kv")
		# Builder.load_file("libs/kv/ecran_demarrage.kv")
		screen_manager.add_widget(MainScreen(name="main_screen"))
		screen_manager.add_widget(ListeElements(name="liste_elements"))
		screen_manager.add_widget(EcranParam(name="parametres"))
		return screen_manager
	
	def on_start(self):
		print("on_start")
		print("Le temps de chargement est : ", time()-self.d)
	
	def on_stop(self):
		print("on_stop")
	
	def on_pause(self):
		print("on_pause")
		return True
	
	def on_resume(self):
		print("on_resume")
	
	def on_key_press(self, window, key, *args):
		if platform not in {'android', 'ios'}:  # ces raccourcis ne sont pas utiles sur mobile
			if key == 275:  # mot suivant
				MainScreen.mot_suivant()
			elif key == 276:  # mot precedent
				MainScreen.mot_precedent()
			elif key == 112:  # ecran de parametre
				self.changer_ecran(nom_ecran="parametres")
			elif key == 109:  # changer de theme
				if self.theme_cls.theme_style == "Light":
					self.theme_cls.theme_style = "Dark"
				else:
					self.theme_cls.theme_style = "Light"
		
		if key == 27 and screen_manager.current != "main_screen":
			if screen_manager.current == "liste_elements":
				self.root_window.children[0].children[0].retour()
			self.changer_ecran(direction="right")
			return True
		return False

	def changer_police(self, police: str):
		"""
		Permet de changer la police de l'app sans rédemarrer
		"""
		font = f"{path.dirname(__file__)}/src/font/{police}"
		screen_manager.get_screen("main_screen").ids.id_kv_mot.font_name = font  # Le mot à definir
		screen_manager.get_screen("main_screen").ids.id_kv_definition.font_name = font  # la delefition
		
		# Applique la police à tout les MDLabel
		ps = screen_manager.get_screen("parametres").ids  # parametres screen
		try:
			# TODO: verifier que la police est appliqué uniquement au MDLabel et non a toutes les class
			for idps in ps.values():
				idps.font_name = font
		except Exception as e:
			print(e)
		
		# Permet de changer dynamiquement le nom de la police
		ps.police_lb.text = font.split("/")[-1]
		
		# Applique la police aux MonButtonTheme
		for card in ps.pal_card.children:
			card.ids.text_btn.font_name = font
	
	def changer_taille(self, taille):
		"""
		Permet de changer la taille du texte de l'app sans rédemarrer
		"""
		screen_manager.get_screen("main_screen").ids.id_kv_mot.font_size = taille  # Le mot à definir
		screen_manager.get_screen("main_screen").ids.id_kv_definition.font_size = taille  # la delefition
		
		# Applique la police à tout les MDLabel
		ps = screen_manager.get_screen("parametres").ids  # parametres screen
		try:
			for idps in ps.values():
				idps.font_size = taille
		except Exception as e:
			print(e)
		
		# Permet de changer dynamiquement le nom de la police
		ps.taille_lb.text = taille
		
		# Applique la police aux MonButtonTheme
		for card in ps.pal_card.children:
			card.ids.text_btn.font_size = taille
	
	"""
	def metre_gras(self, gras: bool = True):
		'''
		Impossible de mettre le texte en gras care elle depend de la police
		'''
		if screen_manager.get_screen("parametres").ids.gras_lb.text == "Non":
			screen_manager.get_screen("parametres").ids.gras_lb.text = "Oui"
			screen_manager.get_screen("parametres").ids.gras_lb.bold = True
			gras = True
		else:
			screen_manager.get_screen("parametres").ids.gras_lb.text = "Non"
			screen_manager.get_screen("parametres").ids.gras_lb.bold = False
			gras = False
		print(screen_manager.get_screen("main_screen").ids.id_kv_mot.bold)
		screen_manager.get_screen("main_screen").ids.id_kv_mot.bold = gras  # Le mot à definir
		print(screen_manager.get_screen("main_screen").ids.id_kv_mot.bold)
		screen_manager.get_screen("main_screen").ids.id_kv_definition.bold = gras  # la delefition
		
		# Applique la police à tout les MDLabel
		ps = screen_manager.get_screen("parametres").ids  # parametres screen
		try:
			for idps in ps.values():
				idps.bold = gras
		except Exception as e:
			print(e)
		
		# Permet de changer dynamiquement le nom de la police
		
		# Applique la police aux MonButtonTheme
		for card in ps.pal_card.children:
			card.ids.text_btn.bold = gras
	"""
	def changer_couleur_bar_statut(self, color, icons_color="Light"):
		couleur = get_color_from_hex(colors[color][self.theme_cls.primary_hue])
		change_statusbar_color(couleur, icons_color)

	def on_mouse(self, *args):
		pass
	
	
	@classmethod
	def changer_ecran(cls, nom_ecran: str = "main_screen", direction: str = "left") -> None:
		"""
		Permet de changer d'ecran, c'est à dire quiter d'un ecran
		vers un autre
		:param: nom_ecran
		:param: direction
		:return: None
		"""
		screen_manager.transition.direction = direction
		screen_manager.current = nom_ecran


if __name__ == '__main__':
	MainApp().run()
