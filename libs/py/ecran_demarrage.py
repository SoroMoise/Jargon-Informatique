#coding: utf-8
from kivy.uix.screenmanager import Screen


class StartScreen(Screen):

	def __init__(self, **kwargs):
		super().__init__(**kwargs)

	def on_enter(self):
		print("je suis sur l'ecrant de demarrage")
