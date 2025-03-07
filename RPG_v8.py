# coding: utf-8


###############
### Imports ###
###############
import os
import platform
import sys
import json
from datetime import datetime
from time import sleep as wait
from random import randint, choice
from copy import deepcopy
if platform.system() == "Linux":
    os.environ['SDL_AUDIODRIVER'] = 'dummy'
    sys.stderr = open(os.devnull, 'w')
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
try:
    import pygame
    from termcolor import colored, cprint
except ModuleNotFoundError as module:
    print(f"⚠ Le module '{module.name}' n'est pas installé.")
    print(f"  Veuillez l'installer avec la commande : pip install {module.name}")
    exit()


######################
### Initialisation ###
######################
SONS_ACTIVES = True
PROGPRINT = False
COULEUR = "green"

### Couleurs ###
couleurs_CMD = {
    "black": "0",
    "blue": "1",
    "green": "2",
    "cyan": "3",
    "red": "4",
    "magenta": "5",
    "yellow": "6",
    "white": "7",
    "gray": "8",
    "light_blue": "9",
    "light_green": "A",
    "light_cyan": "B",
    "light_red": "C",
    "light_magenta": "D",
    "light_yellow": "E",
}
couleurs_ANSI = {
    "black": "\033[30m",
    "red": "\033[31m",
    "green": "\033[32m",
    "yellow": "\033[33m",
    "blue": "\033[34m",
    "magenta": "\033[35m",
    "cyan": "\033[36m",
    "white": "\033[37m",
    "reset": "\033[0m"
}

code_couleur_CMD = couleurs_CMD.get(COULEUR.lower(), "7")
code_couleur_ANSI = couleurs_ANSI.get(COULEUR.lower(), "\033[37m")
if platform.system() == "Windows":
    os.system(f"color {code_couleur_CMD} && cls")
elif platform.system() == "Linux":
    print(code_couleur_ANSI + "\033[2J\033[H")

### Sons ###
try:
    pygame.mixer.init()
except pygame.error as e:
    print(f"⚠ Erreur d'initialisation du mixer pygame : {e}")
    print("  Les sons seront désactivés.")
    SONS_ACTIVES = False
sons = {}
fichiers_sons = {
    "Titre": "title.ogg",
    "Voix": "voice.ogg",
    "Chip": "chip.ogg",
    "Button": "button.ogg",
    "Tidum": "tidum.ogg",
    "Youpi": "cheers.ogg",
    "Awh": "awh.ogg",
    "EXP": "exp.ogg",
    "LevelUp1": "levelup1.ogg",
    "LevelUp2": "levelup2.ogg",
    "Poing": "punch.ogg",
    "Attaque1": "swing1.ogg",
    "Attaque2": "swing2.ogg",
    "Attaque3": "swing3.ogg",
    "Epée": "swordhit.ogg",
    "Critique1": "crit1.ogg",
    "Critique2": "crit2.ogg",
    "Hit1": "hit1.ogg",
    "Hit2": "hit2.ogg",
    "Hit3": "hit3.ogg",
    "Ouch1": "ouch1.ogg",
    "Ouch2": "ouch2.ogg",
    "Ouch3": "ouch3.ogg",
    "Rate": "miss.ogg",
    "Reflect": "reflect.ogg",
    "Slimy1": "slimy1.ogg",
    "Slimy2": "slimy1.ogg",
    "Gobelin1": "goblin1.ogg",
    "Gobelin2": "goblin2.ogg",
    "Gobelin3": "goblin3.ogg",
    "Gobelin4": "goblin4.ogg",
    "Gobelin_Rire": "goblin_laugh.ogg",
    "Squelette1": "skeleton1.ogg",
    "Squelette2": "skeleton2.ogg",
    "Squelette3": "skeleton3.ogg",
    "Squelette4": "skeleton4.ogg",
    "Encounter1": "encounter1.ogg",
    "Encounter2": "encounter2.ogg",
    "Alerte": "alert.ogg",
    "Mort": "dust.ogg",
    "Victoire": "win.ogg",
    "Défaite": "defeat.ogg",
    "Fuite": "flee.ogg",
    "Pièce": "coin.ogg",
    "Objet1": "item.ogg",
    "Objet2": "item2.ogg",
    "Potion": "drink.ogg",
    "Boisson": "drinkgasp.ogg",
    "Manger": "eat.ogg",
    "Fléchette1": "dart1.ogg",
    "Fléchette2": "dart2.ogg",
    "Fléchette3": "dart3.ogg",
    "Magie": "magic.ogg",
    "Choeur": "choir.ogg",
    "Poison": "poison.ogg",
    "Splash": "splash.ogg",
    "Demon": "demon.ogg",
    "Mus_Combat": "mus_battle.ogg", # Version 8-bit de "Rude Buster" (Deltarune) par Toby Fox
    "Mus_Foret": "mus_forest.ogg", # Version 8-bit de "Scarlet Forest" (Deltarune) par Toby Fox
    "Mus_Village": "mus_village.ogg", # Version 8-bit de "Driftveil City" (Pokémon Noir et Blanc) par Hitomi Sato
}

if SONS_ACTIVES:
    for nom, directory in fichiers_sons.items():
        try:
            sons[nom] = pygame.mixer.Sound(f"sounds/{directory}")
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

def playmusic(nom, loop=-1, stop=False):
    if stop:
        pygame.mixer.music.stop()
        return
    if SONS_ACTIVES and f"Mus_{nom}" in fichiers_sons:
        directory = f"sounds/{fichiers_sons[f'Mus_{nom}']}"
        if pygame.mixer.music.get_busy() and pygame.mixer.music.get_pos() > 0:
            return
        pygame.mixer.music.load(directory)
        pygame.mixer.music.play(loops=loop)
        pygame.mixer.music.set_volume(0.5) 
    elif not fichiers_sons.get(f"Mus_{nom}"):
        print(f"⚠ Musique '{nom}' introuvable ou désactivée.")

### Affichage ###
def gras(text):
    return colored(text, attrs=["bold"])

def colorer(text, couleur=COULEUR):
    if platform.system() == "Linux":
        return f"{couleurs_ANSI.get(couleur.lower(), couleurs_ANSI['reset'])}{text}{couleurs_ANSI['reset']}"
    else:
        return colored(text, couleur)

def progprint(text, multi=1, delai=0.01, progprint=PROGPRINT, voix=False, gras=False, couleur=None):
    if couleur is not None:
        text = colored(text, couleur)
    if progprint:
        delai *= multi
        for carac in text:
            if gras:
                carac = colored(carac, attrs=["bold"])
            if voix:
                playsound("Voix")
            sys.stdout.write(carac)
            sys.stdout.flush()
            wait(delai)
        print()
    else:
        if gras:
            text = colored(text, attrs=["bold"])
        print(text)

def dialogue(NomPNJ, text, attente=1):
    NomPNJ = gras(NomPNJ.upper())
    text = f"{NomPNJ} : {text}"
    progprint(text, 2, voix=True)
    wait(attente)

def cls(keep=False):
    if platform.system() == "Windows":
        os.system("cls")
    elif platform.system() == "Linux":
        if keep:
            os.system("clear -x")
        else:
            os.system("clear")

