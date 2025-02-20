### Imports ###
from random import randint
import time
from os import system

### Init ###
system("color e")

### Variables ###
personnage = {"Nom": "Gars", "Age": 20, "EXP": 0, "Classe": "Guerrier", "PV": 100, "ATT": 2, "DEF": 1}
inventaire = {"Or": 100}

ennemi = {"Nom": "Slimy", "PV": 80, "ATT": 2, "DEF": 1}

### Fonctions ###
def combat(perso=personnage, enn=ennemi):
	PVp = perso["PV"]
	PVe = enn["PV"]
	ATTp = perso["ATT"]
	ATTe = enn["ATT"]
	DEFp = perso["DEF"]
	DEFe = enn["DEF"]
	taux = 2
	action = 1
	tour = 0
	while PVp > 0 and PVe > 0 and action != 0:
		tour += 1
		print(f"\nTour n°{tour}")
		DEGp = (ATTe - DEFp) * randint(0, 10)
		DEGe = (ATTp - DEFe) * randint(0, 10)
		if DEGp > 0:
			PVp -= DEGp
			print(f"{enn['Nom']} t\'inflige {DEGp} dégâts !")
		else:
			print(f"{enn['Nom']} rate son attaque !")
		if DEGe > 0:
			PVe -= DEGe
			print(f"{perso['Nom']} inflige {DEGe} dégâts !")
		else:
			print(f"{perso['Nom']} rate son attaque !")
		print("PVs restants :")
		print(f"{PVp} VS {PVe}")
		time.sleep(0.5)
		# action = int(input("Voulez-vous continuer ? \n"))
	if PVp > 0:
		result = "Victoire !"
	elif PVe > 0:
		result = "Défaite"
	elif PVp < 0 and PVe < 0:
		result = "Egalité"
	print("\nCombat terminé !")
	return result

### Exécution ###
for i in range(1):
	print(combat())
	time.sleep(0.5)
