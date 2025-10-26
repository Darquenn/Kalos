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
    "Mus_Boss": "mus_boss.ogg", # Version 8-bit de "Battle Against a True Hero" (Undertale) par Toby Fox
    "Mus_Boutique": "mus_shop.ogg", # Version 8-bit de "Tem Shop" (Undertale) par Toby Fox
    "Mus_Secret": "mus_secret.ogg", # Version 8-bit de "sans." (Undertale) par Toby Fox
}

if SONS_ACTIVES:
    for nom, directory in fichiers_sons.items():
        try:
            sons[nom] = pygame.mixer.Sound(f"sounds/{directory}")
        except FileNotFoundError:
            print(f"⚠ Fichier son introuvable : {directory}. Le son '{nom}' sera désactivé.")
            sons[nom] = None

def playsound(nom, nb=0):
    """Joue un son à partir de son nom. Si nb > 0, choisit un son aléatoire parmi les variantes numérotées."""
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

def playmusic(nom, loop=-1, stop=False, volume=0.5):
    """Joue une musique de fond à partir de son nom. Si stop est True, arrête la musique en cours avant de jouer la nouvelle."""
    if stop:
        pygame.mixer.music.stop()
    if SONS_ACTIVES and f"Mus_{nom}" in fichiers_sons:
        directory = f"sounds/{fichiers_sons[f'Mus_{nom}']}"
        if pygame.mixer.music.get_busy() and pygame.mixer.music.get_pos() > 0:
            return
        pygame.mixer.music.load(directory)
        pygame.mixer.music.play(loops=loop)
        pygame.mixer.music.set_volume(volume)
    elif not fichiers_sons.get(f"Mus_{nom}"):
        print(f"⚠ Musique '{nom}' introuvable ou désactivée.")

def stopmusic():
    """Arrête la musique de fond en cours."""
    pygame.mixer.music.stop()

### Affichage ###
def gras(text):
    """Retourne le texte en gras."""
    return colored(text, attrs=["bold"])

def colorer(text, couleur=COULEUR):
    """Retourne le texte coloré selon la couleur spécifiée."""
    if platform.system() == "Linux":
        return f"{couleurs_ANSI.get(couleur.lower(), couleurs_ANSI['reset'])}{text}{couleurs_ANSI['reset']}"
    else:
        return colored(text, couleur)

def progprint(text, multi=1, delai=0.01, voix=False, gras=False, couleur=None, progprint=PROGPRINT):
    """Affiche le texte de manière progressive, caractère par caractère, avec options de style et son."""
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

def dialogue(NomPNJ, text, attente=1, son=None):
    """Affiche un dialogue d'un PNJ avec son nom en gras et en majuscules, joue un son si spécifié, et attend un certain temps si spécifié."""
    NomPNJ = gras(NomPNJ.upper())
    text = f"{NomPNJ} : {text}"
    progprint(text, 2, voix=True)
    if son:
        playsound(son)
    wait(attente)

def cls(keep=False):
    """Efface l'écran de la console."""
    if platform.system() == "Windows":
        os.system("cls")
    elif platform.system() == "Linux":
        if keep:
            os.system("clear -x")
        else:
            os.system("clear")

