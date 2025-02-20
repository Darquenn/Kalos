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
personnage = {"Nom": "GARS".upper(), "Age": 20, "Classe": "Guerrier", "EXP": 0, "EXP_MAX": 100, "LVL": 1, "PV": 100, "PV_MAX": 100, "ATT": 5, "DEF": 2, "Chance": 10}
inventaire = {
    "Équipement": {
        "Épée en bois": {
            "Quantité": -1,
            "Description": "C'est juste un bâton. Pourquoi tu gardes ça dans ton inventaire ?",
            "Effet": "+1 ATT",
            "ATT": 1,
            "Symbole": "⚔",
            "Valeur": 0
        },
        "Tunique de noob": {
            "Quantité": -1,
            "Description": "L'armure la plus pourrie. Tu pourrais l'enlever, ça serait pareil...",
            "Effet": "+1 DEF",
            "DEF": 1,
            "Symbole": "🛡",
            "Valeur": 1
        },
    },

    "Objets": {
        "Potion de soin": {
            "Quantité": 1,
            "Description": "Une potion rouge et sucrée. Permet de soigner 20 PV instantanément",
            "Effet": "+20 PV",
            "Type": "Soin",
            "Valeur": 20,
            "Symbole": "❤",
            "Prix": 10
        },
        "Fléchette": {
            "Quantité": 1,
            "Description": "Une pointe aiguisée. Inflige 20 dégâts à l'ennemi",
            "Effet": "20 dégâts",
            "Type": "Dégâts",
            "Valeur": 20,
            "Symbole": "➸",
            "Prix": 10
        },
        "Pierre de santé": {
            "Quantité": 0,
            "Description": "Un caillou magique. Permet de gagner 10 PV MAX",
            "Effet": "+10 PV MAX",
            "Type": "PV MAX",
            "Valeur": 10,
            "Symbole": "❤",
            "Prix": 100
        }
    },

    "Or": 100
    }

slimy = {"Nom": "SLIMY".upper(), "LVL": 1, "EXP": 10, "PV": 100, "PV_MAX": 100, "ATT": 3, "DEF": 2, "Chance": 8, "Description": "Un tas de gelée ou de morve ?"}