### Paramétrage ###
def parametrage():
    global SONS_ACTIVES, PROGPRINT, COULEUR, code_couleur_CMD
    cprint("\n═════════ Paramètres du jeu ═════════", "light_blue")
    choix_sons = input(f"♬ Activer les sons et musiques ? [actuel: {'Oui' if SONS_ACTIVES else 'Non'}] : ").strip().lower().startswith("o")
    if choix_sons in ["oui", "non"]:
        SONS_ACTIVES = (choix_sons == "oui")
    choix_progprint = input(f"… Activer l'affichage progressif ? [actuel: {'Oui' if PROGPRINT else 'Non'}] : ").strip().lower().startswith("o")
    if choix_progprint in ["oui", "non"]:
        PROGPRINT = (choix_progprint == "oui")
    # print("Couleurs disponibles :")
    # for i, (couleur, code) in enumerate(couleurs_CMD.items(), 1):
    #     print(f"  {couleur} ({code})", end="\n" if i % 2 == 0 else "  ")
    # print()
    # choix_couleur = input(f"Choisir la couleur du texte [actuel: {COULEUR}]: ").strip().upper()
    # if choix_couleur in couleurs_CMD:
    #     COULEUR = choix_couleur
    #     code_couleur_CMD = couleurs_CMD[COULEUR]
    #     os.system(f"color {code_couleur_CMD} && cls")
    playsound("Tidum")
    cprint("═════ ✓ Paramètres mis à jour ! ═════", "light_blue")
    wait(1)
    

### Sauvegarde ###
PROFILS = {
    "Profil1": {},
    "Profil2": {},
    "Profil3": {}
}

def sauvegarder_json(profil, savedata):
    dossier = f"saves/{profil}"
    if not os.path.exists(dossier):
        os.makedirs(dossier)
    nom_fichier = f"{dossier}/save_{datetime.now().strftime('%d-%m-%Y_%H-%M-%S')}.json"
    with open(nom_fichier, 'w') as fichier:
        json.dump(savedata, fichier, indent=4)
    playsound("Tidum")
    print(f"🖫 Le jeu a été sauvegardé dans '{nom_fichier}'.")
    wait(0.5)

def charger_json(profil, nom_fichier):
    try:
        with open(f"saves/{profil}/{nom_fichier}", 'r') as fichier:
            savedata = json.load(fichier)
        playsound("Tidum")
        print(f"↓ Le jeu a été chargé depuis la sauvegarde '{nom_fichier}'.")
        return savedata
    except FileNotFoundError:
        playsound("Chip")
        print(f"⚠ Le fichier de sauvegarde '{nom_fichier}' n'a pas été trouvé.")
        return
    
def choisir_profil():
    playsound("Button")
    print("""
  ╔════════════════════╗
  ║  1)   Profil 1     ║
  ║  2)   Profil 2     ║
  ║  3)   Profil 3     ║
  ╚════════════════════╝\n""")
    choix = -1
    while choix not in ["1", "2", "3"]:
        choix = input("Numéro du profil : ").strip()
    return f"Profil{choix}"

def creer_partie(profil):
    print(f"🛠 Création d'une nouvelle partie sur {profil}...")
    save_data = {
        "PERSONNAGE" : {
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
            },
            "Quêtes": []
        },
        "INVENTAIRE": {
            "Équipement": {
                "Épée en bois": {
                    "Quantité": -1,
                    "Description": ("C'est juste un bâton.", "Octroie 1 ATT."),
                    "Effet": "+1 ATT",
                    "Type": "Arme",
                    "Valeur": 1,
                    "Symbole": "⚔",
                    "Rareté": "Commun",
                    "Prix": 5
                },
                "Tunique de noob": {
                    "Quantité": -1,
                    "Description": ("L'armure la plus pourrie.", "Octroie 1 DEF."),
                    "Effet": "+1 DEF",
                    "Type": "Armure",
                    "Valeur": 1,
                    "Symbole": "🛡",
                    "Rareté": "Commun",
                    "Prix": 5
                },
            },
            "Objets": {
                "Potion de soin": 2,
                "Potion d'énergie": 2,
                "Fléchette": 1,
            },
            "OR": 100
        }
    }
    wait(1)
    sauvegarder_json(profil, save_data)
    return save_data

def choisir_sauvegarde(profil):
    dossier = f"saves/{profil}"
    if not os.path.exists(dossier):
        playsound("Chip")
        print("⚠ Aucune sauvegarde trouvée pour ce profil.")
        return None
    fichiers = os.listdir(dossier)
    fichiers = sorted(fichiers, reverse=True)
    if not fichiers:
        playsound("Chip")
        print("⚠ Aucune sauvegarde disponible.")
        return None
    print("\n📂 Sauvegardes disponibles :")
    for i, fichier in enumerate(fichiers, 1):
        print(f"  {i}) {fichier}")
    print("  0) Annuler")
    choix = -1
    while choix not in [str(i) for i in range(len(fichiers) + 1)]:
        choix = input("Numéro de la sauvegarde : ").strip()
    if choix == "0":
        return None
    return fichiers[int(choix) - 1]

def charger_jeu(save_data):
    global PERSONNAGE, INVENTAIRE, QUETES
    PERSONNAGE = save_data["PERSONNAGE"]
    INVENTAIRE = save_data["INVENTAIRE"]
    print(f"✔ Partie de {PERSONNAGE['Nom']} chargée avec succès !")
    wait(0.5)
    voir_infos = input("Voulez-vous voir les infos de votre personnage ? (Oui/Non) : ").strip().lower().startswith("o")
    if voir_infos:
        afficher_stats(PERSONNAGE)
        afficher_inventaire(INVENTAIRE)
        wait(1)
        return

def menu_principal():
    playsound("Button")
    print("""
  ╔═══════════════════════════╗
  ║  1)   Nouvelle partie     ║
  ║  2)   Charger une partie  ║
  ║  0)   Quitter le jeu      ║
  ╚═══════════════════════════╝\n""")
    choix = -1
    while choix not in [0, 1, 2]:
        choix = input().strip()
        if choix == "1":
            profil = choisir_profil()
            save_defaut = creer_partie(profil)
            charger_jeu(save_defaut)
            return

        elif choix == "2":
            profil = choisir_profil()
            sauvegarde = choisir_sauvegarde(profil)
            if sauvegarde:
                save_data = charger_json(profil, sauvegarde)
                if save_data:
                    charger_jeu(save_data)
            return

        elif choix == "0":
            print("À bientôt !")
            exit()
  

#################
### Variables ###
#################
PERSONNAGE = {
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
    },
    "Quêtes": []
}

INVENTAIRE = {
    "Équipement": {
        "Épée en bois": 1,
        "Tunique de noob": 1,
    },
    "Objets": {
        "Potion de soin": 2,
        "Potion d'énergie": 2,
        "Fléchette": 1,
    },
    "OR": 100
}

