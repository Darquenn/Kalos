# coding: utf-8

### Imports ###
from random import randint
import time
from os import system as cmd
import sys


### Init ###
PROGPRINT = False

cmd("color e")
def progprint(text, multi=1, delai=0.01, flag=PROGPRINT):
    if flag:
        delai *= multi
        for carac in text:
            sys.stdout.write(carac)
            sys.stdout.flush()
            time.sleep(delai)
        print()
    else:
        print(text)


### Variables ###
personnage = {
    "Nom": "Gars",
    "Age": 20,
    "Classe": "Guerrier",
    "EXP": 0, "EXP_MAX": 100,
    "LVL": 1,
    "PV": 100, "PV_MAX": 100,
    "ATT": 3, "DEF": 2, "Chance": 10
    }

slimy = {
    "Nom": "Slimy",
    "LVL": 1, "EXP": 20,
    "PV": 30, "PV_MAX": 30,
    "ATT": 3, "DEF": 1, "Chance": 8,
    "Description": "Un tas de gelée ou de morve ?"
    }

squelette = {
    "Nom": "Squelette",
    "LVL": 2, "EXP": 40,
    "PV": 100, "PV_MAX": 100,
    "ATT": 5, "DEF": 2, "Chance": 8,
    "Description": "Un tas d'os articulés"
    }

inventaire = {
    "Équipement": {
        "Épée en bois": {
            "Quantité": -1,
            "Description": "C'est juste un bâton. Pourquoi tu gardes ça dans ton inventaire ?",
            "Effet": "+1 ATT",
            "ATT": 1,
            "Symbole": "⚔",
            "Prix": 5
        },
        "Tunique de noob": {
            "Quantité": -1,
            "Description": "L'armure la plus pourrie. Tu pourrais l'enlever, ça serait pareil...",
            "Effet": "+1 DEF",
            "DEF": 1,
            "Symbole": "🛡",
            "Prix": 5
        },
    },

    "Objets": {
        "Potion de soin": {
            "Quantité": 2,
            "Description": ("Une potion rouge et sucrée.", "Permet de soigner 20 PV instantanément"),
            "Effet": "+20 PV",
            "Type": "Soin",
            "Valeur": 20,
            "Symbole": "❤",
            "Prix": 50
        },
        "Poudre enchantée": {
            "Quantité": 1,
            "Description": ("De la poussière magique.", "Permet de gagner 20 PV MAX temporairement"),
            "Effet": "+20 PV MAX",
            "Type": "PV MAX",
            "Valeur": 20,
            "Symbole": "❤",
            "Prix": 100
        },
        "Fléchette": {
            "Quantité": 1,
            "Description": ("Une pointe aiguisée.", "Inflige 20 dégâts à l'ennemi"),
            "Effet": "20 dégâts",
            "Type": "Dégâts",
            "Valeur": 20,
            "Symbole": "➸",
            "Prix": 50
        }
    },

    "Or": 500
    }


