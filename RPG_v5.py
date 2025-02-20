# coding: utf-8

### Imports ###
from random import randint, choice
import time
from os import system as cmd
import sys
try:
    from pygame import mixer
except ModuleNotFoundError:
    print("⚠ Le module 'pygame' n'est pas installé.")
    print("  Veuillez l'installer avec la commande : pip install pygame")
    exit()

### Init ###
SONS_ACTIVES = True
PROGPRINT = False

cmd("color e")

mixer.init()
sons = {}
fichiers_sons = {
    "Voix": "sounds/voice.ogg",
    "Chip": "sounds/chip.ogg",
    "Tidum": "sounds/tidum.ogg",
    "EXP": "sounds/exp.ogg",
    "LevelUp1": "sounds/levelup1.ogg",
    "LevelUp2": "sounds/levelup2.ogg",
    "Attaque1": "sounds/swing1.ogg",
    "Attaque2": "sounds/swing2.ogg",
    "Attaque3": "sounds/swing3.ogg",
    "Epée": "sounds/swordhit.ogg",
    "Critique1": "sounds/crit1.ogg",
    "Critique2": "sounds/crit2.ogg",
    "Hit1": "sounds/hit1.ogg",
    "Hit2": "sounds/hit2.ogg",
    "Hit3": "sounds/hit3.ogg",
    "Rate": "sounds/miss.ogg",
    "Reflect": "sounds/reflect.ogg",
    "Slimy1": "sounds/slimy1.ogg",
    "Slimy2": "sounds/slimy1.ogg",
    "Squelette1": "sounds/skeleton1.ogg",
    "Squelette2": "sounds/skeleton2.ogg",
    "Squelette3": "sounds/skeleton3.ogg",
    "Squelette4": "sounds/skeleton4.ogg",
    "Encounter1": "sounds/encounter1.ogg",
    "Encounter2": "sounds/encounter2.ogg",
    "Alerte": "sounds/alert.ogg",
    "Mort": "sounds/dust.ogg",
    "Victoire": "sounds/win.ogg",
    "Défaite": "sounds/defeat.ogg",
    "Fuite": "sounds/flee.ogg",
    "Pièce": "sounds/coin.ogg",
    "Potion": "sounds/drink.ogg",
    "DrinkGasp": "sounds/drinkgasp.ogg",
    "Fléchette1": "sounds/dart1.ogg",
    "Fléchette2": "sounds/dart2.ogg",
    "Fléchette3": "sounds/dart3.ogg",
    "Magie": "sounds/magic.ogg",
    "Choeur": "sounds/choir.ogg",
    "Poison": "sounds/poison.ogg",
    "Splash": "sounds/splash.ogg",
    "Demon": "sounds/demon.ogg",
}
for nom, directory in fichiers_sons.items():
    try:
        sons[nom] = mixer.Sound(directory)
    except FileNotFoundError:
        print(f"⚠ Fichier son introuvable : {directory}. Le son '{nom}' sera désactivé.")
        sons[nom] = None
def playsound(nom, nb=0):
    if nb == 0:
        i = 1
        while sons.get(f"{nom}{i}"):
            i += 1
        nb = i - 1
    if nb > 0:
        nom += str(randint(1, nb))
    if SONS_ACTIVES and sons.get(nom):
        sons[nom].play()
    elif not sons.get(nom):
        print(f"⚠ Son '{nom}' introuvable ou désactivé.")

def progprint(text, multi=1, delai=0.01, flag=PROGPRINT, voix=False):
    if flag:
        delai *= multi
        for carac in text:
            if voix:
                playsound("Voix")
            sys.stdout.write(carac)
            sys.stdout.flush()
            time.sleep(delai)
        print()
    else:
        print(text)


### Variables ###
personnage = {
    "Nom": "Darawen",
    "Age": 20,
    "Classe": "Guerrier",
    "EXP": 0, "EXP_MAX": 100,
    "LVL": 1,
    "PV": 100, "PV_MAX": 100,
    "EN": 20, "EN_MAX": 20,
    "ATT": 3, "DEF": 2, "Chance": 10,
    "BONUS": {
        "PV_MAX": 0,
        "ATT": 0,
        "DEF": 0,
        "Chance": 0
    }
    }