### Paramétrage ###
def parametrage():
    """Configure les paramètres du jeu."""
    global SONS_ACTIVES, PROGPRINT, COULEUR, code_couleur_CMD
    cprint("\n═════════ Paramètres du jeu ═════════", "light_blue")
    rep_sons = input(f"♬ Activer les sons et musiques ? [actuel: {'Oui' if SONS_ACTIVES else 'Non'}] : ").strip().lower()
    if rep_sons != "":
        SONS_ACTIVES = rep_sons.startswith("o")
    # rep_prog = input(f"… Activer l'affichage progressif ? [actuel: {'Oui' if PROGPRINT else 'Non'}] : ").strip().lower()
    # if rep_prog != "":
    #     PROGPRINT = rep_prog.startswith("o")
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
    return SONS_ACTIVES, PROGPRINT
    
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
    "ATT": 3, "DEF": 2, "LUCK": 10,
    "BONUS": {
        "PV_MAX": 0,
        "ATT": 0,
        "DEF": 0,
        "LUCK": 0
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
    "Épée en fer": {
            "Description": ("Une épée en fer rouillée.", "Octroie 5 ATT."),
            "Effet": "+5 ATT",
            "Type": "Arme",
            "Valeur": 5,
            "Symbole": "⚔",
            "Rareté": "Peu commun",
            "Prix": 50
        },
    "Armure en fer": {
            "Description": ("Une armure en fer rouillée.", "Octroie 5 DEF."),
            "Effet": "+5 DEF",
            "Type": "Armure",
            "Valeur": 5,
            "Symbole": "🛡",
            "Rareté": "Peu commun",
            "Prix": 50
        },
    "Épée légendaire": {
            "Description": ("Une épée magique et puissante.", "Octroie 10 ATT."),
            "Effet": "+10 ATT",
            "Type": "Arme",
            "Valeur": 10,
            "Symbole": "⚔",
            "Rareté": "Légendaire",
            "Prix": 1000
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
        "Bombe": {
            "Description": ("Un explosif artisanal très dangereux.", "Inflige 100 DEG à l'ennemi"),
            "Effet": "50 DEG",
            "Type": "DEG",
            "Valeur": 50,
            "Symbole": "✸",
            "Rareté": "Rare",
            "Prix": 100
        },
} 

ENNEMIS = {
    "Slimy": {
        "Nom": "Slimy",
        "LVL": 1, "EXP": 20,
        "PV": 30, "PV_MAX": 30,
        "ATT": 3, "DEF": 1, "LUCK": 8,
        "Description": "Un tas de gelée ou de morve ?",
    },
    "Gobelin": {
        "Nom": "Gobelin",
        "LVL": 2, "EXP": 40,
        "PV": 50, "PV_MAX": 50,
        "ATT": 4, "DEF": 2, "LUCK": 10,
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
        "ATT": 5, "DEF": 3, "LUCK": 8,
        "Description": "Un tas d'os articulés",
    },
    "Leprechaun": {
        "Nom": "Leprechaun",
        "LVL": 4, "EXP": 80,
        "PV": 80, "PV_MAX": 80,
        "ATT": 4, "DEF": 4, "LUCK": 15,
        "Description": "Un farfadet irlandais",
        "Or": randint(50, 100),
        "Objets": {
            "Poudre enchantée": 1
        }
    }
}

PRENOMS = ["Alaric", "Balthar", "Cedric", "Darael", "Elowen", "Faelar", "Gwendal", "Havren", "Iriel", "Jorvik", "Korrigan", "Ulric", "Vesper", "Temmie"]

PNJS = {
    "Aubergiste": {
        "Nom": "Balthar",
        "PV": 100, "PV_MAX": 100,
    },
    
    "Marchand": {
        "Nom": "Elowen",
        "PV": 100, "PV_MAX": 100,
        "Objets": {
            "Potion de soin": 10,
            "Potion d'énergie": 10,
            "Poudre enchantée": 5,
            "Fléchette": 10,
            "Bombe": 5,
        },
        "Équipement": {
            "Épée en fer": 1,
            "Armure en fer": 1,
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
            "Difficulté": 1,
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
                    ["Fléchette", 1],
                ]
            },
            "Statut": -1,
            "Type": "Tuer",
            "Difficulté": 2,
            "Cible": "Gobelin",
            "Donneur": "Maire"
        },
        "Squelette": {
            "Nom": "Extermination des Squelettes",
            "Description": "Les Squelettes envahissent la forêt voisine et menacent les récoltes des villageois.",
            "Objectif": "Tuer 3 Squelette",
            "Récompenses": {
                "EXP": 60,
                "Objets": [
                    ["Potion d'énergie", 1],
                ]
            },
            "Statut": -1,
            "Type": "Tuer",
            "Difficulté": 3,
            "Cible": "Squelette",
            "Donneur": "Maire"
        },
    }
}

### Sauvegarde ###
PROFILS = {
    "Profil1": {},
    "Profil2": {},
    "Profil3": {}
}

def sauvegarder_json(profil, savedata={"PERSONNAGE": PERSONNAGE, "INVENTAIRE": INVENTAIRE, "PNJS": PNJS, "QUETES": QUETES, "SONS_ACTIVES": SONS_ACTIVES, "PROGPRINT": PROGPRINT}):
    """Sauvegarde les données du jeu dans un fichier JSON sous le profil spécifié."""
    print("↺ Sauvegarde en cours...")
    wait(1)
    dossier = f"saves/{profil}"
    if not os.path.exists(dossier):
        os.makedirs(dossier)
    nom_fichier = f"{dossier}/save_{datetime.now().strftime('%d%m%Y_%H%M%S')}.json"
    with open(nom_fichier, 'w') as fichier:
        json.dump(savedata, fichier, indent=4)
    playsound("Tidum")
    print(f"🖫 Le jeu a été sauvegardé dans '{nom_fichier}'.")
    wait(0.5)

def charger_json(profil, nom_fichier):
    """Charge les données du jeu depuis un fichier JSON sous le profil spécifié."""
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
    """Affiche le menu de sélection de profil et retourne le profil choisi."""
    playsound("Button")
    print("""
  ╔════════════════════╗
  ║  1)   Profil 1     ║
  ║  2)   Profil 2     ║
  ║  3)   Profil 3     ║
  ╚════════════════════╝\n""")
    choix = -1
    while choix not in ["1", "2", "3"]:
        choix = str(input(">>> ").strip())
    return f"Profil{choix}"