### Fonctions ###
def combat(perso=personnage, enn=slimy, inv=inventaire):
    PVp = perso["PV"]
    PVe = enn["PV"]
    ATTp = perso["ATT"]
    ATTe = enn["ATT"]
    DEFp = perso["DEF"]
    DEFe = enn["DEF"]
    NomPerso = perso["Nom"].upper()
    NomEnn = enn["Nom"].upper()
    ancien_PV_MAX = perso["PV_MAX"]
    tour = 0

    progprint("\n⚔ Le combat commence ! ⚔", 3)
    progprint(f"  {NomPerso} VS {NomEnn}",5)
    time.sleep(1)

    while PVp > 0 and PVe > 0:
        tour += 1
        progprint(f"\n========= Tour n°{tour} =========",0.001)
        progprint(f"{NomPerso} : {afficher_barre(PVp, perso['PV_MAX'])}",0.001)
        progprint(f"{NomEnn} : {afficher_barre(PVe, enn['PV_MAX'])}",0.001)
        action = -1
        while action not in [0, 1, 2, 3, 4, 666]:
            progprint("Que veux-tu faire ?",0.05)
            progprint("  1) Attaque",0.05)
            progprint(f"  2) Attaque critique ({2 * perso['Chance']}%)",0.05)
            progprint("  3) Objet",0.05)
            progprint("  4) Inspection",0.05)
            progprint("  0) Fuite",0.05)
            action = input("Ton choix : ")
            if action.isdigit():
                action = int(action)
            else:
                print("## Entre un chiffre valide ##\n")
                action = -1
        time.sleep(0.5)
        print("")
        
        ### Attaque ###
        if action == 1:
            if ATTp <= DEFe:
                progprint(f"{NomPerso} ne peut pas percer la défense de {NomEnn} !")
            else:
                DEGe = (ATTp - DEFe) * randint(1, 3) + 2
                if DEGe > 0:
                    PVe -= DEGe
                    progprint(f"  {NomPerso} inflige {DEGe} dégâts à {NomEnn} !")
                else:
                    progprint(f"༄ {NomPerso} rate son attaque !")
        
        ### Critique ###
        elif action == 2:
            if ATTp < DEFe:
                progprint(f"༄ {NomPerso} ne peut pas percer la défense de {NomEnn}... Même avec un coup critique !")
            else:
                if randint(1, 100) <= 2 * perso["Chance"]:
                    DEGe = (ATTp - DEFe) * 2 + randint(2, 3)
                    PVe -= DEGe
                    progprint(f"🗲 {NomPerso} réussit une attaque critique et inflige {DEGe} dégâts à {NomEnn} !")
                else:
                    progprint(f"༄ {NomPerso} rate son attaque critique.")
        
        ### Objet ###
        elif action == 3:
            progprint("========== Objets ==========")
            objets_dispos = []
            for objet, details in inv["Objets"].items():
                if details["Quantité"] > 0:
                    objets_dispos.append((objet, details))
            if not objets_dispos:
                progprint("Aucun objet consommable dans votre inventaire.",3)
                progprint("===========================")
                tour -= 1
                continue

            for indice, (nom, details) in enumerate(objets_dispos, 1):
                progprint(f"  {indice}) {nom} (x{details['Quantité']}) - {details['Description'][1]}",3)
            progprint("◄ 0) Revenir",3)

            choix_possibles = [str(i) for i in range(len(objets_dispos) + 1)]
            choix = input("Ton choix : ")
            while choix not in choix_possibles:
                print("## Entre un numéro valide ##\n")
                choix = int(input("Ton choix : "))
            choix = int(choix)
            if choix == 0:
                tour -= 1
                continue
            progprint("===========================")

            objet_nom, objet_details = objets_dispos[choix - 1]
            symbole = objet_details["Symbole"]

            # Soin #
            if objet_details["Type"] == "Soin":
                soin = objet_details["Valeur"]
                if PVp < perso["PV"]:
                    progprint(f"\n  {NomPerso} utilise {objet_nom}.",2)
                    time.sleep(0.5)
                    PVp += soin
                    PVp = min(PVp, perso["PV_MAX"])
                    progprint(f"{symbole} {NomPerso} récupère {soin} PV !",2)
                    progprint(f"  {NomPerso} : {afficher_barre(PVp, perso['PV_MAX'])}")
                else:
                    progprint(f"🖒 {NomPerso} est déjà en pleine forme !",2)
                    tour -= 1
                    continue
            # Dégâts #
            elif objet_details["Type"] == "Dégâts":
                progprint(f"\n  {NomPerso} utilise {objet_nom}.",2)
                time.sleep(0.5)
                DEG = objet_details["Valeur"]
                PVe -= DEG
                progprint(f"{symbole} {enn['Nom']} subit {DEG} dégâts !",2)
            # PV MAX #
            elif objet_details["Type"] == "PV MAX":
                progprint(f"\n  {NomPerso} utilise {objet_nom}.",2)
                time.sleep(0.5)
                ancien_PV_MAX = perso["PV_MAX"]
                bonus_PV_MAX = objet_details["Valeur"]
                perso["PV_MAX"] += bonus_PV_MAX
                progprint(f"{symbole} {NomPerso} gagne {bonus_PV_MAX} PV MAX !",2)
                progprint(f"  {NomPerso} : {afficher_barre(PVp, perso['PV_MAX'])}")
            else:
                progprint("  Cela n'a aucun effet...", 5)

            objet_details["Quantité"] -= 1
            if objet_details["Quantité"] <= 0:
                progprint(f"  Il n'y a plus de {objet_nom}.")
        
        ### Inspection ###
        elif action == 4:
            progprint("=== Informations sur l'ennemi ===",2)
            progprint(f"✱  {enn.get('Nom', '?').upper()}   LVL {enn.get('LVL', '?')}",4)
            progprint(f"✱  ATT {enn.get('ATT', '?')}   DEF {enn.get('DEF', '?')}",4)
            progprint(f"✱  {enn.get('Description', 'Tu ne sais rien sur lui...')}", 5)
            progprint("=================================",2)
            tour -= 1
            time.sleep(1)
            continue

        ### Fuite ###
        elif action == 0:
            progprint(f"༄ {NomPerso} s'enfuit !",2)
            result = "Défaite par fuite !"
            time.sleep(1)
            break

        ### Cheatcode ###
        elif action == 666:
            PVe -= 66666
            progprint(f"{NomPerso} invoque une force maléfique et inflige des dégâts dévastateurs à {NomEnn} !")
        
        ### Vérif ###
        if PVe <= 0:
            progprint(f"\n{enn['Nom']} est vaincu !", 5)
            result = "Victoire !"
            EXP = max(1 + (enn["LVL"] - perso["LVL"]) * 0.5, 0.5) * enn["EXP"]
            time.sleep(1)
            break

        ### Attaque enn ###
        time.sleep(0.5)
        ratio_PVe = PVe / enn["PV_MAX"]
        if ratio_PVe < 0.2 and randint(1, 100):
            print(f"‼ {NomEnn} semble terrifié et tente de fuir !")
            time.sleep(1)
            if randint(1, 100) <= 50:
                print(f"༄ {NomEnn} s'enfuit du combat !")
                result = "Victoire par forfait !"
                EXP = max(1 + (enn["LVL"] - perso["LVL"]) * 0.5, 0.5) * enn["EXP"] / 2
                time.sleep(1)
                break
            else:
                print(f"Ö {NomEnn} panique mais ne parvient pas à fuir.")
                continue
        if ATTe <= DEFp:
            progprint(f"༄ {NomEnn} ne peut pas percer la défense de {NomPerso} !")
        else:
            DEGp = max((ATTe - DEFp) * randint(1, 3) + 1, 0)
            if randint(1, 100) <= enn["Chance"] and DEGp > 0:
                DEGp *= 2
                PVp -= DEGp
                progprint(f"🗲 {NomEnn} réussit une attaque critique et inflige {DEGp} dégâts à {NomPerso} !")
            else:
                if DEGp > 0:
                    PVp -= DEGp
                    progprint(f"  {NomEnn} inflige {DEGp} dégâts à {NomPerso} !")
                else:
                    progprint(f"༄ {NomEnn} rate son attaque !")
        time.sleep(1)

        ### Vérif 2 ###
        if PVp <= 0:
            progprint(f"\n{perso['Nom']} est vaincu...", 5)
            result = "Défaite !"
            EXP = 0
            time.sleep(1)
            break
    
    ### Fin combat ###
    perso["PV_MAX"] = ancien_PV_MAX
    perso["PV"] = min(perso["PV"], perso["PV_MAX"])
    progprint("\n===== Combat terminé ! =====",3)
    if result == "Victoire !":
        progprint(f"{result} {NomPerso} a gagné {int(EXP)} XP !",5)
        perso["EXP"] += EXP
        afficher_barre(perso["EXP"], perso["EXP_MAX"], "EXP")
        verifier_niveau()
    elif result == "Victoire par forfait !":
        progprint(f"{result} {NomPerso} a gagné {int(EXP)} XP !",5)
        perso["EXP"] += EXP / 2
        afficher_barre(perso["EXP"], perso["EXP_MAX"], "EXP")
        verifier_niveau()
    else:
        progprint(f"{result} {NomPerso} n'a pas gagné d'XP.",5)
    return result

