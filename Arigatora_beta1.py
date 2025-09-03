# -*- coding: utf-8 -*-

"""
Created on Fri Aug  1 11:30:48 2025

@author: Hugo
"""

# TODO:simplification du code -> moins d'erreurs + pour etre plus facile à écrire
# TODO:mttre en place un vrai menu pause
# TODO: refaire save



import json, pyxel
# {"x": 8, "y": 88,"pos_carte":0, "num_skins":0,"vitesse":2, "coeur":4}
width = 128
height = 128
title = "Arigatora"
pyxel.init(width, height, title)
pyxel.load("2.pyxres")
pyxel.play(0,2, loop=True)


POS_OPTION = 0
position_foret =[0,0,128,112]#position foret dans le stylesheet
position_village = [128, 0, 128,112, 1]
position_habitation = [256, 0, 128, 112]
PAUSE = False


# b = boutique dans un magasin du village
# f foret
# v village
#h habitations
carte = ["f", "v", "h", "h"]
# affichage = [0,1]

# (u, v, w, h)
skins = {"mage": {"pos_tile":[[0,130, 16, -12, 16]]}, "chevalier": {"pos_tile":[[0, 1, 16, 13,16],[0,17,16,14,17]]} }

obj = [{"x":22, "y":87, "w":10, "h":10, "col":2, "partie_carte": 1},{"x":40, "y":66, "w":50, "h":10, "col":2, "partie_carte": 1}]
#position objet physique blt
pnj = [{"x":52, "y":45, "w":10, "h":10, "col":2, "partie_carte": 1}]
# vendeur_maison = 
ensemble_jeux_pnj = [{"x":61, "y":88, "w":10, "h":10, "col":2, "partie_carte": 1}]