def creer_partie(profil):
    """Crée une nouvelle partie pour le profil spécifié. Retourne les données de sauvegarde initiales."""
    global PERSONNAGE, INVENTAIRE, SONS_ACTIVES, PROGPRINT
    dossier = f"saves/{profil}"
    if os.path.exists(dossier) and os.listdir(dossier):
        playsound("Alerte")
        print(f"⚠ Attention : des sauvegardes existent déjà pour {profil}.")
        confirmation = input("Voulez-vous vraiment créer une nouvelle partie ? (Oui/Non) : ").strip().lower()
        if not confirmation.startswith("o"):
            print("Création annulée.")
            wait(1)
            return
        print("↺ Création de la partie...", 2)
        wait(1)
    nom_perso = input("Comment s'appelle ton personnage ? ").strip()
    if not nom_perso:
        nom_perso = "Darawen"
    perso = PERSONNAGE
    perso["Nom"] = nom_perso
    save_data = {
        "PERSONNAGE" : perso,
        "INVENTAIRE": INVENTAIRE,
        "PNJS": PNJS,
        "QUETES": QUETES,
        "SONS_ACTIVES": SONS_ACTIVES,
        "PROGPRINT": PROGPRINT
    }
    print(f"🛠 Création d'une nouvelle partie sur {profil}...")
    wait(1)
    sauvegarder_json(profil, save_data)
    for pnj in PNJS.values():
        choisir_prenom(pnj)
    parametres = parametrage()
    save_data["SONS_ACTIVES"] = parametres[0]
    save_data["PROGPRINT"] = parametres[1]
    return save_data

def choisir_sauvegarde(profil):
    """Affiche le menu de sélection de sauvegarde pour le profil spécifié et retourne le nom du fichier choisi."""
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
    print("\n🗁 Sauvegardes disponibles :")
    for i, fichier in enumerate(fichiers, 1):
        print(f"  {i}) {fichier}")
    print("  0) Annuler")
    choix = -1
    while choix not in [str(i) for i in range(len(fichiers) + 1)]:
        choix = input(">>> ").strip()
    if choix == "0":
        return None
    return fichiers[int(choix) - 1]

def charger_jeu(save_data):
    """Charge les données du jeu à partir des données de sauvegarde fournies."""
    global SONS_ACTIVES, PROGPRINT, PERSONNAGE, INVENTAIRE, QUETES, PNJS
    if not isinstance(save_data, dict):
        return
    mapping = {
        "SONS_ACTIVES": bool,
        "PROGPRINT": bool,
        "PERSONNAGE": dict,
        "INVENTAIRE": dict,
        "QUETES": dict,
        "PNJS": dict
    }
    for key, expected_type in mapping.items():
        if key in save_data and isinstance(save_data[key], expected_type):
            globals()[key] = deepcopy(save_data[key])
    wait(0.5)
    voir_infos = input("Voulez-vous voir les infos de votre personnage ? (Oui/Non) : ").strip().lower().startswith("o")
    if voir_infos:
        afficher_stats(PERSONNAGE)
        afficher_inventaire(INVENTAIRE)
        wait(1)
        return

def menu_principal():
    """Affiche le menu principal du jeu et gère les choix de l'utilisateur."""
    choix = -1
    while choix not in [0, 1, 2]:
        playsound("Button")
        print("""
        ╔═══════════════════════════╗
        ║  1)   Nouvelle partie     ║
        ║  2)   Charger une partie  ║
        ║  0)   Quitter le jeu      ║
        ╚═══════════════════════════╝\n""")
        choix = input(">>> ").strip()
        if choix == "1":
            profil = choisir_profil()
            save_defaut = creer_partie(profil)
            if save_defaut == None:
                choix = -1
                continue
            charger_jeu(save_defaut)
            return

        elif choix == "2":
            profil = choisir_profil()
            sauvegarde = choisir_sauvegarde(profil)
            if sauvegarde != None:
                save_data = charger_json(profil, sauvegarde)
                if save_data:
                    charger_jeu(save_data)
                return
            else:
                choix = -1
                wait(1)

        elif choix == "0":
            print("À bientôt !")
            wait(1)
            exit()
        
        else:
            playsound("Chip")
            print("⚠ Choix invalide. Veuillez réessayer.")
            wait(1)


#################
### Fonctions ###
#################

### Fonctions de combat ###
def choisir_ennemi(perso=PERSONNAGE, ENNEMIS=ENNEMIS):
    """Choisit un ennemi adapté au niveau du personnage."""
    ENNEMIS_adaptes = [
        ennemi for ennemi in ENNEMIS.values()
        if abs(ennemi["LVL"] - perso["LVL"]) <= 1
    ]
    if not ENNEMIS_adaptes:
        ENNEMIS_adaptes = list(ENNEMIS.values())
    return deepcopy(choice(ENNEMIS_adaptes))