### Fonctions combat ###
def action_craintif(enn):
    ratio_PVe = enn["PV"] / enn["PV_MAX"]
    if ratio_PVe < 0.2:
        print(f"  {enn['Nom']} semble terrifié et tente de fuir !")
        if randint(1, 100) <= 50:
            print(f"༄ {enn['Nom']} s'enfuit du combat !")
            return "Fuite"
        else:
            print(f"  {enn['Nom']} panique mais ne parvient pas à fuir.")
            return "Panique"

### Fonctions autres ###
def afficher_inventaire(inv=inventaire):
    progprint("\n=== Inventaire ===")
    if "Équipement" in inv:
        progprint("Équipement :",2)
        for item, details in inv["Équipement"].items():
            if details["Quantité"] == -1:
                progprint(f"  - {item} : {details['Effet']}",2)
            else:
                progprint(f"  - {item} : {details['Effet']} (x{details['Quantité']})",2)
    if "Objets" in inv:
        progprint("Objets :",2)
        for objet, details in inv["Objets"].items():
            if details["Quantité"] != 0:
                progprint(f"  - {objet} : {details['Effet']} (x{details['Quantité']})",2)
    progprint(f"Or : {inv['Or']}",2)
    progprint("==================")

def afficher_barre(stat, stat_MAX, type="PV", long_base=20):
    long = max(long_base, stat_MAX // 5)
    prop = max(0, min(1, stat / stat_MAX))
    rempli = int(prop * long)
    barre = f"[{'█' * rempli}{'░' * (long - rempli)}] {stat}/{stat_MAX}"
    if type == "PV":
        return f"{barre} PV"
    elif type == "EXP":
        return f"{barre} EXP"
    else:
        return barre

def verifier_niveau(perso=personnage):
    while perso["EXP"] >= perso["EXP_MAX"]:
        perso["EXP"] -= perso["EXP_MAX"]
        perso["LVL"] += 1
        perso["EXP_MAX"] = int(perso["EXP_MAX"] * 1.5)
        stats_avant = {
            "PV": personnage["PV"],
            "ATT": personnage["ATT"],
            "DEF": personnage["DEF"],
            "Chance": personnage["Chance"]
        }
        perso["PV"] += 10
        perso["ATT"] += 2
        perso["DEF"] += 1
        perso["Chance"] += 1
        progprint(f"★ {perso['Nom']} passe au niveau {perso['LVL']} !",2)
        for stat, ancienne in stats_avant.items():
            nouvelle = personnage[stat]
            progprint(f"  {stat}: {ancienne} --> {nouvelle}",2)

def village(perso=personnage, inv=inventaire):
    NomPerso = perso["Nom"]
    choix = -1
    while choix not in [1, 2, 3, 4, 0]:
        progprint("\n===== Village =====", 2)
        progprint("1) Mairie", 2)
        progprint("2) Boutique", 2)
        progprint("3) Auberge", 2)
        progprint(f"4) Statistiques de {NomPerso}", 2)
        progprint("0) Quitter le village", 2)
        choix = input("Ton choix : ")
        if choix.isdigit():
            choix = int(choix)
        else:
            print("## Entre un chiffre valide ##\n")
            choix = -1
        time.sleep(0.5)
        print("")
        
        ### Mairie
        if choix == 1:
            progprint(f"{NomPerso} entre dans la mairie.", 2)
            
        ### Boutique
        elif choix == 2:
            progprint(f"{NomPerso} entre dans la boutique.", 2)
        
        ### Auberge
        elif choix == 3:
            progprint(f"{NomPerso} entre dans l'auberge.", 2)
            
            progprint(f"{NomPerso} se repose à l'auberge et récupère tous ses PVs.", 2)
            perso["PV"] = perso["PV_MAX"]
            progprint(f"{NomPerso} : {afficher_barre(perso['PV'], perso['PV_MAX'])}")
            
        ### Statistiques
        elif choix == 4:
            progprint(f"=== Statistiques de {NomPerso} ===", 2)
            progprint(f"✱  {perso.get('Nom', '?').upper()}   LVL {perso.get('LVL', '?')}", 4)
            progprint(f"✱  EXP {perso.get('EXP', '?')} / {perso.get('EXP_MAX', '?')}", 4)
            progprint(f"✱  PV {perso.get('PV', '?')} / {perso.get('PV_MAX', '?')}", 4)
            progprint(f"✱  ATT {perso.get('ATT', '?')}   DEF {perso.get('DEF', '?')}", 4)
            progprint(f"✱  Chance {perso.get('Chance', '?')}", 4)
            progprint("=================================", 2)
            
        ### Quitter
        elif choix == 0:
            progprint("Tu quittes le village.", 2)
        
        time.sleep(1)

### Exécution ###
print("""
██╗  ██╗ █████╗ ██╗      ██████╗ ███████╗
██║ ██╔╝██╔══██╗██║     ██╔═══██╗██╔════╝
█████╔╝ ███████║██║     ██║   ██║███████╗
██╔═██╗ ██╔══██║██║     ██║   ██║╚════██║
██║  ██╗██║  ██║███████╗╚██████╔╝███████║
╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝ ╚═════╝ ╚══════╝
""")
progprint("	Par Darius Georgescu",5)
afficher_inventaire()
village()
for i in range(1):
    combat()