EQUIPEMENT = {
    "Épée en bois": {
            "Description": ("C'est juste un bâton.", "Octroie 1 ATT."),
            "Effet": "+1 ATT",
            "Type": "Arme",
            "Valeur": 1,
            "Symbole": "⚔",
            "Rareté": "Commun",
            "Prix": 5
        },
        "Tunique de noob": {
            "Description": ("L'armure la plus pourrie.", "Octroie 1 DEF."),
            "Effet": "+1 DEF",
            "Type": "Armure",
            "Valeur": 1,
            "Symbole": "🛡",
            "Rareté": "Commun",
            "Prix": 5
        },
}

OBJETS = {
        "Potion de soin": {
            "Description": ("Une potion rouge et sucrée.", "Permet de soigner 20 PV instantanément"),
            "Effet": "+20 PV",
            "Type": "PV",
            "Valeur": 20,
            "Symbole": "❤",
            "Rareté": "Commun",
            "Prix": 50
        },
        "Potion d'énergie": {
            "Description": ("Une potion jaune et pétillante.", "Permet de restaurer 10 EN instantanément"),
            "Effet": "+10 EN",
            "Type": "EN",
            "Valeur": 10,
            "Symbole": "🗲",
            "Rareté": "Commun",
            "Prix": 50
        },
        "Poudre enchantée": {
            "Description": ("De la poussière magique.", "Permet de gagner 20 PV MAX temporairement"),
            "Effet": "+20 PV MAX",
            "Type": "PV MAX",
            "Valeur": 20,
            "Symbole": "❤",
            "Rareté": "Peu commun",
            "Prix": 100
        },
        "Fléchette": {
            "Description": ("Une pointe aiguisée.", "Inflige 20 DEG à l'ennemi"),
            "Effet": "20 DEG",
            "Type": "DEG",
            "Valeur": 20,
            "Symbole": "➸",
            "Rareté": "Commun",
            "Prix": 50
        },
} 

ENNEMIS = {
    "Slimy": {
        "Nom": "Slimy",
        "LVL": 1, "EXP": 20,
        "PV": 30, "PV_MAX": 30,
        "ATT": 3, "DEF": 1, "Chance": 8,
        "Description": "Un tas de gelée ou de morve ?",
    },
    "Gobelin": {
        "Nom": "Gobelin",
        "LVL": 2, "EXP": 40,
        "PV": 50, "PV_MAX": 50,
        "ATT": 4, "DEF": 2, "Chance": 10,
        "Description": "Un méchant lutin vert",
        "Or": randint(10, 50),
        "Objets": {
            "Potion de soin": 1
        }
    },
    "Squelette": {
        "Nom": "Squelette",
        "LVL": 3, "EXP": 60,
        "PV": 70, "PV_MAX": 70,
        "ATT": 5, "DEF": 3, "Chance": 8,
        "Description": "Un tas d'os articulés",
    },
    "Leprechaun": {
        "Nom": "Leprechaun",
        "LVL": 4, "EXP": 80,
        "PV": 80, "PV_MAX": 80,
        "ATT": 4, "DEF": 4, "Chance": 15,
        "Description": "Un farfadet irlandais",
        "Or": randint(50, 100),
        "Objets": {
            "Poudre enchantée": 1
        }
    }
}

PRENOMS = ["Alaric", "Balthar", "Cedric", "Darael", "Elowen", "Faelar", "Gwendal", "Havren", "Iriel", "Jorvik"]

PNJS = {
    "Aubergiste": {
        "Nom": "Balthar",
        "PV": 100, "PV_MAX": 100,
    },
    
    "Marchand": {
        "Nom": "Elowen",
        "PV": 100, "PV_MAX": 100,
        "Objets": {
            "Potion de soin": 50,
            "Potion d'énergie": 50,
            "Poudre enchantée": 50,
            "Fléchette": 50,
        },
    },

    "Maire": {
        "Nom": "Havren",
        "PV": 100, "PV_MAX": 100,
    }
}

QUETES = {
    "Principales": {
        "La Quête": {
            "Nom": "La Quête",
            "Description": "Retrouve le méchant et tue-le",
            "Objectif": "Tuer le méchant",
            "Récompenses": {
                "EXP": 200,
                "Objets": [
                    ["Épée légendaire", 1]
                ],
            },
            "Statut": "En cours",
            "Donneur": None
        },
    },
    "Secondaires": {
        "Slimy": {
            "Nom": "Extermination des Slimies",
            "Description": "Les Slimies envahissent la forêt voisine et menacent les récoltes des villageois.",
            "Objectif": "Tuer 3 Slimy",
            "Récompenses": {
                "EXP": 20,
                "Objets": [
                    ["Potion de soin", 1],
                ]
            },
            "Statut": -1,
            "Type": "Tuer",
            "Cible": "Slimy",
            "Donneur": "Maire"
        },
        "Gobelin": {
            "Nom": "Extermination des Gobelins",
            "Description": "Les Gobelins envahissent la forêt voisine et menacent les récoltes des villageois.",
            "Objectif": "Tuer 3 Gobelin",
            "Récompenses": {
                "EXP": 40,
                "Objets": [
                    ["Potion d'énergie", 1],
                ]
            },
            "Statut": -1,
            "Type": "Tuer",
            "Cible": "Gobelin",
            "Donneur": "Maire"
        },
    }
}


#################
### Fonctions ###
#################

### Fonctions de combat ###
def choisir_ennemi(perso=PERSONNAGE, ENNEMIS=ENNEMIS):
    ENNEMIS_adaptes = [
        ennemi for ennemi in ENNEMIS.values()
        if abs(ennemi["LVL"] - perso["LVL"]) <= 1
    ]
    if not ENNEMIS_adaptes:
        ENNEMIS_adaptes = list(ENNEMIS.values())
    return deepcopy(choice(ENNEMIS_adaptes))