def combat(perso=PERSONNAGE, enn=None, inv=INVENTAIRE):
    """Lance un combat entre le personnage et un ennemi."""
    if enn is None:
        enn = choisir_ennemi()
    NomPerso = perso["Nom"].upper()
    NomEnn = enn["Nom"].upper()
    tour = 0
    stopmusic()

    playsound("Encounter1")
    progprint("⚔ Le combat commence ! ⚔", 3, gras=True)
    progprint(f"   {NomPerso} VS {NomEnn}", 3, gras=True)
    print()
    wait(1)
    playmusic("Combat")

    while perso["PV"] > 0 and enn["PV"] > 0:
        tour += 1
        progprint(f"═════════ Tour n°{tour} ═════════",0.001, gras=True, couleur="light_red", progprint=False)
        print(afficher_barre('PV', perso))
        print(afficher_barre('PV', enn))
        progprint("Que veux-tu faire ?", 0.05)
        
        actions = ["Attaque", f"Attaque critique ({2 * perso['LUCK']}%)", "Objet", "Inspection", "Passer"]
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
                if randint(1, 100) <= 2 * perso["LUCK"]:
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
            seuil_fuite = 30 + enn["LUCK"] - perso["LUCK"]
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
            critique = randint(1, 100) <= enn["LUCK"]
            esquive = randint(1, 100) <= perso["LUCK"]
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
            stopmusic()
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
        stopmusic()
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
        stopmusic()
        playsound("Défaite")
        progprint(f"{result} {NomPerso} n'a pas gagné d'XP.", 5)
        wait(1)
    if any(perso["BONUS"].values()):
        reinitialiser_bonus(perso)
        for stat in ["PV_MAX", "ATT", "DEF", "LUCK"]:
            perso[stat] = calculer_bonus(perso, stat)
        perso["PV"] = min(perso["PV"], perso["PV_MAX"])
    wait(1)
    print()


### Fonctions d'actions ###
def balade(perso=PERSONNAGE, cout_EN=3, continuer=True):
    """Fonction permettant au personnage de se balader et de rencontrer des événements aléatoires."""
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
            action = randint(1, perso["LUCK"])
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
                    if perso["LUCK"] > palier:
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
                    progprint(f"{messages[rarete_objet]} {PERSONNAGE['Nom']} a trouvé {colorer(objet_trouve, couleur.lower())} !", 2)
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
    stopmusic()

def dormir(perso=PERSONNAGE, type_chambre="dehors", dérangé=False, inv=INVENTAIRE):
    """Permet au personnage de dormir et de récupérer de l'énergie et des points de vie."""
    NomPerso = perso["Nom"]
    recup_EN = 0
    recup_PV = 0
    if type_chambre == "dehors":
        recup_EN = 5
        progprint(f"{NomPerso} s'endort craintivement...", 5)
        wait(1)
    elif type_chambre in ["normale", "campement"]:
        recup_EN = 10
        progprint(f"{NomPerso} s'endort tranquillement...", 5)
        wait(1)
    elif type_chambre == "royale":
        recup_EN = 20
        recup_PV = 50
        progprint(f"{NomPerso} s'endort paisiblement...", 5)
        wait(1)
    if dérangé:
        recup_EN //= 2
        recup_PV //= 2
    perso["EN"] = min(perso["EN"] + recup_EN, perso["EN_MAX"])
    if recup_PV > 0:
        perso["PV"] = min(perso["PV"] + recup_PV, perso["PV_MAX"])
    if not dérangé:
        progprint("ᶻ 𝘇𐰁", 50)
        playsound("LevelUp2")
        progprint(f"{NomPerso} s'est bien reposé et récupère {recup_EN} EN.", 2)
        if recup_PV > 0:
            progprint(f"{NomPerso} récupère aussi {recup_PV} PV !", 2)
        wait(1)
    else:
        progprint("ᶻ 𝗓!", 50)
        playsound("Alerte")
        progprint(f"{NomPerso} se réveille brusquement ! (+{recup_EN} EN)", 2)
    print(afficher_barre('EN', perso))
    if recup_PV > 0:
        print(afficher_barre('PV', perso))