inventaire = {
    "Équipement": {
        "Épée en bois": {
            "Quantité": -1,
            "Description": ("C'est juste un bâton.", "Octroie 1 ATT."),
            "Effet": "+1 ATT",
            "ATT": 1,
            "Symbole": "⚔",
            "Prix": 5
        },
        "Tunique de noob": {
            "Quantité": -1,
            "Description": ("L'armure la plus pourrie.", "Octroie 1 DEF."),
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

ennemis = {
    "Slimy": {
        "Nom": "Slimy",
        "LVL": 1, "EXP": 20,
        "PV": 30, "PV_MAX": 30,
        "ATT": 3, "DEF": 1, "Chance": 8,
        "Description": "Un tas de gelée ou de morve ?"
        },

    "Squelette": {
        "Nom": "Squelette",
        "LVL": 2, "EXP": 40,
        "PV": 100, "PV_MAX": 100,
        "ATT": 5, "DEF": 2, "Chance": 8,
        "Description": "Un tas d'os articulés"
        },
    }

PNJs = {
    "Aubergiste": {
        "Nom": "Balthar",
    },
    
    "Marchand": {
        "Nom": "Elowen",
    },
}

prenoms = ["Alaric", "Balthar", "Cedric", "Darael", "Elowen", "Faelar", "Gwendal", "Havren", "Iriel", "Jorvik"]

### Fonctions ###
def combat(perso=personnage, enn=ennemis[choice(list(ennemis.keys()))], inv=inventaire):
    PVp = perso["PV"]
    PVe = enn["PV"]
    ATTp = perso["ATT"]
    ATTe = enn["ATT"]
    DEFp = perso["DEF"]
    DEFe = enn["DEF"]
    NomPerso = perso["Nom"].upper()
    NomEnn = enn["Nom"].upper()
    tour = 0

    playsound("Encounter1")
    progprint("⚔ Le combat commence ! ⚔", 3)
    progprint(f"  {NomPerso} VS {NomEnn}",5)
    print()
    time.sleep(1)

    while PVp > 0 and PVe > 0:
        tour += 1
        progprint(f"========= Tour n°{tour} =========",0.001)
        progprint(f"{NomPerso} : {afficher_barre(PVp, perso['PV_MAX'])}",0.001)
        progprint(f"{NomEnn} : {afficher_barre(PVe, enn['PV_MAX'])}",0.001)
        action = -1
        actions = [0, 1, 2, 3, 4, 5, 666]
        while action not in actions:
            progprint("Que veux-tu faire ?",0.05)
            progprint("  1) Attaque",0.05)
            progprint(f"  2) Attaque critique ({2 * perso['Chance']}%)",0.05)
            progprint("  3) Objet",0.05)
            progprint("  4) Inspection",0.05)
            progprint("  5) Passer",0.05)
            progprint("◄ 0) Fuite",0.05)
            action = input("Ton choix : ")
            if action.isdigit():
                action = int(action)
                if action not in actions:
                    playsound("Chip")
                    print("## Entre un chiffre valide ##\n")
                    action = -1
            else:
                playsound("Chip")
                print("## Entre un chiffre valide ##\n")
                action = -1
            time.sleep(0.5)
        time.sleep(0.5)
        print()
        
        ### Attaque ###
        if action == 1:
            if ATTp <= DEFe:
                progprint(f"🛡 {NomPerso} ne peut pas percer la défense de {NomEnn} !")
                playsound("Attaque")
                playsound("Reflect")
            else:
                DEGe = (ATTp - DEFe) * randint(1, 3) + 2
                if DEGe > 0:
                    PVe -= DEGe
                    progprint(f"  {NomPerso} inflige {DEGe} dégâts à {NomEnn} !")
                    playsound("Attaque")
                    playsound("Epée")
                    
                else:
                    progprint(f"༄ {NomPerso} rate son attaque !")
                    playsound("Attaque")
                    playsound("Rate")
        
        ### Critique ###
        elif action == 2:
            if ATTp < DEFe:
                progprint(f"🛡 {NomPerso} ne peut pas percer la défense de {NomEnn}... Même avec un coup critique !")
                playsound("Attaque")
                playsound("Reflect")
            else:
                if randint(1, 100) <= 2 * perso["Chance"]:
                    DEGe = (ATTp - DEFe) * 2 + randint(2, 3)
                    PVe -= DEGe
                    progprint(f"🗲 {NomPerso} réussit une attaque critique et inflige {DEGe} dégâts à {NomEnn} !")
                    playsound("Attaque")
                    playsound("Epée")
                    playsound("Critique")
                else:
                    progprint(f"༄ {NomPerso} rate son attaque critique.")
                    playsound("Attaque")
                    playsound("Rate")
        
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
                playsound("Chip")
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
                if PVp < perso["PV_MAX"]:
                    progprint(f"\n  {NomPerso} utilise {objet_nom}.",2)
                    time.sleep(0.5)
                    PVp += soin
                    PVp = min(PVp, perso["PV_MAX"])
                    playsound("Potion")
                    playsound("Magie")
                    progprint(f"{symbole} {NomPerso} récupère {soin} PV !",2)
                    progprint(f"  {NomPerso} : {afficher_barre(PVp, perso['PV_MAX'])}",0.001)
                else:
                    progprint(f"🖒 {NomPerso} est déjà en pleine forme !",2)
                    tour -= 1
                    time.sleep(0.5)
                    continue
            # Dégâts #
            elif objet_details["Type"] == "Dégâts":
                playsound(objet_nom)
                progprint(f"\n  {NomPerso} utilise {objet_nom}.",2)
                time.sleep(0.5)
                DEG = objet_details["Valeur"]
                PVe -= DEG
                playsound("Attaque")
                progprint(f"{symbole} {enn['Nom']} subit {DEG} dégâts !",2)
            # PV MAX #
            elif objet_details["Type"] == "PV MAX":
                progprint(f"\n  {NomPerso} utilise {objet_nom}.",2)
                time.sleep(0.5)
                bonus_PV_MAX = objet_details["Valeur"]
                perso["BONUS"]["PV_MAX"] += bonus_PV_MAX
                perso["PV_MAX"] = calculer_bonus(perso, "PV_MAX")
                playsound("Magie")
                progprint(f"{symbole} {NomPerso} gagne {bonus_PV_MAX} PV MAX !",2)
                progprint(f"  {NomPerso} : {afficher_barre(PVp, perso['PV_MAX'])}",0.001)
            else:
                playsound("Chip")
                progprint("  Cela n'a aucun effet...", 5)

            objet_details["Quantité"] -= 1
            if objet_details["Quantité"] <= 0:
                time.sleep(1)
                playsound("Chip")
                progprint(f"  Il n'y a plus de {objet_nom}.")
        
        ### Inspection ###
        elif action == 4:
            playsound("Encounter2")
            progprint("=== Informations sur l'ennemi ===",2)
            progprint(f"✱  {enn.get('Nom', '?').upper()}   LVL {enn.get('LVL', '?')}",4)
            progprint(f"✱  ATT {enn.get('ATT', '?')}   DEF {enn.get('DEF', '?')}",4)
            progprint(f"✱  {enn.get('Description', 'Tu ne sais rien sur lui...')}", 5)
            progprint("=================================",2)
            tour -= 1
            time.sleep(1)
            continue
        
        ### Passer ###
        elif action == 5:
            playsound("Chip")
            dialogues = [
            f"(・―・) {NomPerso} décide de passer son tour.",
            f"(╭ರ_•́)  {NomPerso} prend une pause pour réfléchir.",
            f"(⊙︿⊙)  {NomPerso} observe attentivement {NomEnn}.",
            f"(◡̀_◡́)ᕤ  {NomPerso} se prépare pour le prochain coup.",
            f"(￢_￢) {NomPerso} reste sur ses gardes."
            ]
            progprint(f"  {choice(dialogues)}", 2)
            time.sleep(1)

        ### Fuite ###
        elif action == 0:
            playsound("Fuite")
            progprint(f"༄ {NomPerso} s'enfuit !",2)
            result = "Défaite par fuite !"
            time.sleep(1)
            break

        ### Cheatcode ###
        elif action == 666:
            PVe -= 66666
            playsound("Demon")
            progprint(f"𖤐  {NomPerso} invoque une force maléfique et inflige des dégâts dévastateurs à {NomEnn} !")
            time.sleep(1)
        
        ### Vérif ###
        if PVe <= 0:
            playsound("Mort")
            progprint(f"\n{enn['Nom']} est vaincu !", 5)
            result = "Victoire !"
            EXP = max(1 + (enn["LVL"] - perso["LVL"]) * 0.5, 0.5) * enn["EXP"]
            time.sleep(3)
            break
  
        ### Fuite enn ###
        time.sleep(1)
        ratio_PVe = PVe / enn["PV_MAX"]
        if ratio_PVe < 0.2:
            playsound("Alerte")
            progprint(f"‼ {NomEnn} semble terrifié et tente de fuir !")
            time.sleep(1)
            seuil_fuite = 30 + enn["Chance"] - perso["Chance"]
            if randint(1, 100) <= seuil_fuite:
                playsound("Fuite")
                progprint(f"༄ {NomEnn} s'enfuit du combat !")
                result = "Victoire par forfait !"
                EXP = max(1 + (enn["LVL"] - perso["LVL"]) * 0.5, 0.5) * enn["EXP"] / 2
                time.sleep(1.5)
                break
            else:
                playsound("Rate")
                progprint(f"Ö {NomEnn} panique mais ne parvient pas à fuir.")
                continue

        ### Attaque enn ###
        if ATTe <= DEFp:
            playsound("Reflect")
            progprint(f"🛡 {NomEnn} ne peut pas percer la défense de {NomPerso} !")
        else:
            DEGp = max((ATTe - DEFp) * randint(1, 3) + 1, 0)
            critique = randint(1, 100) <= enn["Chance"]
            esquive = randint(1, 100) <= perso["Chance"]
            if critique and not esquive:
                DEGp *= 2
                PVp -= DEGp
                playsound(enn["Nom"])
                playsound("Critique", 2)
                progprint(f"🗲 {NomEnn} réussit une attaque critique et inflige {DEGp} dégâts à {NomPerso} !")
            elif esquive:
                playsound("Rate")
                progprint(f"༄ {NomPerso} esquive l'attaque de {NomEnn} !")
            elif DEGp > 0:
                PVp -= DEGp
                playsound(enn["Nom"])
                progprint(f"  {NomEnn} inflige {DEGp} dégâts à {NomPerso} !")
            else:
                playsound("Rate")
                progprint(f"༄ {NomEnn} rate son attaque !")

        time.sleep(1)
        print()

        ### Vérif 2 ###
        if PVp <= 0:
            playsound("Hit3")
            playsound("Mort")
            progprint(f"\n{perso['Nom']} est vaincu...", 5)
            result = "Défaite !"
            EXP = 0
            time.sleep(3)
            break
    
    ### Fin combat ###
    progprint("\n===== Combat terminé ! =====",3)
    if result == "Victoire !":
        playsound("Victoire")
        playsound("EXP")
        progprint(f"{result} {NomPerso} a gagné {int(EXP)} XP !",5)
        perso["EXP"] += EXP
        time.sleep(1)
        print(f"{NomPerso} : {afficher_barre(perso['EXP'], perso['EXP_MAX'], 'EXP')}")
        verifier_niveau(perso)
    elif result == "Victoire par forfait !":
        playsound("Victoire")
        playsound("EXP")
        EXP /= 2
        progprint(f"{result} {NomPerso} a gagné {int(EXP)} XP !",5)
        perso["EXP"] += EXP
        time.sleep(1)
        print(f"{NomPerso} : {afficher_barre(perso['EXP'], perso['EXP_MAX'], 'EXP')}")
        verifier_niveau(perso)
    else:
        playsound("Défaite")
        progprint(f"{result} {NomPerso} n'a pas gagné d'XP.",5)
        time.sleep(1)
    if any(perso["BONUS"].values()):
        reinitialiser_bonus(perso)
        for stat in ["PV_MAX", "ATT", "DEF", "Chance"]:
            perso[stat] = calculer_bonus(perso, stat)
        PVp = min(PVp, perso["PV_MAX"])
    perso["PV"] = PVp
    time.sleep(1)


### Fonctions de combat ###
def debut_combat(perso=personnage, cout_EN=5):
    NomPerso = perso["Nom"]
    BONUS_actifs = 0
    for type, valeur in perso["BONUS"].items():
        if type != "PV_MAX":
            BONUS_actifs += valeur
    cout_EN += BONUS_actifs
    if perso["EN"] < cout_EN:
        progprint(f"{NomPerso} est épuisé et n'a plus assez d'EN pour se battre.",5)
        return False
    else:
        perso["EN"] -= cout_EN
        progprint(f"{NomPerso} engage un combat !  -{cout_EN} EN",5)
        if BONUS_actifs > 0:
            progprint(f"Les pouvoirs actifs de {NomPerso} drainent {BONUS_actifs} points d'énergie supplémentaires.",5)
        progprint(f"{perso['EN']}/{perso['EN_MAX']} EN",5)
        return True

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
    barre = f"[{'█' * rempli}{'░' * (long - rempli)}] {int(stat)}/{stat_MAX}"
    if type == "PV":
        return f"{barre} PV"
    elif type == "EN":
        return f"{barre} EN"
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
        playsound("LevelUp1")
        progprint(f"★ {perso['Nom']} passe au niveau {perso['LVL']} !",2)
        time.sleep(0.25)
        for stat, ancienne in stats_avant.items():
            nouvelle = personnage[stat]
            progprint(f"  {stat}: {ancienne} --> {nouvelle}",2)
            time.sleep(0.25)
        time.sleep(0.5)

def calculer_bonus(perso, stat):
    return perso[stat] + perso["BONUS"].get(stat, 0)

def reinitialiser_bonus(perso, stats=None):
    if stats is None:
        stats = perso["BONUS"].keys()
    for stat in stats:
        if stat in perso["BONUS"]:
            perso["BONUS"][stat] = 0
    progprint(f"{perso['Nom']} ressent une rechute d'énergie.", 2)
    
def dormir(perso=personnage, type_chambre="dehors", dérangé=False, inv=inventaire):
    if type_chambre == "dehors":
        recup = 5
        progprint(f"{perso['Nom']} s'endort craintivement...", 5)
        time.sleep(1)
    elif type_chambre == "normale" or type_chambre == "campement":
        recup = 10
        progprint(f"{perso['Nom']} s'endort tranquillement...", 5)
        time.sleep(1)
    elif type_chambre == "royale":
        recup = 20
        progprint(f"{perso['Nom']} s'endort paisiblement...", 5)
        time.sleep(1)
    if dérangé:
        recup //= 2
    perso["EN"] = min(perso["EN"] + recup, perso["EN_MAX"])
    if not dérangé:
        progprint("ᶻ 𝘇𐰁", 50)
        playsound("LevelUp2")
        progprint(f"{perso['Nom']} s'est bien reposé et récupère {recup} EN.")
        time.sleep(1)
    else:
        progprint("ᶻ 𝗓!", 50)
        playsound("Alerte")
        progprint(f"{perso['Nom']} se réveille brusquement ! (+{recup} EN)")
    progprint(afficher_barre(perso['EN'], perso['EN_MAX'], 'EN'))
    
def choisir_prenom(pnj, prenoms=prenoms):
    pnj["Nom"] = choice(prenoms)


### Village ###
def village(perso=personnage, inv=inventaire):
    NomPerso = perso["Nom"]
    choix = -1
    while choix not in [1, 2, 3, 4, 5, 0]:
        progprint("\n===== Village =====", 0.001)
        progprint("  1) Mairie", 2)
        progprint("  2) Boutique", 2)
        progprint("  3) Auberge", 2)
        progprint("  4) Fontaine", 2)
        progprint(f"  5) Statistiques de {NomPerso}", 2)
        progprint("◄ 0) Quitter le village", 2)
        choix = input("Ton choix : ")
        if choix.isdigit():
            choix = int(choix)
        else:
            playsound("Chip")
            print("## Entre un chiffre valide ##\n")
            choix = -1
        print()
        time.sleep(0.5)
        
        ### Mairie
        if choix == 1:
            mairie()
            
        ### Boutique
        elif choix == 2:
            boutique()
        
        ### Auberge
        elif choix == 3:
            auberge()
            
        ### Fontaine
        elif choix == 4:
            fontaine()   
                        
        ### Statistiques
        elif choix == 5:
            afficher_stats(perso)
            afficher_inventaire(inv)
            
        ### Quitter
        elif choix == 0:
            playsound("Fuite")
            progprint(f"{NomPerso} quitte le village.", 2)
            break
        
        choix = -1

### Mairie ###
def mairie(perso=personnage, inv=inventaire):
    NomPerso = perso["Nom"]
    playsound("Fuite")
    progprint(f"{NomPerso} entre dans la mairie.", 2)
    time.sleep(1)

### Boutique ###
def boutique(perso=personnage, inv=inventaire):
    NomPerso = perso["Nom"]
    playsound("Fuite")
    progprint(f"{NomPerso} entre dans la boutique.", 2)
    time.sleep(1)
    choix = -1
    NomMarch = PNJs["Marchand"]["Nom"].upper()

### Auberge ###
def auberge(perso=personnage, inv=inventaire):
    NomPerso = perso["Nom"]
    playsound("Fuite")
    progprint(f"{NomPerso} entre dans l'auberge.", 2)
    time.sleep(1)
    choix = -1
    NomAuberg = PNJs["Aubergiste"]["Nom"].upper()
    progprint(f"{NomAuberg} : Bienvenue à l'auberge, {NomPerso} ! Je suis {NomAuberg.capitalize()} l'Aubergiste.", 2, voix=True)
    time.sleep(1)
    progprint(f"{NomAuberg} : Nous avons deux types de chambres disponibles.", 2, voix=True)
    time.sleep(1)
    progprint(f"{NomAuberg} : Une chambre normale pour 10 pièces d'OR qui vous offre un sommeil réparateur.", 2, voix=True)
    time.sleep(1)
    progprint(f"{NomAuberg} : Ou une chambre royale pour 20 pièces d'OR qui vous offre un sommeil divin.", 2, voix=True)
    time.sleep(1)
    while choix not in [0, 1, 2]:
        progprint("  1) Chambre normale - (10 OR)", 2)
        progprint("  2) Chambre royale - (20 OR)", 2)
        progprint("◄ 0) Revenir", 2)
        progprint(f"{inv['Or']} OR", 2)
        choix = input("Ton choix : ")
        if choix.isdigit():
            choix = int(choix)
        else:
            playsound("Chip")
            print("## Entre un chiffre valide ##")
            choix = -1
        print()
        time.sleep(0.5)
        
        ### Chambre normale ###
        if choix == 1:
            if inv["Or"] >= 10:
                inv["Or"] -= 10
                progprint(f"{NomPerso} se repose dans une chambre normale et récupère tous ses PVs.", 2)
                perso["PV"] = perso["PV_MAX"]
                playsound("Potion")
                progprint(f"{NomPerso} : {afficher_barre(perso['PV'], perso['PV_MAX'])}")
            else:
                playsound("Chip")
                progprint(f"{NomAuberg} : Désolé ! Il semble que vous n'avez pas assez d'or pour une chambre normale.", 2)
        
        ### Chambre royale ###
        elif choix == 2:
            if inv["Or"] >= 20:
                inv["Or"] -= 20
                playsound("Potion")
                progprint(f"{NomPerso} se repose dans une chambre royale, récupère tous ses PVs et gagne 10 PV MAX temporaires !", 2)
                perso["BONUS"]["PV_MAX"] = 10
                perso["PV"] = calculer_bonus(perso, "PV_MAX")
                progprint(f"{NomPerso} : {afficher_barre(perso['PV'], calculer_bonus(perso, 'PV_MAX'))}")
            else:
                playsound("Chip")
                progprint(f"{NomAuberg} : Désolé ! Il semble que vous n'avez pas assez d'or pour une chambre royale.", 2)
        
        ### Quitter ###
        elif choix == 0:
            progprint(f"{NomAuberg} : Au revoir et à bientôt !", 2, voix=True)
            playsound("Fuite")
            progprint(f"{NomPerso} sort de l'auberge.", 2)
            break
        
        choix = -1
        time.sleep(1)

### Fontaine ###
def fontaine(perso=personnage, inv=inventaire):
    NomPerso = perso["Nom"]
    OrPerso = inv["Or"]
    choix = -1
    playsound("Fuite")
    progprint(f"{NomPerso} arrive devant la fontaine.", 2)
    while choix not in [1, 2, 3, 0]:
        time.sleep(1)
        progprint("\n=== Fontaine ===", 0.001)
        progprint("  1) Se laver le visage", 2)
        progprint("  2) Boire l'eau", 2)
        progprint("  3) Jeter une pièce", 2)
        progprint("◄ 0) Revenir au village", 2)
        choix = input("Ton choix : ")
        if choix.isdigit():
            choix = int(choix)
        else:
            playsound("Chip")
            print("## Entre un chiffre valide ##")
            choix = -1
        print()
        time.sleep(0.5)
        
        ### Se laver le visage
        if choix == 1:
            playsound("Splash")
            progprint(f"{NomPerso} se lave le visage et se sent rafraîchi.", 2)
        
        ### Boire l'eau
        elif choix == 2:
            playsound("Splash")
            playsound("Potion")
            progprint(f"{NomPerso} boit l'eau de la fontaine.", 2)
            time.sleep(1)
            if randint(1, 3) == 1:
                soin = randint(5, 10)
                playsound("DrinkGasp")
                progprint(f"Elle est bonne ! {NomPerso} récupère {soin} PVs.", 2)
                perso["PV"] = min(perso["PV"] + soin, perso["PV_MAX"])
            else:
                DEG = randint(5, 10)
                playsound("Poison")
                progprint(f"Elle est mauvaise ! {NomPerso} perd {DEG} PVs.", 2)
                perso["PV"] -= DEG
            progprint(f"{NomPerso} : {afficher_barre(perso['PV'], perso['PV_MAX'])}",0.001)
            
        ### Jeter une pièce
        elif choix == 3:
            if OrPerso >= 1:
                playsound("Pièce")
                progprint(f"{NomPerso} jette une pièce dans la fontaine.", 2)
                OrPerso -= 1
                inv["Or"] = OrPerso
                time.sleep(1)
                if randint(1, 10) * perso["Chance"] >= 0:
                    playsound("Choeur")
                    progprint(f"La fontaine brille légèrement et {NomPerso} sent une douce chaleur.", 2)
                    time.sleep(1)
                    playsound("LevelUp2")
                    progprint(f"{NomPerso} se sent plus chanceux !", 2)
                    perso["Chance"] += 1
                else:
                    progprint("Cela n'a aucun effet...", 2)
                time.sleep(1)
                progprint(f"{NomPerso} a maintenant {OrPerso} pièces d'or.", 2)
            else:
                playsound("Chip")
                progprint(f"{NomPerso} n'a aucune pièce d'or.", 2)
                
        ### Quitter
        elif choix == 0:
            playsound("Fuite")
            progprint(f"{NomPerso} s'éloigne de la fontaine.", 2)
            continue
    
        choix = -1

### Stats ###
def afficher_stats(perso=personnage): 
    progprint(f"=== Statistiques de {perso["Nom"]} ===", 0.001)
    progprint(f"✱  LVL {perso.get('LVL', '?')}", 2)
    progprint(f"✱  EXP {afficher_barre(perso.get('EXP', '?'), perso.get('EXP_MAX', '?'), "")}", 2)
    progprint(f"✱  PV {afficher_barre(perso.get('PV', '?'), perso.get('PV_MAX', '?'), "")}", 2)
    progprint(f"✱  ATT {perso.get('ATT', '?')}", 2)
    progprint(f"✱  DEF {perso.get('DEF', '?')}", 2)
    progprint(f"✱  Chance {perso.get('Chance', '?')}", 4)
    progprint("=================================", 0.001)
        

### Exécution ###
# print("""
# ██╗  ██╗ █████╗ ██╗      ██████╗ ███████╗
# ██║ ██╔╝██╔══██╗██║     ██╔═══██╗██╔════╝
# █████╔╝ ███████║██║     ██║   ██║███████╗
# ██╔═██╗ ██╔══██║██║     ██║   ██║╚════██║
# ██║  ██╗██║  ██║███████╗╚██████╔╝███████║
# ╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝ ╚═════╝ ╚══════╝
# """)
# progprint("	Par Darius Georgescu",5)
# afficher_inventaire()
for pnj in PNJs.values():
    choisir_prenom(pnj)
continuer = input("Continuer à se balader ? (Oui/Non) : ").lower().strip().startswith("o")
while continuer:
    debut_combat()
    combat()
# progprint(f"{personnage['Nom']} est de retour au village.", 2)
village()