def combat(perso=PERSONNAGE, enn=None, inv=INVENTAIRE):
    if enn is None:
        enn = choisir_ennemi()
    NomPerso = perso["Nom"].upper()
    NomEnn = enn["Nom"].upper()
    tour = 0
    playmusic("Foret", stop=True)

    playsound("Encounter1")
    progprint("⚔ Le combat commence ! ⚔", 3, gras=True)
    progprint(f"   {NomPerso} VS {NomEnn}", 3, gras=True)
    print()
    wait(1)
    playmusic("Combat")

    while perso["PV"] > 0 and enn["PV"] > 0:
        tour += 1
        progprint(f"═════════ Tour n°{tour} ═════════",0.001, progprint=False, gras=True, couleur="light_red")
        print(afficher_barre('PV', perso))
        print(afficher_barre('PV', enn))
        progprint("Que veux-tu faire ?", 0.05)
        
        actions = ["Attaque", f"Attaque critique ({2 * perso['Chance']}%)", "Objet", "Inspection", "Passer"]
        action = choisir_actions(actions, retour="Fuite", cheatcode=666)
        wait(0.5)
        
        ### Attaque ###
        if action == 1:
            if perso["ATT"] <= enn["DEF"]:
                progprint(f"🛡 {NomPerso} ne peut pas percer la défense de {NomEnn} !")
                playsound("Attaque")
                playsound("Reflect")
            else:
                DEGe = (perso["ATT"] - enn["DEF"]) * randint(1, 3) + 2
                if DEGe > 0:
                    enn["PV"] -= DEGe
                    progprint(f"  {NomPerso} inflige {DEGe} DEG à {NomEnn} !")
                    playsound("Attaque")
                    playsound("Epée")
                else:
                    progprint(f"༄ {NomPerso} rate son attaque !")
                    playsound("Attaque")
                    playsound("Rate")
        
        ### Critique ###
        elif action == 2:
            if perso["ATT"] < enn["DEF"]:
                progprint(f"🛡 {NomPerso} ne peut pas percer la défense de {NomEnn}... Même avec un coup critique !")
                playsound("Attaque")
                playsound("Reflect")
            else:
                if randint(1, 100) <= 2 * perso["Chance"]:
                    DEGe = (perso["ATT"] - enn["DEF"]) * 2 + randint(2, 3)
                    enn["PV"] -= DEGe
                    progprint(f"🗲 {NomPerso} réussit une attaque critique et inflige {DEGe} DEG à {NomEnn} !")
                    playsound("Attaque")
                    playsound("Epée")
                    playsound("Critique")
                else:
                    progprint(f"༄ {NomPerso} rate son attaque critique.")
                    playsound("Attaque")
                    playsound("Rate")
        
        ### Objet ###
        elif action == 3:
            progprint("═════════ Objets ═════════", 0.001, gras=True)
            objets_dispos = [(nom, inv["Objets"][nom]) for nom in inv["Objets"] if inv["Objets"][nom] > 0]
            if not objets_dispos:
                progprint("✘ Aucun objet consommable dans votre inventaire.", 3)
                progprint("═══════════════════════════", 0.001, gras=True)
                continue
            actions = []
            for nom, quantite in objets_dispos:
                actions.append(f"{nom} (x{quantite}) - {OBJETS[nom]['Description'][1]}")
            choix = choisir_actions(actions, retour="Revenir")
            if choix == 0:
                tour -= 1
                continue
            NomObjet = objets_dispos[choix - 1][0]
            _, objet = obtenir_details_objet(NomObjet)
            utiliser_objet(NomObjet, objet, ennemi=enn, combat=True)
        
        ### Inspection ###
        elif action == 4:
            playsound("Encounter2")
            NomEnn = enn.get('Nom', 'Inconnu').upper()
            LVL = enn.get('LVL', '?')
            ATT = enn.get('ATT', '?')
            DEF = enn.get('DEF', '?')
            description = enn.get('Description', 'Tu ne sais rien sur lui...')
            longueur = max(35, len(description) + 8)
            milieu = longueur // 2
            progprint(f"╔═══{((longueur - 35) // 2) * '═'} Informations sur l'ennemi {((longueur - 35) // 2) * '═'}═══╗", 0.001, gras=True)
            progprint(f"║ ✱  {NomEnn} {(milieu - len(NomEnn) - 7) * ' '} LVL {LVL} {(milieu - len(str(LVL)) - 6) * ' '} ║", 2, gras=True)
            progprint(f"║ ✱  ATT {ATT} {(milieu - len(str(ATT)) - 11) * ' '} DEF {DEF} {(milieu - len(str(DEF)) - 6) * ' '} ║", 2, gras=True)
            progprint(f"║ ✱  {description} {(longueur - len(description) - 8) * ' '} ║", 2, gras=True)
            progprint(f"╚{(longueur - 2) * '═'}╝\n", 0.001, gras=True)
            tour -= 1
            wait(1)
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
            wait(1)

        ### Cheatcode ###
        elif action == 666:
            enn["PV"] -= 66666
            playsound("Demon")
            progprint(f"\n⛤  {NomPerso} invoque une force maléfique et inflige des dégâts dévastateurs à {NomEnn} !")
            wait(1)

        ### Fuite ###
        elif action == 0:
            playsound("Fuite")
            progprint(f"༄ {NomPerso} s'enfuit !",2)
            result = "Défaite par fuite !"
            wait(1)
            break

        ### Vérif ###
        if enn["PV"] <= 0:
            playsound("Hit2")
            playsound("Mort")
            progprint(f"\n{enn['Nom']} est vaincu !", 5)
            result = "Victoire !"
            EXP = max(1 + (enn["LVL"] - perso["LVL"]) * 0.5, 0.5) * enn["EXP"]
            wait(2)
            break
  
        ### Fuite enn ###
        wait(1)
        ratio_PVe = enn["PV"] / enn["PV_MAX"]
        if ratio_PVe < 0.2:
            playsound("Alerte")
            progprint(f"‼ {NomEnn} semble terrifié et tente de fuir !")
            wait(1)
            seuil_fuite = 30 + enn["Chance"] - perso["Chance"]
            if randint(1, 100) <= seuil_fuite:
                playsound("Fuite")
                progprint(f"༄ {NomEnn} s'enfuit du combat !")
                result = "Victoire par forfait !"
                EXP = max(1 + (enn["LVL"] - perso["LVL"]) * 0.5, 0.5) * enn["EXP"] / 2
                wait(1.5)
                break
            else:
                playsound("Rate")
                progprint(f"Ö {NomEnn} panique mais ne parvient pas à fuir.")
                wait(1)
                print()
                continue

        ### Attaque enn ###
        if enn["ATT"] <= perso["DEF"]:
            playsound("Reflect")
            progprint(f"🛡 {NomEnn} ne peut pas percer la défense de {NomPerso} !")
        else:
            DEGp = max((enn["ATT"] - perso["DEF"]) * randint(1, 3) + 1, 0)
            critique = randint(1, 100) <= enn["Chance"]
            esquive = randint(1, 100) <= perso["Chance"]
            if critique and not esquive:
                DEGp *= 2
                perso["PV"] -= DEGp
                playsound(enn["Nom"])
                playsound("Critique", 2)
                playsound("Ouch")
                progprint(f"🗲{NomEnn} réussit une attaque critique et inflige {DEGp} DEG à {NomPerso} !")
            elif esquive:
                playsound("Rate")
                progprint(f"༄ {NomPerso} esquive l'attaque de {NomEnn} !")
            elif DEGp > 0:
                perso["PV"] -= DEGp
                playsound("Poing")
                playsound(enn["Nom"])
                playsound("Ouch")
                progprint(f"  {NomEnn} inflige {DEGp} DEG à {NomPerso} !")
            else:
                playsound("Rate")
                progprint(f"༄ {NomEnn} rate son attaque !")

        wait(1)
        print()

        ### Vérif 2 ###
        if perso["PV"] <= 0:
            playmusic("Combat", stop=True)
            playsound("Hit3")
            playsound("Mort")
            progprint(f"\n{perso['Nom']} est vaincu...", 5)
            result = "Défaite !"
            EXP = 0
            wait(2)
            break
    
    ### Fin du combat ###
    progprint("\n═════ Combat terminé ! ═════",3, gras=True, couleur="light_blue")
    if result.startswith("Victoire"):
        playmusic("Combat", stop=True)
        playsound("Victoire")
        if result == "Victoire par forfait !":
            EXP /= 2
        progprint(f"{result} {NomPerso} a gagné {int(EXP)} XP !", 5)
        perso["EXP"] += EXP
        wait(1)
        playsound("EXP")
        print(afficher_barre('EXP', perso, nom=False))
        verifier_niveau()
        wait(1)
        for quete in perso["Quêtes"]:
            quete = QUETES["Secondaires"][quete]
            if quete["Statut"] >= 0 and quete["Type"] == "Tuer" and quete["Cible"] == enn["Nom"]:
                quete["Statut"] += 1
                objectif = int(quete["Objectif"].split()[1])
                if quete["Statut"] >= objectif:
                    playsound("Victoire")
                    progprint(f"Quête terminée : {quete['Nom']} - {quete['Objectif']} ({quete['Statut']}/{objectif})", 2)
                else:
                    progprint(f"Quête en cours : {quete['Nom']} - {quete['Objectif']} ({quete['Statut']}/{objectif})", 2)
    
    if result.startswith("Défaite"):
        playmusic("Combat", stop=True)
        playsound("Défaite")
        progprint(f"{result} {NomPerso} n'a pas gagné d'XP.", 5)
        wait(1)
    if any(perso["BONUS"].values()):
        reinitialiser_bonus(perso)
        for stat in ["PV_MAX", "ATT", "DEF", "Chance"]:
            perso[stat] = calculer_bonus(perso, stat)
        perso["PV"] = min(perso["PV"], perso["PV_MAX"])
    wait(1)
    print()