### Fonctions d'affichage ###
def afficher_stats(perso=PERSONNAGE):
    """Affiche les statistiques du personnage."""
    calculer_stats_equipement(perso)
    NomPerso = perso['Nom']
    LVL = perso['LVL']
    EXP = afficher_barre('EXP', nom=False)
    PV = afficher_barre('PV', nom=False)
    EN = afficher_barre('EN', nom=False)
    ATT = perso['ATT']
    DEF = perso['DEF']
    LUCK = perso['LUCK']
    longueur = max(44, (len(NomPerso) + 41))
    progprint(f"╔═════════{((longueur - 44) // 2) * '═'} Statistiques de {NomPerso} {((longueur - 44) // 2) * '═'}════════╗", 0.001, gras=True)
    progprint(f"║ ✱  LVL {LVL} {(longueur - len(str(LVL)) - 12) * ' '} ║", 2, gras=True)
    progprint(f"║ ✱  EXP {EXP} {(longueur - len(str(EXP)) + 5) * ' '} {gras('║')}", 2, gras=True)
    progprint(f"║ ✱  PV {PV} {(longueur - len(str(PV)) + 6) * ' '} {gras('║')}", 2, gras=True)
    progprint(f"║ ✱  EN {EN} {(longueur - len(str(EN)) + 6) * ' '} {gras('║')}", 2, gras=True)
    progprint(f"║ ✱  ATT {ATT} {(longueur - len(str(ATT)) - 12) * ' '} ║", 2, gras=True)
    progprint(f"║ ✱  DEF {DEF} {(longueur - len(str(DEF)) - 12) * ' '} ║", 2, gras=True)
    progprint(f"║ ✱  LUCK {LUCK} {(longueur - len(str(LUCK)) - 13) * ' '} ║", 2, gras=True)
    progprint(f"╚{(longueur - 2) * '═'}╝", 0.001, gras=True)

def afficher_inventaire(inv=INVENTAIRE):
    """Affiche l'inventaire du personnage."""
    progprint("\n═════════ Inventaire ═════════", gras=True)
    progprint(gras("Équipement :"), 2)
    for item, quantite in list(inv.get("Équipement", {}).items()):
        details = EQUIPEMENT.get(item, {})
        effet = details.get("Effet", "Effet inconnu")
        if quantite == 0:
            inv["Équipement"].pop(item, None)
        elif quantite in (-1, 1):
            progprint(f"  - {item} : {effet}", 2)
        else:
            progprint(f"  - {item} : {effet} (x{quantite})", 2)
    progprint(gras("Objets :"), 2)
    for objet, quantite in list(inv.get("Objets", {}).items()):
        if quantite != 0:
            details = OBJETS.get(objet, {})
            effet = details.get("Effet", "Effet inconnu")
            progprint(f"  - {objet} : {effet} (x{quantite})", 2)
        else:
            inv["Objets"].pop(objet, None)
    progprint(f"OR : {inv.get('OR', 0)}", 2, gras=True)
    progprint("══════════════════════════════\n", gras=True)

def afficher_barre(type="PV", perso=PERSONNAGE, long_base=20, nom=True):
    """Crée une barre de vie/énergie/expérience pour le personnage."""
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
    """Affiche un menu d'actions et retourne le choix de l'utilisateur."""
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

### Fonctions d'objets ###
def obtenir_details_objet(NomObjet):
    """Retourne les détails d'un objet donné."""
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
    """Utilise un objet sur le personnage ou l'ennemi."""
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

def acheter_objet(perso=PERSONNAGE, inv=INVENTAIRE, marchand=PNJS["Marchand"]):
    """Permet au personnage d'acheter des objets auprès d'un marchand."""
    NomPerso = perso["Nom"]
    NomMarch = marchand["Nom"].capitalize()
    dialogue(NomMarch, f"Voici ce que j'ai en stock.")
    
    def construire_objets_dispos():
        """Construit la liste des objets disponibles à la vente."""
        objets_dispos = []
        for objet in marchand["Objets"]:
            quantite = marchand["Objets"][objet]
            if quantite > 0:
                prix = OBJETS[objet]["Prix"]
                symbole = OBJETS[objet]["Symbole"]
                objets_dispos.append(("Objets", objet, prix, symbole))
        for equip in marchand.get("Équipement", {}):
            quantite = marchand["Équipement"][equip]
            if quantite > 0:
                prix = EQUIPEMENT[equip]["Prix"]
                symbole = EQUIPEMENT[equip]["Symbole"]
                objets_dispos.append(("Équipement", equip, prix, symbole))
        return objets_dispos

    def obtenir_actions(objets_dispos):
        """Retourne la liste des actions d'achat disponibles."""
        actions = []
        for typ, nom, prix, symbole in objets_dispos:
            stock = marchand[typ][nom]
            if stock > 0:
                stock_str = f" (x{stock})" if typ == "Objets" else ""
                actions.append(f"{symbole} {nom}{stock_str} - {prix} OR")
        return actions

    objets_dispos = construire_objets_dispos()
    actions = obtenir_actions(objets_dispos)
    if not actions:
        playsound("Chip")
        dialogue(NomMarch, f"Désolé, je n'ai plus rien en stock !")
        return

    choix = choisir_actions(actions, "Acheter", "Revenir")
    while choix != 0:
        objets_dispos = construire_objets_dispos()
        actions = obtenir_actions(objets_dispos)
        if not actions:
            playsound("Chip")
            dialogue(NomMarch, f"Désolé, je n'ai plus rien en stock !")
            return
        typ, NomItem, prix, _ = objets_dispos[choix - 1]
        stock_actuel = marchand[typ][NomItem]
        
        if stock_actuel <= 0:
            playsound("Chip")
            progprint(f"✘ {NomMarch} n'a plus de {NomItem} en stock.", 2)
            dialogue(NomMarch, f"Oups ! Je crois que je n'en ai plus...")
        elif inv["OR"] >= prix:
            inv["OR"] -= prix
            marchand[typ][NomItem] -= 1
            if NomItem in inv[typ]:
                inv[typ][NomItem] += 1
            else:
                inv[typ][NomItem] = 1
            playsound("Pièce")
            progprint(f"✓ {NomPerso} a acheté {NomItem} pour {prix} OR.", 2)
            progprint(f"OR restant : {inv['OR']} OR", 2)
        else:
            playsound("Chip")
            progprint(f"✘ {NomPerso} n'a pas assez d'or pour acheter {NomItem}.", 2)
        
        objets_dispos = construire_objets_dispos()
        actions = obtenir_actions(objets_dispos)
        if not actions:
            playsound("Chip")
            dialogue(NomMarch, f"Désolé, je n'ai plus rien en stock !")
            return
        
        choix = choisir_actions(actions, "Acheter", "Revenir")
    
    dialogue(NomMarch, f"Merci pour vos achats !", 0)
    calculer_stats_equipement(perso)

