#!/usr/bin/python3
# coding : utf-8

# bibliothèque propre au language python
import cProfile
import io
import pstats
from random import choice
from sqlite3 import connect
from string import ascii_lowercase, digits
from sys import exit

# from time import time

try:
	connection = connect("src/base_de_donner/dictionnaire.sqlite")
	curseur = connection.cursor()
except Exception as e:
	print("une erreur c'est produite, le code de l'erreur est --> : ", e)
	exit("Erreur lier a la base de donnée")


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

def interroger_bd(valeur: str, table: str = "dictionnaire", condition: str = "") -> list:
	"""
	print(f"la requette est SELEC")
	permet de faire une requêtte à la Base de Donnée
						Example de requete :
	Simple : interroger_bd("mot", "dictionnaire", f"WHERE numero = '{numero + 1}'")
	complexe : interroger_bd("mot, definition", "dictionnaire", f"WHERE numero = '{numero + 1}'")
	request = "SELECT " + valeur + " FROM
	"""
	curseur.execute(f"SELECT {valeur} FROM {table} {condition}")
	
	# j'essayais de regler le probleme des requette où le idmot contient de " ' " EX:"serveur d'application"
	# if condition == "":
	# 	curseur.execute('SELECT ? FROM ?', valeur, table)
	# else:
	# 	curseur.execute(f"SELECT {valeur} FROM {table} {condition}")
	return curseur.fetchall()  # renvoie tout les rerultats de la requette


def ajouter_mot(table, id_mot, date) -> None:
	"""# permet d'ajouter un mot à la base de donnée
	# Example de requete :
	#  Simple : ajouter_mot("aimer", idmot, str(datetime.today())[:19])
	#  complexe :"""
	try:
		numero_id = curseur.execute(f"SELECT numero FROM {table} ORDER BY numero DESC LIMIT 1").fetchone()[0] + 1
	except Exception:
		numero_id = 0
	
	curseur.execute(f"INSERT INTO {table} VALUES(?, ?, ?)", (numero_id, str(id_mot), str(date)))
	connection.commit()


def suppreime_mot(table: str, condition: str = "") -> None:
	"""
	cette fonction permet de supprimer un element dans une table
	:param table: c'est la table dans la quelle serras supprimer l'élément
	:param condition:la condition a remplire pour supprimer l'element
	:return: None
	"""
	curseur.execute(f"DELETE FROM {table}{condition}")
	connection.commit()


def purge(mot: str = "") -> str:
	"""
	# Permet de d'extraire tout element jugé comme inutile (la date, les balises ...) dans la definition
	"""
	ajouter = True
	debut = 1
	if mot.endswith("). "):  # if mot[-3:] == "). ": Permet d'enlever la date < se trouvent a la fin de la definition
		mot = mot[:-14]
	
	# Permet de supprimer les elements de la liste
	l1 = ["&nbsp;", "&copy;", "€", "<ul>", "</ul>", "<li>", "</li>", "<att>", "</att>", "&lt;", "&gt;"]
	listes = ["<i>", "</i>", "<b>", "</b>", "<br>", "<fig>", "</fig>", "<B>", "</B>"] + l1
	for i in listes:
		mot_temp = str(mot).split(i)
		# print(mot_temp, "---pour----", i)
		mot = ""
		for j in mot_temp:
			if i == "€":
				if debut == 1:
					mot += j
					debut += 1
				elif ajouter:
					mot += f"[ref={j}][u][color=3333ff][b]{j}[/b][/color][/u][/ref]"
					ajouter = False
				else:
					mot += j
					ajouter = True
			elif i == "<b>":
				mot += f"[b]{j}[/b]"  # La mise en gras ne fonctionne pas à cause de la police
			else:
				mot += j
	# print("JE SUIS A LA FIN\n\n")
	return mot


def mot_aleatoir() -> tuple:
	"""
	NB : la politique a légèrement changer, et j'ai la flème de réécrire toute la DOC
	
	Cette fonction permet de générer un mot et sa définition en fonction des règles suivantes:
	1: On choisie dans un premier temps un caractère aleatoire parmis 'ascii_lowercase+digits (abc...z+012...9)'
	2: En suite on choisi aleatoirement un mot dans notre base de donnée parmis les 150 premier mot commencant par
		le caractère choisi précédemment
	:return : retourne le mot et sa definition qui est bien sur choisie de façons aleatoire selon les regles precedents
	mot = str("Mot de l'heur : " + choice(interroger_bd("mot", "dictionnaire ", f"WHERE idmot like \
								'{choice(ascii_lowercase + digits)}%' LIMIT 150"))[0])
	request = f"SELECT mot FROM dictionnaire WHERE idmot like '{choice(ascii_lowercase + digits)}%' LIMIT 150"
	#print("la requette est ", request)
	mot = str(choice(curseur.execute(request).fetchall()))
	
	#print(interroger_bd("definition", "dictionnaire", f" WHERE mot = '{mot[16:]}'"))
	definition = purge(interroger_bd("definition", "dictionnaire", f" WHERE mot = '{mot[16:]}'"))
	print(f"le retout {mot}, {definition}")
	"""
	idmot = choice(interroger_bd(valeur="idmot", table="dictionnaire",
	                             condition=f'where idmot like "%{choice(ascii_lowercase + digits)}%"')[0])
	if len(idmot) <= 150:
		mot, definition = interroger_bd(valeur='mot, definition', table='dictionnaire',
		                                condition=f'WHERE idmot = "{idmot}"')[0]
	
	return mot, definition