### Fonctions de déplacement ###
def balade(perso=PERSONNAGE, cout_EN=3, continuer=True):
    NomPerso = perso["Nom"]
    cout_EN_initial = cout_EN
    while continuer:
        wait(1)
        print()
        
        if perso["EN"] < cout_EN:
            playsound("Chip")
            progprint(f"{NomPerso} est épuisé et n'a plus assez d'EN pour se balader.", 2)
            wait(1)
            break
        else:
            playmusic("Foret")
            cout_EN += randint(0, 2)
            perso["EN"] -= cout_EN
            perso["EN"] = max(perso["EN"], 0)
            playsound("Fuite")
            progprint(f"{NomPerso} se balade... -{min(cout_EN, perso['EN'])} EN", 2)
            print(afficher_barre('EN', perso)+"\n")
            action = randint(1, perso["Chance"])
            wait(1.5)
            
            if action <= 5:
                playsound("Alerte")
                progprint(f"‼ {NomPerso} tombe sur un ennemi !\n", 2, gras=True)
                wait(1)
                combat()
            
            elif action >= 10:
                messages = {
                    "Commun": "Tiens !",
                    "Peu commun": "Oh, cool !",
                    "Rare": "Ca brille !",
                    "Épique": "Waouh !",
                    "Légendaire": "OH MOOON DIEEUU !!1!"
                }
                paliers = {
                    15: ["Commun", "Peu commun"],
                    20: ["Commun", "Peu commun", "Rare"],
                    25: ["Commun", "Peu commun", "Rare", "Épique"],
                    30: ["Commun", "Peu commun", "Rare", "Épique", "Légendaire"]
                }
                couleurs = {
                    "Commun": "WHITE",
                    "Peu commun": "GREEN",
                    "Rare": "BLUE",
                    "Épique": "MAGENTA",
                    "Légendaire": "YELLOW"
                }
                rarete = ["Commun"]
                for palier, raretes in paliers.items():
                    if perso["Chance"] > palier:
                        rarete = raretes
                objets_possibles = []
                for nom, details in OBJETS.items():
                    if details["Rareté"] in rarete:
                        objets_possibles.append(nom)
                if objets_possibles:
                    objet_trouve = choice(objets_possibles)
                    playsound("Objet1")
                    playsound("Objet2")
                    rarete_objet = OBJETS[objet_trouve]['Rareté']
                    couleur = couleurs[rarete_objet]
                    progprint(f"{messages[rarete_objet]} {PERSONNAGE['Nom']} a trouvé {colorer(objet_trouve, couleur)} !", 2)
                    if objet_trouve in INVENTAIRE["Objets"]:
                        INVENTAIRE["Objets"][objet_trouve] += 1
                    else:
                        INVENTAIRE["Objets"][objet_trouve] = 1
                else:
                    progprint(f"{PERSONNAGE['Nom']} ne trouve rien d'intéressant.", 2)
            
            else:
                dialogues = [
                    f"(・―・) {NomPerso} marche tranquillement.",
                    f"(╭ರ_•́)  {NomPerso} observe les alentours.",
                    f"(⨀ ︿⨀ )  {NomPerso} entend un bruit bizarre !",
                    f"(◡̀_◡́)ᕤ  {NomPerso} se dit qu'il est le meilleur.",
                    f"(￢_￢) {NomPerso} reste sur ses gardes."
                ]
                progprint(choice(dialogues), 2)
            wait(1)
        
        cout_EN = cout_EN_initial
        continuer = input("Continuer à se balader ? (Oui/Non) : ").lower().strip().startswith("o")
    playmusic("Foret", stop=True)

### Fonctions autres ###
def obtenir_details_objet(NomObjet):
    objet = OBJETS.get(NomObjet, {
        "Description": ("Objet inconnu", "Effet inconnu."),
        "Type": "Inconnu",
        "Effet": "Inconnu",
        "Valeur": 0,
        "Symbole": " ",
        "Prix": 0
    })
    return NomObjet, objet

def utiliser_objet(NomObjet, objet, ennemi=None, combat=False, perso=PERSONNAGE, inv=INVENTAIRE):
    if NomObjet not in inv["Objets"] or inv["Objets"][NomObjet] <= 0:
        progprint(f"✘ {perso['Nom']} n'a pas de {NomObjet}.")
        return False
    if not objet:
        progprint(f"⁇ {NomObjet} est inconnu.")
        return False
    NomPerso = gras(perso["Nom"].upper())
    espace = ""
    if combat:
        espace = "  "

    if objet["Type"] == "PV":
        soin = objet["Valeur"]
        if perso["PV"] < perso["PV_MAX"]:
            progprint(f"  {NomPerso} utilise {NomObjet}.", 2)
            wait(0.5)
            perso["PV"] += soin
            perso["PV"] = min(perso["PV"], perso["PV_MAX"])
            playsound(NomObjet.split()[0])
            progprint(f"{objet['Symbole']} {NomPerso} récupère {soin} PV !", 2)
            print(espace, afficher_barre('PV', perso))
        else:
            progprint(f"🖒 {NomPerso} est déjà en pleine forme.")
            return False

    elif objet["Type"] == "EN":
        energie = objet["Valeur"]
        if perso["EN"] < perso["EN_MAX"]:
            progprint(f"  {NomPerso} utilise {NomObjet}.", 2)
            wait(0.5)
            perso["EN"] += energie
            perso["EN"] = min(perso["EN"], perso["EN_MAX"])
            playsound(NomObjet.split()[0])
            progprint(f"{objet['Symbole']} {NomPerso} gagne {energie} EN !", 2)
            print(espace, afficher_barre('EN', perso))
        else:
            progprint(f"🖒 {NomPerso} a déjà toute son énergie !\n", 2)
            return False

    elif objet["Type"] == "DEG" and combat:
        DEG = objet["Valeur"]
        NomEnn = gras(ennemi['Nom'].upper())
        if ennemi:
            progprint(f"\n  {NomPerso} utilise {NomObjet}.", 2)
            wait(0.5)
            ennemi["PV"] -= DEG
            playsound("Attaque")
            progprint(f"{objet['Symbole']} {NomEnn} subit {DEG} dégâts !", 2)
        else:
            progprint(f"✘ Aucun ennemi pour utiliser {NomObjet}.")
            return False

    elif objet["Type"] == "DEG" and not combat:
        progprint(f"✘ {NomObjet} ne peut pas être utilisé hors combat.")
        return False

    inv["Objets"][NomObjet] -= 1
    if inv["Objets"][NomObjet] == 0:
        playsound("Chip")
        progprint(f"✘ {NomPerso} n'a plus de {NomObjet}.")

    return True