def vendre_objet(perso=PERSONNAGE, inv=INVENTAIRE, marchand=PNJS["Marchand"]):
    """Permet au personnage de vendre des objets à un marchand."""
    NomPerso = perso["Nom"]
    NomMarch = marchand["Nom"].capitalize()
    dialogue(NomMarch, f"Que souhaitez-vous me vendre ?")
    objets_dispos = []
    for objet, quantite in inv["Objets"].items():
        if quantite > 0:
            prix = OBJETS[objet]["Prix"] // 2
            stock_marchand = marchand["Objets"].get(objet, 0)
            objets_dispos.append(("Objets", objet, prix, quantite, stock_marchand))
    for equip, quantite in inv["Équipement"].items():
        if quantite > 0:
            prix = EQUIPEMENT[equip]["Prix"] // 2
            objets_dispos.append(("Équipement", equip, prix, quantite, None))
    if not objets_dispos:
        progprint(f"{NomPerso} n'a rien à vendre.", 2)
        return

    actions = []
    for typ, nom, prix, quantite, stock_marchand in objets_dispos:
        actions.append(f"{nom} (x{quantite}) - {prix} OR")

    choix = choisir_actions(actions, "Vendre", "Revenir")
    while choix != 0:
        typ, NomItem, prix, quantite, stock_marchand = objets_dispos[choix - 1]
        if typ == "Objets":
            inv["Objets"][NomItem] -= 1
            marchand["Objets"][NomItem] = marchand["Objets"].get(NomItem, 0) + 1
            inv["OR"] += prix
            playsound("Pièce")
            progprint(f"✓ {NomPerso} a vendu {NomItem} pour {prix} OR.", 2)
            progprint(f"OR total : {inv['OR']} OR", 2)
        else:  # Équipement
            inv["Équipement"][NomItem] -= 1
            inv["OR"] += prix
            playsound("Pièce")
            progprint(f"✓ {NomPerso} a vendu {NomItem} pour {prix} OR.", 2)
            progprint(f"OR total : {inv['OR']} OR", 2)
        
        objets_dispos = []
        for objet, quantite in inv["Objets"].items():
            if quantite > 0:
                prix = OBJETS[objet]["Prix"] // 2
                stock_marchand = marchand["Objets"].get(objet, 0)
                objets_dispos.append(("Objets", objet, prix, quantite, stock_marchand))
        for equip, quantite in inv["Équipement"].items():
            if quantite > 0:
                prix = EQUIPEMENT[equip]["Prix"] // 2
                objets_dispos.append(("Équipement", equip, prix, quantite, None))
        if not objets_dispos:
            progprint(f"{NomPerso} n'a plus rien à vendre.", 2)
            return
        actions = []
        for typ, nom, prix, quantite, stock_marchand in objets_dispos:
            actions.append(f"{nom} (x{quantite}) - {prix} OR")
        choix = choisir_actions(actions, "Vendre", "Revenir")
    dialogue(NomMarch, f"Merci pour vos ventes !", 0)
    calculer_stats_equipement(perso)