class Player:
    def __init__(self):
        self.name = input("Quel est ton nom? ")
        
        self.pos_x = 8
        self.pos_y = 88
        self.pos_carte = 0
        
        
        self.num_skins = 0
        self.nom_skins = "chevalier"
        # TODO: verif num_skin et nom_skin ont des utilités différentes
                    #lequel des skins de skins["chevalier"]["pos_tile"]s par ex
        self.pos_skins = 0
        self.skins_actuel = skins["chevalier"]["pos_tile"][self.pos_skins]
        
        
        self.vitesse = 2
        self.coeur = 5
        self.etat_jeu = "MENU"
        self.sauvegarde = {"name": self.name, "pos_x" : self.pos_x,
                           "pos_y": self.pos_y, "num_skins": self.num_skins,
                           "vitesse": self.vitesse, "coeur": self.coeur,
                           "etat_jeu": "EXPLORATION"}
        self.saut = False
        self.vitesse_chute = 0
        self.long_saut = 25
        
        
        
        
    def update(self):
        
        self.touches()
        self.chg_skins()
        self.incrementation_vitesse_saut()
        self.animation_skin()
        
    
    def collision(self,obj_1):
        """vérifie les collisions avec une entitée"""
        
        # TODO: faire class mur et consommable
        touche = False
        
        for obj in obj_1:
            if obj["partie_carte"] ==Perso.pos_carte:
                
                if Perso.pos_x <= obj["x"]+ obj['w'] and\
                    Perso.pos_x + 14 >= obj["x"] and\
                    Perso.pos_y <= obj["y"]+ obj['h'] and\
                    Perso.pos_y + 15 >= obj["y"]:
                    touche = True
                    return touche  
        return touche
    
    def update_propriete(self):
        
        self.name = self.sauvegarde["name"]
        self.pos_x = self.sauvegarde["pos_x"]
        self.pos_y = self.sauvegarde["pos_y"]
        self.num_skins = self.sauvegarde["num_skins"]
        self.vitesse = self.sauvegarde["vitesse"]
        self.coeur = self.sauvegarde["coeur"]
        
    def commandes(self):
        # essaie de ne pas mettre self
        """permet de lancer des commandes en jeu en appuyant sur U"""
        try:
            commande = input("Quel est le nom de la commande que vous voulez utiliser? ")
            exec(commande)
        except:
            print('Erreur de la commande')
    def chg_skins(self):
        """met à jour le skins dans la base de donnée du perso"""
        
        global skins_actuel, pos_skins, nom_skins, nb_skins
        if self.num_skins == 0:
            self.skins_actuel = skins["chevalier"]["pos_tile"][self.pos_skins]
            nb_skins = len(skins["chevalier"]["pos_tile"])-1
            nom_skins = "chevalier"
            
        elif self.num_skins == 1:
            self.pos_skins = 0
            self.skins_actuel = skins["mage"]["pos_tile"][self.pos_skins]
            nb_skins = len(skins["mage"]["pos_tile"])-1
            nom_skins = "mage"
            
    def animation_skin(self):
        global nb_skins
        
        
        if pyxel.frame_count %16 ==0:
            self.pos_skins += 1
        # print(self.pos_skins)
       
        if self.pos_skins <= nb_skins:
            
            self.skins_actuel = skins[nom_skins]["pos_tile"][self.pos_skins]
            
            
            # print('numéro du skin',nom_skins, self.pos_skins)
        else:
            self.pos_skins =0
            self.skins_actuel = skins[nom_skins]["pos_tile"][self.pos_skins]
        
       
        
        
        
        
        
    def incrementation_vitesse_saut(self):
        """implémente l'accélération dans la descente du sprite"""
       
        if self.saut == True or (self.saut == False and self.collision(obj) == False):
            Perso.pos_y += self.vitesse_chute
            
            if Perso.pos_y > 88:
                Perso.pos_y = 88
                self.saut = False
                self.vitesse_chute = 0
                # print('collision avec le sol')
            elif self.collision(obj) == True:
                while self.collision(obj) == True:
                    self.pos_y -= 1
                self.saut = False
                self.vitesse_chute=0
                
            self.vitesse_chute +=1
        
            
    
            
                                          
        # return touche
    def cg_sens_skins(self, touche):
        if touche == "gauche":
            self.skins_actuel[3] = abs(self.skins_actuel[3])*-1
        elif touche == "droite":
            self.skins_actuel[3] = abs(self.skins_actuel[3])
        
    def touches(self):
        global carte, PAUSE
        """prise en compte des touches pressées par le joueur"""
        
        
        
        dx = 0
        
        if self.etat_jeu == "EXPLORATION":
        
            if pyxel.btn(pyxel.KEY_LEFT):
                dx = -1
                self.cg_sens_skins("gauche")
                
                
                
                if self.collision(obj) == True:
                    self.pos_x += dx #une position après
                    if self.collision(obj) == True:
                        self.pos_x -= dx
                        dx = 0
                        
                    else:
                        self.pos_x -= dx
                
                    
                
                
                
                if self.pos_x < 0:
                    # perso["x"] = 0
                    if self.pos_carte >=1:
                        self.pos_x = 113
                        self.pos_carte -= 1
                        # changement_carte(1)
                        
                        
                    else: 
                        self.pos_carte = 0
                        self.pos_x = 4
                        
                   
                
            if pyxel.btn(pyxel.KEY_RIGHT):
                
                self.cg_sens_skins("droite")
                dx = 1
                if self.collision(obj) == True:
                    self.pos_x += dx
                    if self.collision(obj) == True:
                        self.pos_x -= dx
                        dx = 0
                    else:
                        self.pos_x -= dx
                    
                    
                    
                    
                if self.pos_x + self.skins_actuel[3] > pyxel.width:
                    # perso["x"] = pyxel.width-skins_actuel[3]
                    
                    
                    if len(carte)-1 > self.pos_carte:
                        self.pos_x = 2
                        self.pos_carte += 1
                    else: 
                        dx = 0
            
            if pyxel.btnp(pyxel.KEY_SPACE):
                if self.saut == False:
                    self.vitesse_chute = 0
                    self.pos_y -= self.long_saut
                    self.saut = True
                    if self.collision(obj) == True:
                        self.long_saut += self.long_saut
                        self.saut = False
                    
                
            
                # commandes() 
            if pyxel.btn(pyxel.KEY_U):
                self.commandes()
                    
                        
            # elif pyxel.btnp(pyxel.KEY_UP):
            #     perso['y'] -=1
            
            # elif pyxel.btnp(pyxel.KEY_DOWN):
            #     perso['y'] +=1
            
            
            
            elif pyxel.btnp(pyxel.KEY_S):            
                # nom_fichier =  str(name) +".json"
                self.sauvegarder(self.name, self.sauvegarde)
                print("fin de save")
            
            
               
            elif pyxel.btnp(pyxel.KEY_P):
                if PAUSE == False:
                    PAUSE = True
                else:
                    PAUSE= False   
        
            
        self.pos_x += dx * self.vitesse
    def sauvegarder(self, name, chose_dump):
        """cree fichier a partir de rien ou"""
        nom_fichier = str(name)+".json"
        
        
        with open(nom_fichier ,"w") as fichier:
            json.dump(chose_dump, fichier)
            return fichier
            
    
    def lecture_sauvegarde(self, name):
        """chargement de la sauvegarde"""
        nom_fichier = str(name)+".json"
        
        try:
            # si save
            with open(nom_fichier ,"r") as fichier:
                
                sauvegarde = json.load(fichier)
                return sauvegarde
            
        except:
            # sans save
            
            self.sauvegarder(name, self.sauvegarde)
            with open(nom_fichier ,"r") as fichier:
                sauvegarde = json.load(fichier)
                
                return sauvegarde



    

    


