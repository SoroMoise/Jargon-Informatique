#!/usr/bin/python3
# coding : utf-8

# bibliothèque propre au language python
from random import choice
from sqlite3 import connect
from string import ascii_lowercase, digits


connection = connect("src/base_de_donner/dictionnaire.sqlite")
# cursseur permetent de se deplacer dans la base de donnee
curseur = connection.cursor()


def interroger_bd(valeur: str, table: str, condition: str = "") -> list:
	# permet de faire une requêtte à la Base de Donnée
	#                     Example de requete :
	#  Simple : interroger_bd("mot", "dictionnaire", f"WHERE numero = '{numero + 1}'")
	#  complexe : interroger_bd("mot, definition", "dictionnaire", f"WHERE numero = '{numero + 1}'")
	curseur.execute("SELECT " + valeur + " FROM " + table + " " + condition)
	return curseur.fetchall()  # renvoie tout les rerultats de la requette


def ajouter_mot(table, id_mot, date) -> None:
	"""# permet d'ajouter un mot à la base de donnée
	#                     Example de requete :
	#  Simple : ajouter_mot("aimer", idmot, str(datetime.today())[:19])
	#  complexe :"""
	try:
		numero_id = curseur.execute("SELECT numero FROM " + table + " ORDER BY numero DESC LIMIT 1").fetchone()[0] + 1
	except:
		numero_id = 0

	curseur.execute("INSERT INTO " + table + " VALUES(?, ?, ?)", (numero_id, str(id_mot), str(date)))
	connection.commit()


def suppreime_mot(table: str, condition: str = "") -> None:
	"""
	cette fonction permet de supprimer un element dans une table
	:param table: c'est la table dans la quelle serras supprimer l'élément
	:param condition:la condition a remplire pour supprimer l'element
	:return: None
	"""
	curseur.execute("DELETE FROM " + table + condition)
	connection.commit()


def purge(mot: str = "") -> str:
	"""
	# Permet de d'extraire tout element jugé comme unitile (la date, les balises ...) dans la definition
	"""
	if mot[-3:] == "). ":  # Permet d'enlever la date < se trouvent a la fin de la definition
		mot = mot[:-14]

	# Permet de supprimer les elements de la liste
	for i in ["&nbsp;", "&copy;", "€", "<ul>", "</ul>", "<li>", "</li>", "<att>", "</att>", "<i>",
	          "</i>", "<b>", "</b>", "<br>", "<fig>", "</fig>"]:
		mot_temp = mot.split(i)
		mot = ""
		for j in mot_temp:
			mot += j

	return mot


def mot_aleatoir() -> tuple:
	"""
	Cette fonction permet de générer un mot et sa définition en fonction des règles suivantes:
	1: On choisie dans un premier temps un caractère aleatoire parmis 'ascii_lowercase+digits (abc...z+012...9)'
	2: En suite on choisi aleatoirement un mot dans notre base de donnée parmis les 150 premier mot commencant par
		le caractère choisi précédemment
	:return: retourne le mot et sa definition qui est bien sur choisie de façons aleatoire selon les regles precedents
	"""
	mot = str("Mot de l'heur : " + choice(interroger_bd("mot", "dictionnaire ", f"WHERE idmot like \
								'{choice(ascii_lowercase + digits)}%' LIMIT 150"))[0])
	definition = purge(interroger_bd("definition", "dictionnaire ", f"WHERE mot = '{mot[16:]}'")[0][0])

	return mot, definition