### Fonctions de statistiques ###
def verifier_niveau(perso=PERSONNAGE):
    """Vérifie si le personnage a assez d'EXP pour monter de niveau et met à jour ses statistiques en conséquence."""
    while perso["EXP"] >= perso["EXP_MAX"]:
        perso["EXP"] -= perso["EXP_MAX"]
        perso["LVL"] += 1
        perso["EXP_MAX"] = int(perso["EXP_MAX"] * 1.5)
        stats_avant = {
            "PV": perso["PV"],
            "EN": perso["EN"],
            "ATT": perso["ATT"],
            "DEF": perso["DEF"],
            "LUCK": perso["LUCK"]
        }
        perso["PV_MAX"] += 10
        perso["EN_MAX"] += 5
        perso["PV"] = perso["PV_MAX"]
        perso["EN"] = perso["EN_MAX"]
        perso["ATT"] += 2
        perso["ATT_BASE"] += 2
        perso["DEF"] += 1
        perso["DEF_BASE"] += 1
        perso["LUCK"] += 1
        playsound("LevelUp1")
        progprint(f"★ {perso['Nom']} passe au niveau {perso['LVL']} !", 2)
        wait(0.25)
        for stat, ancienne in stats_avant.items():
            nouvelle = perso[stat]
            progprint(f"  {stat}: {ancienne} --> {nouvelle}", 2)
            wait(0.25)
        wait(0.5)

def calculer_bonus(perso, stat):
    """Calcule la statistique totale en ajoutant les bonus temporaires."""
    return perso[stat] + perso["BONUS"].get(stat, 0)

def reinitialiser_bonus(perso, stats=None):
    """Réinitialise les bonus temporaires du personnage pour les statistiques spécifiées ou toutes si aucune n'est donnée."""
    if stats is None:
        stats = perso["BONUS"].keys()
    for stat in stats:
        if stat in perso["BONUS"]:
            perso["BONUS"][stat] = 0
    progprint(f"{perso['Nom']} ressent une rechute d'énergie.", 2)

def calculer_stats_equipement(perso=PERSONNAGE, inv=INVENTAIRE):
    """Calcule les statistiques d'attaque et de défense du personnage en fonction de son niveau et de son équipement."""
    lvl = perso.get("LVL", 1)
    att_base = 2 * lvl + 1
    def_base = lvl + 1
    meilleur_arme_val = 0
    meilleur_armure_val = 0
    for nom, quantite in inv.get("Équipement", {}).items():
        if quantite <= 0:
            continue
        equip = EQUIPEMENT.get(nom)
        if not equip:
            continue
        valeur = equip.get("Valeur", 0)
        typ = equip.get("Type", "").lower()
        if typ == "arme" and valeur > meilleur_arme_val:
            meilleur_arme_val = valeur
        elif typ == "armure" and valeur > meilleur_armure_val:
            meilleur_armure_val = valeur

    perso["ATT_BASE"] = att_base
    perso["DEF_BASE"] = def_base
    perso["ATT"] = att_base + meilleur_arme_val
    perso["DEF"] = def_base + meilleur_armure_val
    return perso["ATT"], perso["DEF"]

### Fonctions de quêtes ###
def donner_quete(quete=None, NomDonneur=None, perso=PERSONNAGE):
    """Propose une quête au personnage et gère son acceptation ou son refus."""
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
    """Termine une quête pour le personnage et lui attribue les récompenses."""
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

### Fonctions autres ###
def choisir_prenom(pnj, prenoms=PRENOMS):
    """Choisit un prénom aléatoire pour le PNJ spécifié."""
    prenom = choice(prenoms)
    prenoms.remove(prenom)
    pnj["Nom"] = prenom


### Village ###
def village(perso=PERSONNAGE, inv=INVENTAIRE):
    """Permet au personnage d'interagir avec les différentes fonctionnalités du village."""
    NomPerso = perso["Nom"]
    playsound("Fuite")
    progprint(f"\n{NomPerso} arrive au village.", 2)
    wait(1)
    print()
    # Lancer la musique du village à l'arrivée
    playmusic("Village", stop=True, volume=0.3)
    actions = ["Mairie", "Boutique", "Auberge", "Fontaine", f"Statistiques de {NomPerso}", "Sauvegarder"]
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
        
        ### Sauvegarder
        elif choix == 6:
            sauvegarder_json("Profil1", {"PERSONNAGE": PERSONNAGE, "INVENTAIRE": INVENTAIRE, "PNJS": PNJS, "QUETES": QUETES, "SONS_ACTIVES": SONS_ACTIVES, "PROGPRINT": PROGPRINT})
            
        # if choix in [1, 2, 3, 4]:
        #     playmusic("Village", stop=True, volume=0.3) # Reprendre la musique du village
        
        choix = choisir_actions(actions, "Village", "Quitter le village")
    
    if perso["EN"] <= 0:
        playsound("Awh")
        progprint(f"{NomPerso} devrait rester un peu au village pour se reposer...")
    else:
        stopmusic()
        playsound("Fuite")
        progprint(f"{NomPerso} quitte le village.", 2)
    wait(1)