def menu(col, titre, list_option):
    pyxel.cls(col)
    pyxel.text(2, 2,title , 4)
    affichage_sandwich(list_option)
    selection_option(list_option)
    
    if titre == "Boutique":
        pyxel.bltm(0, 56 ,0,0,192, 128,64, colkey=2)
    elif titre == "Menu Pause":
        pyxel.bltm(0, 56 ,0,0,128, 128,64, colkey=2)
        pyxel.bltm(9, 60, 0, 16*8, 16*8, 16, 24)
        #-> cadre
    
def initialisation_affichage():
    global carte
    """affichage EXPLORATION"""
    if Perso.etat_jeu == "EXPLORATION":
        if carte[Perso.pos_carte] == "f":
            
            pyxel.bltm(0 , 0, 0, position_foret[0], position_foret[1], position_foret[2], position_foret[3], colkey=2)
                                                 #u                  v               w                   h
        elif carte[Perso.pos_carte] == "v":
            
            pyxel.bltm(0 , 0, 0, position_village[0], position_village[1], position_village[2], position_village[3], colkey=2)        
        elif carte[Perso.pos_carte] == "h":
            pyxel.bltm(0 , 0, 0, position_habitation[0], position_habitation[1], position_habitation[2], position_habitation[3], colkey=2)
            
            
            
        pyxel.bltm(0, 112, 0, 0, 112, 128, 16,colkey=2)                                        
        
        pyxel.text(5, 118, "Bonjour", 4)
        
def creation_obj():
    """crée les objets sur le passage, ou avec qui on peut interragir
    coffre, blocs ou plateformes"""
    
    for pnj_1 in pnj:
        
        if pnj_1["partie_carte"] == Perso.pos_carte:
            pyxel.blt(pnj_1["x"], pnj_1['y'], 0,130,16,12,15, colkey=2)
        
    for obj_1 in obj:
        
        if obj_1["partie_carte"] == Perso.pos_carte:
            pyxel.rectb(obj_1["x"],obj_1["y"],obj_1["w"], obj_1["h"], obj_1["col"])
    for jeux in ensemble_jeux_pnj:
        if jeux["partie_carte"] == Perso.pos_carte:
            pyxel.blt(jeux["x"], jeux['y'], 0,130,16,12,15, colkey=2)

   
    
    
    # # pyxel.text(7, 86, nom_skins, 4)#nom
    # for i in range(Perso.coeur):
    #     pyxel.blt(4*(i+1), 92, 0, 115, 52, 10, 9, colkey=2)
    #     pyxel.text(4, 100, "attaque", 4)

def regles():
    pass

def commandes():
    """permet de lancer des commandes en jeu en appuyant sur U"""
    try:
        commande = input("Quel est le nom de la commande que vous voulez utiliser? ")
        exec(commande)
    except:
        print('Erreur de la commande')            