### Fonctions ###
def combat(perso=personnage, enn=slimy, inv=inventaire):
    PVp = perso["PV"]
    PVe = enn["PV"]
    ATTp = perso["ATT"]
    ATTe = enn["ATT"]
    DEFp = perso["DEF"]
    DEFe = enn["DEF"]
    NomPerso = perso["Nom"]
    NomEnn = enn["Nom"]
    tour = 0
    EXP = enn["EXP"]

    while PVp > 0 and PVe > 0:
        tour += 1
        progprint(f"\n========= Tour n°{tour} =========")
        progprint(f"{perso['Nom']} : {afficher_barre_sante(PVp, perso['PV_MAX'])}")
        progprint(f"{enn['Nom']} : {afficher_barre_sante(PVe, enn['PV_MAX'])}")

        action = -1
        while action not in [0, 1, 2, 3, 4, 666]:
            progprint("Que veux-tu faire ?")
            progprint("  1) Attaquer")
            progprint(f"  2) Tenter une attaque critique ({2 * perso['Chance']}%)")
            progprint("  3) Se soigner")
            progprint("  4) Inspecter")
            progprint("  0) Fuir")
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
            DEGe = max((ATTp - DEFe) * randint(0, 10), 0)
            if DEGe > 0:
                PVe -= DEGe
                print(f"  {NomPerso} inflige {DEGe} dégâts à {NomEnn} !")
            else:
                print(f"༄ {NomPerso} rate son attaque !")
        
        ### Critique ###
        elif action == 2:
            if randint(1, 100) <= 2 * perso['Chance']:
                DEGe = max((ATTp - DEFe) * randint(1, 10) * 2, 0)
                PVe -= DEGe
                print(f"🗲 Attaque critique réussie ! {NomPerso} inflige {DEGe} dégâts à {NomEnn} !")
            else:
                print(f"༄ Attaque critique ratée ! {NomPerso} perd ton tour.")

        ### Soin ###
        elif action == 3:
            if "Potion de soin" in inv["Objets"] and inv["Objets"]["Potion de soin"]["Quantité"] > 0:
                if PVp < perso['PV']:
                    soin = inv["Objets"]["Potion de soin"]["Soin"]
                    PVp += soin
                    if PVp > perso['PV']:
                        PVp = perso['PV']
                    inv["Objets"]["Potion de soin"]["Quantité"] -= 1
                    print(f"  -1 Potion de soin")
                    print(f"{inv['Objets']['Potion de soin']['Symbole']} {NomPerso} utilise une Potion de soin et récupère {soin} PV !")
                    print(f"  {NomPerso} : {afficher_barre_sante(PVp, perso['PV_MAX'])}")
                else:
                    print(f"{NomPerso} est déjà en pleine forme !")
            else:
                print(f"Oups ! {NomPerso} n'a pas de Potion de soin dans son inventaire.")
                tour -= 1
                continue
        
        # ### Objet ###
        # elif action == 3:
        #     progprint("===== Objets =====")
        #     choix = -1
        #     indice = 1
        #     while choix == -1:
        #         for objet in inv["Objets"].keys():
        #             if inv["Objets"][objet]["Quantité"] > 0:
        #                 print(f"{indice}) {objet} (x{inv['Objets'][objet]['Quantité']})")
        #                 indice += 1
        #         choix = input("Ton choix : ")
        #         if choix.isdigit():
        #             choix = int(choix)
        #         else:
        #             print("## Entre un chiffre valide ##\n")
        #             choix = -1
        #     if "Potion de soin" in inv["Objets"] and inv["Objets"]["Potion de soin"]["Quantité"] > 0:
        #         if PVp < perso['PV']:
        #             soin = inv["Objets"]["Potion de soin"]["Soin"]
        #             PVp += soin
        #             if PVp > perso['PV']:
        #                 PVp = perso['PV']
        #             inv["Objets"][objet]["Quantité"] -= 1
        #             print(f"  -1 {list(objet.keys())[objet]}")
        #             print(f"{objet['Symbole']} {NomPerso} utilise {objet}.")
        #             print(f"{effet}")
        #         else:
        #             print(f"{NomPerso} n'a pas besoin d'utiliser cet objet !")
        #     else:
        #         print("Aucun objet dans l'inventaire")
        #         tour -= 1
        #         continue
        
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
            print(f"༄ {NomPerso} s'enfuit !")
            result = "Défaite par fuite !"
            break

        ### Cheatcode ###
        elif action == 666:
            PVe -= 999999
            print(f"{NomPerso} invoque une force maléfique et inflige 999999 dégâts à {NomEnn} !")
        
        ### Vérif ###
        if PVe <= 0:
            print(f"\n{enn['Nom']} est vaincu !")
            result = "Victoire !"
            EXP += perso["LVL"] * 200
            break

        ## Attaque enn ##
        time.sleep(0.5)
        DEGp = max((ATTe - DEFp) * randint(0, 10), 0)
        if randint(1, 100) <= enn["Chance"]:
            DEGp *= 2
            PVp -= DEGp
            print(f"🗲 {NomEnn} réussit une attaque critique et inflige {DEGp} dégâts à {NomPerso} !")
        else:
            if DEGp > 0:
                PVp -= DEGp
                print(f"  {NomEnn} inflige {DEGp} dégâts à {NomPerso} !")
            else:
                print(f"༄ {NomEnn} rate son attaque !")
        time.sleep(1)

        ### Vérif 2 ###
        if PVp <= 0:
            print(f"\n{perso['Nom']} est vaincu...")
            result = "Défaite !"
            EXP = 0
            break
    
    ### Fin combat ###
    print("\n===== Combat terminé ! =====")
    if result == "Victoire !":
        print(f'{result} Tu as gagné {EXP} XP !')
        perso["EXP"] += EXP
        verifier_niveau()
    else:
        print(f"{result} Tu n'as pas gagné d'XP.")
    return result

def afficher_inventaire(inv=inventaire):
    progprint("\n=== Inventaire ===")
    if "Équipement" in inv:
        progprint("Équipement :")
        for item, details in inv["Équipement"].items():
            if details["Quantité"] == -1:
                progprint(f"  - {item} : {details['Effet']}",2)
            else:
                progprint(f"  - {item} : {details['Effet']} (x{details['Quantité']})",2)
    if "Objets" in inv:
        progprint("Objets :")
        for objet, details in inv["Objets"].items():
            if details["Quantité"] != 0:
                progprint(f"  - {objet} : {details['Effet']} (x{details['Quantité']})",2)
    progprint(f"Or : {inv['Or']}")
    progprint("==================")

def afficher_barre_sante(PV, PV_MAX, long_base=20):
    long = max(long_base, PV_MAX // 5)
    prop = max(0, min(1, PV / PV_MAX))
    rempli = int(prop * long)
    barre = f"[{'█' * rempli}{'░' * (long - rempli)}]"
    return f"{barre} {PV}/{PV_MAX} PV"

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
        print(f"★ {perso['Nom']} passe au niveau {perso['LVL']} !")
        for stat, ex in stats_avant.items():
            new = personnage[stat]
            print(f"  {stat}: {ex} --> {new}")

### Exécution ###
# print("""
# ██╗  ██╗ █████╗ ██╗      ██████╗ ███████╗
# ██║ ██╔╝██╔══██╗██║     ██╔═══██╗██╔════╝
# █████╔╝ ███████║██║     ██║   ██║███████╗
# ██╔═██╗ ██╔══██║██║     ██║   ██║╚════██║
# ██║  ██╗██║  ██║███████╗╚██████╔╝███████║
# ╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝ ╚═════╝ ╚══════╝

# 	Par Darius Georgescu""")
afficher_inventaire()
combat()