def acheter_objet(NomObjet, vendeur=PNJS["Marchand"], NomPerso=PERSONNAGE["Nom"], inv=INVENTAIRE):
    if vendeur["Objets"][NomObjet] <= 0:
        playsound("Chip")
        progprint(f"✘ {vendeur['Nom']} n'a plus de {NomObjet} en stock.")
        return
    if inv["OR"] >= OBJETS[NomObjet]["Prix"]:
        inv["OR"] -= OBJETS[NomObjet]["Prix"]
        vendeur["Objets"][NomObjet] -= 1
        if NomObjet in inv["Objets"]:
            inv["Objets"][NomObjet] += 1
        else:
            inv["Objets"][NomObjet] = 1
        playsound("Pièce")
        progprint(f"✓ {NomPerso} a acheté {NomObjet} pour {OBJETS[NomObjet]['Prix']} OR.")
        return True
    else:
        playsound("Chip")
        progprint(f"✘ {NomPerso} n'a pas assez d'or pour acheter {NomObjet}.")
        return False

def afficher_stats(perso=PERSONNAGE):
    NomPerso = perso['Nom']
    LVL = perso['LVL']
    EXP = afficher_barre('EXP', nom=False)
    PV = afficher_barre('PV', nom=False)
    EN = afficher_barre('EN', nom=False)
    ATT = perso['ATT']
    DEF = perso['DEF']
    Chance = perso['Chance']
    longueur = max(44, (len(NomPerso) + 41))
    progprint(f"╔═════════{((longueur - 44) // 2) * '═'} Statistiques de {NomPerso} {((longueur - 44) // 2) * '═'}════════╗", 0.001, gras=True)
    progprint(f"║ ✱  LVL {LVL} {(longueur - len(str(LVL)) - 12) * ' '} ║", 2, gras=True)
    progprint(f"║ ✱  EXP {EXP} {(longueur - len(str(EXP)) + 5) * ' '} {gras('║')}", 2, gras=True)
    progprint(f"║ ✱  PV {PV} {(longueur - len(str(PV)) + 6) * ' '} {gras('║')}", 2, gras=True)
    progprint(f"║ ✱  EN {EN} {(longueur - len(str(EN)) + 6) * ' '} {gras('║')}", 2, gras=True)
    progprint(f"║ ✱  ATT {ATT} {(longueur - len(str(ATT)) - 12) * ' '} ║", 2, gras=True)
    progprint(f"║ ✱  DEF {DEF} {(longueur - len(str(DEF)) - 12) * ' '} ║", 2, gras=True)
    progprint(f"║ ✱  Chance {Chance} {(longueur - len(str(Chance)) - 15) * ' '} ║", 2, gras=True)
    progprint(f"╚{(longueur - 2) * '═'}╝", 0.001, gras=True)

def afficher_inventaire(inv=INVENTAIRE):
    progprint("\n═════════ Inventaire ═════════", gras=True)
    progprint(gras("Équipement :"), 2)
    for item, details in inv["Équipement"].items():
        if details["Quantité"] == -1:
            progprint(f"  - {item} : {details['Effet']}", 2)
        else:
            progprint(f"  - {item} : {details['Effet']} (x{details['Quantité']})", 2)
    progprint(gras("Objets :"), 2)
    for objet, quantite in inv["Objets"].items():
        if quantite != 0:
            details = OBJETS[objet]
            effet = details["Effet"]
            progprint(f"  - {objet} : {effet} (x{quantite})", 2)
    progprint(f"OR : {inv['OR']}", 2, gras=True)
    progprint("══════════════════════════════\n", gras=True)