def selection_option(list_option):
    """selection des options avec touches du clavier"""
    global PAUSE, POS_OPTION
    if pyxel.btnp(pyxel.KEY_UP):
        POS_OPTION -= 1
    elif pyxel.btnp(pyxel.KEY_DOWN):
        POS_OPTION +=1
        
        
    if POS_OPTION >= len(list_option):
        
        POS_OPTION = 0
       
    elif POS_OPTION < 0:
        POS_OPTION = len(list_option) -1
        
    if Perso.etat_jeu == "MENU":
        if pyxel.btnp(pyxel.KEY_RETURN):
            
            
            if POS_OPTION == 0:
                Perso.sauvegarder(Perso.name, Perso.sauvegarde)
                print('Nouvelle sauvegarde en cour ...')
            elif POS_OPTION == 1:
                Perso.lecture_sauvegarde(Perso.name)
                print('Lecture de la sauvegarde en cour ...')
       
            Perso.etat_jeu = "EXPLORATION"
            
        # else:
        #     raise "ERROR{type:OPTION>/<1/0}"
    elif PAUSE == True:
        if pyxel.btnp(pyxel.KEY_RETURN):
            
            
            if POS_OPTION == 0:
                
                print('changement skins en cour ...')
            elif POS_OPTION == 1:
                Perso.sauvegarder(Perso.name, Perso.sauvegarde)
                print('En cour de Sauvegarde ...')
            elif POS_OPTION == 2:
                with open("Documentation.txt", "r") as file:
                    reading_file = file.read()
                    
                    print(reading_file)
                
                
                
                
            elif POS_OPTION == 3:
                print('Sortie de pause')
                PAUSE = False
                
    elif Perso.etat_jeu =="BOUTIQUE":
        if pyxel.btnp(pyxel.KEY_RETURN):
            if POS_OPTION == 4:
                Perso.etat_jeu = "EXPLORATION"
                # perso["x"] -= der_mouv
                print(Perso.etat_jeu)
        
    pyxel.text(0, 8+(8*POS_OPTION), "*", 2)
    
def affichage_sandwich(list_option):
    i = 0
    for option in list_option.values():
        
        pyxel.text(2, 8+(8*i), option , 8)
        i+=1

    
 
Perso = Player()

def interaction_pnj():
    if Perso.etat_jeu == "EXPLORATION":
        
        
        if Perso.collision(pnj) == True and pyxel.btnp(pyxel.KEY_E)== True:
            Perso.etat_jeu = "BOUTIQUE"
            Perso.pos_x -= 10
        # if Perso.collision(ensemble_jeux_pnj) == True and pyxel.btnp(pyxel.KEY_E)== True:
        #     Perso.etat_jeu = "MINI_JEU"
        #     Perso.pos_x -= 10
        
        Perso.chg_skins()
        
    # elif Perso.etat_jeu == "MINI_JEU":
    #     pass
    

def update():
    global PAUSE
    
    
    if PAUSE == False:
        interaction_pnj()
    Perso.update()
    
    
def draw():   
    
    if PAUSE == False:
        if Perso.etat_jeu == "EXPLORATION":
            pyxel.cls(11)
            initialisation_affichage()
            creation_obj()
            pyxel.blt(Perso.pos_x, Perso.pos_y, 0, Perso.skins_actuel[1], Perso.skins_actuel[2], Perso.skins_actuel[3],Perso.skins_actuel[4], colkey=2)#rotate=45
            
            
        
        
            
    
    
    
    #affichage différents menu
    if Perso.etat_jeu == "MENU":
        menu(6, "Arigatora", {0: "Nouvelle Sauvegarde",
                 1: "Reprendre Sauvegarde"})
        
     
    
    elif Perso.etat_jeu == "BOUTIQUE":
        
        menu(6, "Boutique", {0:"Changer de skins",
                  1: "Boosts(potions)",
                  2: "Armes",
                  3: "Familiers",
                  4:"Sortir"})
    elif PAUSE == True:
        # col -> 15 ou 6
        menu(15, "Menu Pause", list_option = {0:"Changer de skins",
                   1: "Sauvegarder",
                   2: "Aide + ameliorations prevues",
                   3: "Sortir"})
    
        
pyxel.run(update, draw)