### Mairie ###
def mairie(perso=PERSONNAGE):
    """Fonction permettant d'interagir avec la mairie notamment pour obtenir des quêtes."""
    NomPerso = perso["Nom"]
    playsound("Fuite")
    progprint(f"{NomPerso} entre dans la mairie.", 2)
    wait(1)
    NomMaire = PNJS["Maire"]["Nom"].capitalize()
    # Sélection de la quête adaptée
    quetes = list(QUETES["Secondaires"].values())
    quete = None
    for q in quetes:
        if q.get("Difficulté") == perso["LVL"]:
            quete = q
    if quete is None:
        dialogue(NomMaire, f"Ah, {NomPerso}... Tu veux une quête ? Désolé, j'ai rien à ton niveau. Reviens plus tard, hein !", "Gobelin_Rire")
        progprint(f"{NomPerso} se sent légèrement humilié...\n", 2)
        wait(1)
        playsound("Fuite")
        progprint(f"{NomPerso} sort de la mairie.\n", 2)
        return
    
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
    """Fonction permettant d'interagir avec la boutique pour acheter ou vendre des objets."""
    NomPerso = perso["Nom"]
    playsound("Fuite")
    progprint(f"{NomPerso} entre dans la boutique.", 2)
    wait(1)
    NomMarch = PNJS["Marchand"]["Nom"].capitalize()
    if NomMarch == "TEMMIE":  # Easter egg
        playmusic("Boutique", stop=True)
    dialogue(NomMarch, f"Bienvenue à la boutique, {NomPerso} ! Je suis {NomMarch} le Marchand.")
    actions = ["Acheter", "Vendre"]
    choix = choisir_actions(actions, "Boutique", "Revenir au village")
    while choix != 0:
        if choix == 1:
            acheter_objet(perso, inv)
        elif choix == 2:
            vendre_objet(perso, inv)
        choix = choisir_actions(actions, "Boutique", "Revenir au village")
    dialogue(NomMarch, f"Merci et au revoir !", 0)
    playsound("Fuite")
    progprint(f"{NomPerso} sort de la boutique.\n", 2)

### Auberge ###
def auberge(perso=PERSONNAGE, inv=INVENTAIRE):
    """Fonction permettant d'interagir avec l'auberge pour se reposer."""
    NomPerso = perso["Nom"]
    playsound("Fuite")
    progprint(f"{NomPerso} entre dans l'auberge.", 2)
    wait(1)
    NomAuberg = PNJS["Aubergiste"]["Nom"].capitalize()
    dialogue(NomAuberg, f"Bienvenue à l'auberge, {NomPerso} ! Je suis {NomAuberg} l'Aubergiste.", attente=0.75)
    dialogue(NomAuberg, "Nous avons deux types de chambres disponibles.", attente=0.75)
    dialogue(NomAuberg, "Une chambre normale pour 10 pièces d'OR qui vous offre un sommeil réparateur.", attente=0.75)
    dialogue(NomAuberg, "Ou une chambre royale pour 20 pièces d'OR qui vous offre un sommeil divin.", attente=0.75)
    actions = ["Chambre normale - (10 OR)", "Chambre royale - (20 OR)"]
    choix = choisir_actions(actions, "Auberge", "Revenir au village")
    
    ### Chambre normale ###
    if choix == 1:
        if inv["OR"] >= 10:
            inv["OR"] -= 10
            dormir(perso, type_chambre="normale")
        else:
            playsound("Chip")
            dialogue(NomAuberg, f"Désolé {NomPerso} ! Je ne fais pas de crédit. Reviens quand tu es un peu, hmmmmmmm, plus riche !")

    ### Chambre royale ###
    elif choix == 2:
        if inv["OR"] >= 20:
            inv["OR"] -= 20
            dormir(perso, type_chambre="royale")
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
    """Fonction permettant d'interagir avec la fontaine du village."""
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
                if randint(1, 10) * perso["LUCK"] >= 90:
                    playsound("Choeur")
                    progprint(f"La fontaine brille légèrement et {NomPerso} sent une douce chaleur.", 2)
                    wait(1)
                    playsound("LevelUp2")
                    progprint(f"{NomPerso} se sent plus chanceux !", 2)
                    perso["LUCK"] += 1
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
    """Fonction principale d'exécution du jeu."""
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
    for i in range(100):
        village()
        balade()
    print("(・―・) Normalement, ce message ne devrait pas s'afficher")
    wait(3)
    print("(ㆆ_ㆆ) Mais si vous le voyez, c'est que vous avez vraiment forcé")
    wait(2)
    print("Dégagez.")
    exit()


execution()