def afficher_barre(type="PV", perso=PERSONNAGE, long_base=20, nom=True):
    stat = perso[type]
    stat_MAX = perso[f"{type}_MAX"]
    long = max(long_base, stat_MAX // 5)
    prop = max(0, min(1, stat / stat_MAX))
    rempli = int(prop * long)
    couleurs = {
        "PV": 'green',
        "EN": 'cyan',
        "EXP": 'yellow',
        None: 'white',
    }
    NomPerso = perso["Nom"].upper()
    carac = ["\u2588", "\u2591"] # ["░", "█"]
    barre = f"{colorer(f'[{carac[0] * rempli}{carac[1] * (long - rempli)}]', couleurs[type])} {int(stat)}/{stat_MAX}"
    if nom:
        return gras(f"{NomPerso} : {barre} {type}")
    else:
        return gras(f"{barre} {type}")

def choisir_actions(actions, titre=None, retour=None, cheatcode=False):
    choix = -1
    actions_dict = {i + 1: action for i, action in enumerate(actions)}
    if retour:
        actions_dict[0] = retour
    if titre:
        long_totale = 20
        marge = (long_totale - len(titre)) // 2
        séparateurs = "═" * marge
        progprint(f"{séparateurs} {titre} {séparateurs}", 0.001, gras=True)
    while choix not in actions_dict:
        for i, action in actions_dict.items():
            if i == 0:
                progprint(f"◄ {i}) {action}", 0.05)
            else:
                progprint(f"  {i}) {action}", 0.05)
        choix = input("Ton choix : ")
        if choix.isdigit():
            choix = int(choix)
            if cheatcode and choix == cheatcode:
                return choix
        else:
            playsound("Chip")
            print("## Entre un chiffre valide ##")
            choix = -1
        print()
        wait(0.5)
    return choix

def verifier_niveau(perso=PERSONNAGE):
    while perso["EXP"] >= perso["EXP_MAX"]:
        perso["EXP"] -= perso["EXP_MAX"]
        perso["LVL"] += 1
        perso["EXP_MAX"] = int(perso["EXP_MAX"] * 1.5)
        stats_avant = {
            "PV": perso["PV"],
            "EN": perso["EN"],
            "ATT": perso["ATT"],
            "DEF": perso["DEF"],
            "Chance": perso["Chance"]
        }
        perso["PV_MAX"] += 10
        perso["EN_MAX"] += 5
        perso["PV"] = perso["PV_MAX"]
        perso["EN"] = perso["EN_MAX"]
        perso["ATT"] += 2
        perso["DEF"] += 1
        perso["Chance"] += 1
        playsound("LevelUp1")
        progprint(f"★ {perso['Nom']} passe au niveau {perso['LVL']} !", 2)
        wait(0.25)
        for stat, ancienne in stats_avant.items():
            nouvelle = perso[stat]
            progprint(f"  {stat}: {ancienne} --> {nouvelle}", 2)
            wait(0.25)
        wait(0.5)

def calculer_bonus(perso, stat):
    return perso[stat] + perso["BONUS"].get(stat, 0)

def reinitialiser_bonus(perso, stats=None):
    if stats is None:
        stats = perso["BONUS"].keys()
    for stat in stats:
        if stat in perso["BONUS"]:
            perso["BONUS"][stat] = 0
    progprint(f"{perso['Nom']} ressent une rechute d'énergie.", 2)
    
def donner_quete(quete=None, NomDonneur=None, perso=PERSONNAGE):
    NomPerso = perso["Nom"]
    if quete is None:
        print("⚠ Aucune quête n'a été fournie.")
        return
    progprint("\n════════════  Quête  ════════════", 0.001, gras=True)
    progprint(f"{NomDonneur} propose une quête à {NomPerso} : {gras(quete['Nom'])}")
    progprint(quete['Description'])
    progprint(f"Objectif : {quete['Objectif']}")
    progprint(f"Récompenses :")
    progprint(f"- {quete['Récompenses']['EXP']} EXP")
    for objet, quantite in quete['Récompenses']['Objets']:
        progprint(f"- {objet} (x{quantite})")
    acceptation = input("Accepter la quête ? (Oui/Non) : ").strip().lower().startswith("o")
    progprint("═════════════════════════════════\n", 0.001, gras=True)
    if acceptation:
        perso["Quêtes"].append(quete["Cible"])
        quete["Statut"] = 0
        playsound("Youpi")
        progprint(f"✓ {NomPerso} a accepté la quête : {quete['Nom']}")
        result = True
    else:
        playsound("Awh")
        progprint(f"✘ {NomPerso} a refusé la quête : {quete['Nom']}")
        result = False
    wait(1)
    print()
    return result

def terminer_quete(quete=None, perso=PERSONNAGE, inv=INVENTAIRE):
    if quete is None:
        print("⚠ Aucune quête n'a été fournie.")
        return
    if quete not in perso["Quêtes"]:
        print("⚠ La quête n'a pas été trouvée dans la liste des quêtes du personnage.")
        return
    quete = QUETES["Secondaires"][quete]
    quete["Statut"] = -2
    perso["EXP"] = perso.get("EXP", 0) + quete["Récompenses"]["EXP"]
    for objet, quantite in quete["Récompenses"]["Objets"]:
        if objet in inv["Objets"]:
            inv["Objets"][objet] += quantite
        else:
            inv["Objets"][objet] = quantite
    playsound("Victoire")
    progprint("\n════════════  Quête  ════════════", 0.001, gras=True)
    progprint(f"Quête terminée : {quete['Nom']} !", 3)
    # perso["Quêtes"].remove(quete)
    wait(1)
    playsound("EXP")
    progprint(f"+ {quete['Récompenses']['EXP']} EXP")
    afficher_barre('EXP', perso, nom=False)
    for objet, quantite in quete['Récompenses']['Objets']:
        playsound("Objet1")
        playsound("Objet2")
        progprint(f"+ {objet} (x{quantite})")
    progprint("═════════════════════════════════\n", 0.001, gras=True)
    wait(1)
    verifier_niveau()

def dormir(perso=PERSONNAGE, type_chambre="dehors", dérangé=False, inv=INVENTAIRE):
    NomPerso = perso["Nom"]
    if type_chambre == "dehors":
        recup = 5
        progprint(f"{NomPerso} s'endort craintivement...", 5)
        wait(1)
    elif type_chambre == "normale" or type_chambre == "campement":
        recup = 10
        progprint(f"{NomPerso} s'endort tranquillement...", 5)
        wait(1)
    elif type_chambre == "royale":
        recup = 20
        progprint(f"{NomPerso} s'endort paisiblement...", 5)
        wait(1)
    if dérangé:
        recup //= 2
    perso["EN"] = min(perso["EN"] + recup, perso["EN_MAX"])
    if not dérangé:
        progprint("ᶻ 𝘇𐰁", 50)
        playsound("LevelUp2")
        progprint(f"{NomPerso} s'est bien reposé et récupère {recup} EN.")
        wait(1)
    else:
        progprint("ᶻ 𝗓!", 50)
        playsound("Alerte")
        progprint(f"{NomPerso} se réveille brusquement ! (+{recup} EN)")
    print(afficher_barre('EN', perso))
    
def choisir_prenom(pnj, prenoms=PRENOMS):
    prenom = choice(prenoms)
    prenoms.remove(prenom)
    pnj["Nom"] = prenom


### Village ###
def village(perso=PERSONNAGE, inv=INVENTAIRE):
    NomPerso = perso["Nom"]
    playsound("Fuite")
    progprint(f"\n{NomPerso} arrive au village.", 2)
    wait(1)
    print()
    playmusic("Village")
    actions = ["Mairie", "Boutique", "Auberge", "Fontaine", f"Statistiques de {NomPerso}"]
    choix = choisir_actions(actions, "Village", "Quitter le village")
    
    while choix != 0:
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
            wait(1)
            afficher_inventaire(inv)
            wait(1)
            
        choix = choisir_actions(actions, "Village", "Quitter le village")
    
    if perso["EN"] <= 0:
        playsound("Awh")
        progprint(f"{NomPerso} devrait rester un peu au village pour se reposer...")
    else:
        playmusic("Village", stop=True)
        playsound("Fuite")
        progprint(f"{NomPerso} quitte le village.", 2)
    wait(1)

### Mairie ###
def mairie(perso=PERSONNAGE, inv=INVENTAIRE):
    NomPerso = perso["Nom"]
    playsound("Fuite")
    progprint(f"{NomPerso} entre dans la mairie.", 2)
    wait(1)
    NomMaire = PNJS["Maire"]["Nom"].capitalize()
    quete = QUETES["Secondaires"]["Slimy"]
    if quete["Cible"] in perso["Quêtes"]:
        if quete["Statut"] >= 0 and quete["Statut"] < int(quete["Objectif"].split()[1]):
            dialogue(NomMaire, f"Qu'est-ce que vous attendez pour finir la quête ? Allez-y !")
        elif quete["Statut"] == 3:
            dialogue(NomMaire, f"Vous les avez tous tués ?! Merveilleux !")
            dialogue(NomMaire, f"Laissez-moi vous offrir ceci !")
            terminer_quete(quete["Cible"])
            dialogue(NomMaire, f"Merci pour votre aide ! Au revoir !")
    else:
        dialogue(NomMaire, f"Bienvenue à la mairie, {NomPerso} ! Je suis {NomMaire} le Maire du village.")
        dialogue(NomMaire, f"Nous avons besoin de votre aide, {NomPerso} ! Des monstres ont envahi la forêt d'à côté.")
        dialogue(NomMaire, f"Voulez-vous bien nous aider ?")
        resultat = donner_quete(quete, NomMaire.capitalize())
        if resultat:
            dialogue(NomMaire, f"Merci pour votre aide ! Au revoir !")
        else:
            dialogue(NomMaire, f"Dommage ! On a vraiment besoin de vous ! Au revoir !")
    playsound("Fuite")
    progprint(f"{NomPerso} sort de la mairie.\n", 2)

### Boutique ###
def boutique(perso=PERSONNAGE, inv=INVENTAIRE):
    NomPerso = perso["Nom"]
    playsound("Fuite")
    progprint(f"{NomPerso} entre dans la boutique.", 2)
    wait(1)
    NomMarch = PNJS["Marchand"]["Nom"].capitalize()
    dialogue(NomMarch, f"Bienvenue à la boutique, {NomPerso} ! Je suis {NomMarch} le Marchand.")
    dialogue(NomMarch, f"Voici les objets que j'ai en stock.")
    print()
    objets_dispos = []
    for objet in PNJS["Marchand"]["Objets"]:
        prix = OBJETS[objet]["Prix"]
        objets_dispos.append((objet, prix))
    actions = []
    for objet, prix in objets_dispos:
        actions.append(f"{objet} - {prix} OR")
    choix = choisir_actions(actions, "Boutique", "Revenir au village")
    while choix != 0:
        NomObjet = objets_dispos[choix - 1][0]
        if acheter_objet(NomObjet):
            progprint(f"OR restant : {inv['OR']} OR", 2)
        choix = choisir_actions(actions, "Boutique", "Revenir au village")
    dialogue(NomMarch, f"Merci et au revoir !", 0)
    playsound("Fuite")
    progprint(f"{NomPerso} sort de la boutique.\n", 2)
        
### Auberge ###
def auberge(perso=PERSONNAGE, inv=INVENTAIRE):
    NomPerso = perso["Nom"]
    playsound("Fuite")
    progprint(f"{NomPerso} entre dans l'auberge.", 2)
    wait(1)
    NomAuberg = PNJS["Aubergiste"]["Nom"].capitalize()
    dialogue(NomAuberg, f"Bienvenue à l'auberge, {NomPerso} ! Je suis {NomAuberg} l'Aubergiste.")
    dialogue(NomAuberg, "Nous avons deux types de chambres disponibles.")
    dialogue(NomAuberg, "Une chambre normale pour 10 pièces d'OR qui vous offre un sommeil réparateur.")
    dialogue(NomAuberg, "Ou une chambre royale pour 20 pièces d'OR qui vous offre un sommeil divin.")
    actions = ["Chambre normale - (10 OR)", "Chambre royale - (20 OR)"]
    choix = choisir_actions(actions, "Auberge", "Revenir au village")
    
    ### Chambre normale ###
    if choix == 1:
        if inv["OR"] >= 10:
            inv["OR"] -= 10
            progprint(f"  {NomPerso} se repose dans une chambre normale.", 2)
            progprint(f"❤ {NomPerso} récupère tous ses PVs.", 2)
            perso["PV"] = perso["PV_MAX"]
            playsound("Potion")
            print(afficher_barre('PV'))
        else:
            playsound("Chip")
            dialogue(NomAuberg, f"Désolé {NomPerso} ! Je ne fais pas de crédit. Reviens quand tu es un peu, hmmmmmmm, plus riche !")
    
    ### Chambre royale ###
    elif choix == 2:
        if inv["OR"] >= 20:
            inv["OR"] -= 20
            progprint(f"  {NomPerso} se repose dans une chambre royale.",2)
            progprint(f"❤ {NomPerso} récupère tous ses PVs et gagne 10 PV MAX temporaires !", 2)
            perso["BONUS"]["PV_MAX"] = 10
            perso["PV"] = calculer_bonus(perso, "PV_MAX")
            playsound("Potion")
            print(afficher_barre('PV'))
        else:
            playsound("Chip")
            dialogue(NomAuberg, f"Désolé {NomPerso} ! Je ne fais pas de crédit. Reviens quand tu es un peu, hmmmmmmm, plus riche !")
    
    ### Quitter ###
    elif choix == 0:
        dialogue(NomAuberg, "Au revoir et à bientôt !", 0)
        playsound("Fuite")
        progprint(f"{NomPerso} sort de l'auberge.", 2)
    print()

### Fontaine ###
def fontaine(perso=PERSONNAGE, inv=INVENTAIRE):
    NomPerso = perso["Nom"]
    OrPerso = inv["OR"]
    playsound("Fuite")
    progprint(f"{NomPerso} arrive devant la fontaine.", 2)
    wait(1)
    print()
    
    actions = ["Se laver le visage", "Boire l'eau", "Jeter une pièce"]
    action = choisir_actions(actions, "Fontaine", "Revenir au village")
    while action != 0:
        ### Se laver le visage
        if action == 1:
            playsound("Splash")
            progprint(f"{NomPerso} se lave le visage et se sent rafraîchi.", 2)

        ### Boire l'eau
        elif action == 2:
            playsound("Splash")
            playsound("Potion")
            progprint(f"{NomPerso} boit l'eau de la fontaine.", 2)
            wait(1)
            if randint(1, 3) == 1:
                soin = randint(5, 10)
                playsound("Boisson")
                progprint(f"Elle est bonne ! {NomPerso} récupère {soin} PVs.", 2)
                perso["PV"] = min(perso["PV"] + soin, perso["PV_MAX"])
            else:
                DEG = randint(5, 10)
                playsound("Poison")
                wait(0.1)
                playsound("Ouch")
                progprint(f"Elle est mauvaise ! {NomPerso} perd {DEG} PVs.", 2)
                perso["PV"] -= DEG
            print(afficher_barre('PV'))

        ### Jeter une pièce
        elif action == 3:
            if OrPerso >= 1:
                playsound("Pièce")
                progprint(f"{NomPerso} jette une pièce dans la fontaine.", 2)
                OrPerso -= 1
                inv["OR"] = OrPerso
                wait(1)
                if randint(1, 10) * perso["Chance"] >= 90:
                    playsound("Choeur")
                    progprint(f"La fontaine brille légèrement et {NomPerso} sent une douce chaleur.", 2)
                    wait(1)
                    playsound("LevelUp2")
                    progprint(f"{NomPerso} se sent plus chanceux !", 2)
                    perso["Chance"] += 1
                else:
                    progprint("Cela n'a aucun effet...", 2)
                wait(1)
                progprint(f"{NomPerso} a maintenant {OrPerso} OR.", 2)
            else:
                playsound("Chip")
                progprint(f"{NomPerso} n'a aucun OR.", 2)

        action = choisir_actions(actions, "Fontaine", "Revenir au village")
    
    playsound("Fuite")
    progprint(f"{NomPerso} s'éloigne de la fontaine.", 2)
        

### Exécution ###
def execution():
    playsound("Titre")
    print("""
    ██╗  ██╗ █████╗ ██╗      ██████╗ ███████╗
    ██║ ██╔╝██╔══██╗██║     ██╔═══██╗██╔════╝
    █████╔╝ ███████║██║     ██║   ██║███████╗
    ██╔═██╗ ██╔══██║██║     ██║   ██║╚════██║
    ██║  ██╗██║  ██║███████╗╚██████╔╝███████║
    ╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝ ╚═════╝ ╚══════╝
    """)
    wait(1)
    progprint("	Par Darius Georgescu", 5, gras=True)
    wait(1)
    menu_principal()
    parametrage()
    for pnj in PNJS.values():
        choisir_prenom(pnj)
    for i in range(100):
        village()
        balade()


execution()