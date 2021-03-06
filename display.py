import pygame
from pygame.locals import *
from create_button import button
from Shop import shop
from Hive import hive
from math import floor

class display():
    
    def __init__(self):
        self._button_dic = {}
        self._background = None
    
    def display_new_game(self, w, h, first_time):
        surface = pygame.Surface((1920,1080))
        self._background = pygame.image.load('./Images/greywp.jpg')
        surface.blit(self._background, (0, 0))
        logo = pygame.image.load('./Images/logo.png')
        surface.blit(logo, (0,0))
        if first_time is True:
            self._button_dic = {
                "launch_game_button" : button((255,180,255), 720, 100, 480, 100, w, h, 'Nouvelle Partie', sizeFont=60)
            }
        else:
             self._button_dic = {

                "launch_game_button" : button((255,180,255), 720, 100, 480, 100, w, h, 'Continuer Partie', sizeFont=60)
            }

        self._button_dic['launch_game_button'].draw_button(surface)

        return surface
    
    def standard_line(self, surface):
        pygame.draw.rect(surface, (255, 247, 153), (0,0,1920,50))
        # pygame.draw.line(surface, (0,0,0), (0, 0), (1920, 0), 10)
        pygame.draw.line(surface, (0,0,0), (0, 50), (1920, 50), 5)
        # pygame.draw.line(surface, (0,0,0), (0, 0), (0, 50), 10)
        pygame.draw.line(surface, (0,0,0), (1920, 0), (1920, 50), 10)
        pygame.draw.line(surface, (0,0,0), (290, 0), (290, 50), 3)
        pygame.draw.line(surface, (0,0,0), (588, 0), (588, 50), 3)
        pygame.draw.line(surface, (0,0,0), (894, 0), (894, 50), 3)
        pygame.draw.line(surface, (0,0,0), (1190, 0), (1190, 50), 3)
        pygame.draw.line(surface, (0,0,0), (1486, 0), (1486, 50), 3)
        return surface

    def display_menu(self, w, h):
        surface = pygame.Surface((1920,1080))
        # On désinitialise nos boutons quit et launch
        self._button_dic = {
            "bees_button" : button((212,180,0), 720, 203, 480, 75, w, h, 'Gestion des Abeilles', sizeFont=50),
            "upgrade_button" : button((212,180,0), 720, 403, 480, 75, w, h, 'Améliorations', sizeFont=50),
            "shop_button" : button((212,180,0), 720, 603, 480, 75, w, h, 'Magasin', sizeFont=50),
            "fight_menu_button" : button((212,180,0), 720, 803, 480, 75, w, h, 'Combat!', sizeFont=50),
            "quit_button" : button((212,180,0), 1720, 985, 180, 75, w, h,'Quitter', font='comicsans', sizeFont=50)
        }
        
        #On redessine le background
        #self._background.fill((255,255,255))
        surface.blit(self._background, (0, 0))
        #Bouton Bees
        self._button_dic['bees_button'].draw_button(surface)
        #Boutons upgrade
        self._button_dic['upgrade_button'].draw_button(surface)
        #Bouton Shop
        self._button_dic['shop_button'].draw_button(surface)
        #Bouton Fight
        self._button_dic['fight_menu_button'].draw_button(surface)
        # Bouton Quitter
        self._button_dic['quit_button'].draw_button(surface)
        
        surface = self.standard_line(surface)

        return surface

    # def display_fight_upgrades(self, w, h, hive):
    #     surface = pygame.Surface((1920,1080))
    #     surface.blit(self._background, (0, 0))
        

    #     self._button_dic = {
    #         "back_button" : button((212,180,0), 1720, 985, 180, 75, w, h,'Retour', font='comicsans', sizeFont=50)
    #     }
    #     self._button_dic["back_button"].draw_button(surface)
        
    #     return surface
    
    def display_upgrades(self, w, h, hive, upgrade_type):
        # name, lvl, required_level , price, category, possession, placement = (0,0)

        # mettre les bonnes upgrades
        upgrades = []
        for row in hive._upgrades:
            if row._category == upgrade_type:
                upgrades.append(row)
        print(upgrades)
        # upgrades = hive._upgrades
        surface = pygame.Surface((1920,1080))
        surface.blit(self._background, (0, 0))

        # Déterminer la taille de la matrice
        #print(range (0, len(upgrades) - 1))
        max_x = 0
        max_y = 0
        for i in range (0, len(upgrades) - 1): 
            #print(f"upgrade i: {upgrades[i]._placement[0]}  upgrade i+1: {upgrades[i + 1]._placement[0]}")
            if upgrades[i]._placement[0] > upgrades[i + 1]._placement[0]:
                max_x = upgrades[i]._placement[0]
            elif upgrades[i]._placement[0] < upgrades[i + 1]._placement[0]:
                max_x = upgrades[i + 1]._placement[0]
            if upgrades[i]._placement[1] > upgrades[i + 1]._placement[1]:
                max_y = upgrades[i]._placement[1]
            elif upgrades[i]._placement[1] < upgrades[i + 1]._placement[1]:
                max_y = upgrades[i + 1]._placement[1]
        
        # Création de la matrice des upgrades
        list_up = [[0 for i in range(max_y + 1)] for j in range(max_x + 1)]

        for upgrade in upgrades:
            list_up[upgrade._placement[0]][upgrade._placement[1]] = upgrade

        # print(list_up)

        # taille de la surface
        width = 1200 
        height = 600
        total_height = 0
        font = pygame.font.SysFont('comicsans', 50)
        surface_dic = {}
        surface_dic['surface'] = []
        surface_dic['buttons'] = []
        cpt = -1

        for row in list_up:
            surface_dic['surface'].append(pygame.Surface((width, height), pygame.SRCALPHA))
            cpt += 1
            total_height += height
            x = 0
            for upgrade in row:
                if upgrade != 0:
                    image = pygame.image.load(upgrade.sprite())
                    surface_dic['surface'][cpt].blit(image, (x, 55))
                    prod = font.render(upgrade.name() + " lvl" + str(upgrade.lvl()) , 1, (0,0,0))
                    surface_dic['surface'][cpt].blit(prod, (x, 0))

                    print(f"test {upgrade.name()} {upgrade.possession()}")

                    prix = font.render( "Prix: " + str(upgrade.price()[1]), 1, (0,0,0))
                    surface_dic['surface'][cpt].blit(prix, (x, 300))

                    if upgrade.price()[0] == "honey":
                        image = pygame.image.load("./Images/honey.png")
                        surface_dic['surface'][cpt].blit(pygame.transform.scale(image, (45, 45)), ( x + 80 + 20*len(str(upgrade.price()[1])), 293 ))
                    elif upgrade.price()[0] == "water":
                        image = pygame.image.load("./Images/water.png")
                        surface_dic['surface'][cpt].blit(pygame.transform.scale(image, (30, 30)), ( x + 90 + 20*len(str(upgrade.price()[1])), 300 ))
                    elif upgrade.price()[0] == "metal":
                        image = pygame.image.load("./Images/metal.png")
                        surface_dic['surface'][cpt].blit(pygame.transform.scale(image, (30, 30)), ( x + 90 + 20*len(str(upgrade.price()[1])), 300 ))
                    elif upgrade.price()[0] == "uranium":
                        image = pygame.image.load("./Images/uranium.png")
                        surface_dic['surface'][cpt].blit(pygame.transform.scale(image, (30, 30)), ( x + 90 + 20*len(str(upgrade.price()[1])), 300 ))
                    elif upgrade.price()[0] == "pollen":
                        image = pygame.image.load("./Images/pollen.png")
                        surface_dic['surface'][cpt].blit(pygame.transform.scale(image, (30, 30)), ( x + 90 + 20*len(str(upgrade.price()[1])), 300 ))
                    
                    if upgrade.required_level() > hive.level():
                        button_temp = button((169, 169, 169), x, 450, 300, 75, w, h,"Niveau " + str(upgrade.required_level()) + " requis" , font='comicsans', sizeFont=50, get=None)
                        surface_dic["buttons"].append(button_temp)
                        button_temp.draw_button(surface_dic["surface"][cpt])
                    elif upgrade.possession() == True:
                        button_temp = button((169, 169, 169), x, 450, 300, 75, w, h,"Possédé" , font='comicsans', sizeFont=50, get=None)
                        surface_dic["buttons"].append(button_temp)
                        button_temp.draw_button(surface_dic["surface"][cpt])
                    else:
                        button_temp = button((212,180,0), x, 450, 300, 75, w, h, "Acheter", font='comicsans', sizeFont=50, get = [upgrade.name(),upgrade.lvl(),upgrade.category()])
                        surface_dic["buttons"].append(button_temp)
                        button_temp.draw_button(surface_dic["surface"][cpt])

                    button_temp = button((212,180,0), x, 350, 300, 75, w, h, "Description", font='comicsans', sizeFont=50, get = ["description",upgrade.name(),upgrade.lvl()])#[upgrade.name(),upgrade.lvl()])
                    surface_dic["buttons"].append(button_temp)
                    button_temp.draw_button(surface_dic["surface"][cpt])

                x += 400

        final_surface = pygame.Surface((width, total_height), pygame.SRCALPHA)
        y = 0
        for surface_temp in surface_dic['surface']:
            final_surface.blit(surface_temp, (0, y))
            y += height

        surface_dic['surface'] = final_surface  

        
        # Détermine le nombre d'amélioration par ligne (utile pour déterminer la position des boutons)
        cpt_list = [0 for y in range(len(list_up))]
        for i in range(0, len(list_up)):
            for thing in list_up[i]:
                if thing != 0:
                    cpt_list[i] += 1

        
        for i in range (0, len(surface_dic["buttons"])):
            surface_dic["buttons"][i]._x += 400
            surface_dic["buttons"][i]._y += 200

        # decal = 200
        # total_height = 375
        # but_id = -1
        # print(cpt_list)
        # for value in cpt_list:
        #     for i in range(value):
        #         but_id += 1
        #         surface_dic["buttons"][but_id]._y = total_height
        #         surface_dic["buttons"][but_id + 1]._y = total_height + 100
        #     total_height += decal

        

        but_id = 0
        decal = height
        butt_id = cpt_list[0] * 2
        for i in range (1, len(cpt_list)):
            for j in range (0, cpt_list[i]):
                surface_dic['buttons'][butt_id]._y += decal
                butt_id += 1
                surface_dic['buttons'][butt_id]._y += decal
                butt_id += 1
            decal += height


        # for i in range (3, len(surface_dic['buttons'])):
            
        #     if i % 3 == 0 and i != 3:
        #         value += height
        #     surface_dic['buttons'][i]._y += value

        
        # for butts in surface_dic["buttons"]:
            

        self._button_dic["back_button"] = button((255,180,255), 1720, 985, 180, 75, w, h,'Retour', font='comicsans', sizeFont=50)
        
        self._button_dic["back_button"].draw_button(surface)

        surface = self.standard_line(surface)

        return surface, surface_dic

    def display_map(self, w, h):
        surface = pygame.Surface((1920,1080))

        map_pic = pygame.image.load('./Images/last.jpg')
        surface.blit(map_pic, (0, 0))

        self._button_dic = {
            "ennemy_ter" : [
                button((0,0,0), 328, 42, 270, 118, w, h,'hauteurs', font='comicsans', sizeFont=50),
                button((0,0,0), 497, 205, 186, 131, w, h,'urbaines', font='comicsans', sizeFont=50),
                button((0,0,0), 770, 16, 236, 100, w, h,'profondeurs', font='comicsans', sizeFont=50),
                button((0,0,0), 1218, 135, 183, 118, w, h,'mutantes', font='comicsans', sizeFont=50),
                button((0,0,0), 714, 277, 184, 75, w, h,'plaines', font='comicsans', sizeFont=50),
                button((0,0,0), 694, 436, 203, 86, w, h,'solitaires', font='comicsans', sizeFont=50),
                button((0,0,0), 628, 628, 208, 176, w, h,'arboricoles', font='comicsans', sizeFont=50),
                button((0,0,0), 1155, 591, 178, 205, w, h,'ruines', font='comicsans', sizeFont=50),
                button((0,0,0), 1049, 799, 180, 78, w, h,'eau douce', font='comicsans', sizeFont=50),
                button((0,0,0), 1088, 938, 84, 113, w, h,'tour', font='comicsans', sizeFont=50),
                button((0,0,0), 1442, 377, 217, 241, w, h,'macabres', font='comicsans', sizeFont=50),
                button((0,0,0), 317, 876, 79, 111, w, h,'RUSSIA', font='comicsans', sizeFont=50),
                button((0,0,0), 252, 356, 193, 313, w, h,'rurales', font='comicsans', sizeFont=50)
            ],
            "back_button" : button((255,180,255), 1720, 985, 180, 75, w, h,'Retour', font='comicsans', sizeFont=50)
        }
        self._button_dic["back_button"].draw_button(surface)
    
        return surface

    def display_management_bee(self, bees, w, h, scroll_y):
        
        font = pygame.font.SysFont('comicsans', 50)
        
        i = 0
        
        surface_dic = {}
        surface_dic['surface'] = []
        surface_dic['buttons'] = []
        height = 550
        width = 1800
        total_height = 0
        
        for i in range (0, len(bees)):
            
            indice = floor(i / 3) # Pour accéder à la bonne surface
           
            if i % 3 == 0:
                x = 100
                surface_dic['surface'].append(pygame.Surface((width, height), pygame.SRCALPHA)) # pygame.SRCALPHA créé une surface transparente dans laquelle on peut ajouter des éléments qui eux s'afficheront 
                total_height += height

            # nom abeille 
            nom_abeille = font.render(bees[i][0]._name, 1, (0,0,0))
            surface_dic['surface'][indice].blit(nom_abeille, (x, 0))

            # image abeille
            image = pygame.image.load(bees[i][0]._sprite)
            surface_dic['surface'][indice].blit(image, (x, 20))

            quantity = font.render("Quantité: " + str(bees[i][1]), 1, (0,0,0))
            surface_dic['surface'][indice].blit(quantity, (x, 300))



            if bees[i][0].category() == "worker":
                tot_prod = bees[i][0].prod() * bees[i][1]
                prod = font.render("PT: " + str(tot_prod) + "    /s" , 1, (0,0,0))
                surface_dic['surface'][indice].blit(prod, (x, 350))

                if bees[i][0].ressource() == "honey":
                    image = pygame.image.load("./Images/honey.png")
                    surface_dic['surface'][indice].blit(pygame.transform.scale(image, (45, 45)), ( x + 55 + 21*len(str(tot_prod)), 343))
                elif bees[i][0].ressource() == "water":
                    image = pygame.image.load("./Images/water.png")
                    surface_dic['surface'][indice].blit(pygame.transform.scale(image, (30, 30)), ( x + 65 + 21*len(str(tot_prod)), 350 ))
                elif bees[i][0].ressource() == "metal":
                    image = pygame.image.load("./Images/metal.png")
                    surface_dic['surface'][indice].blit(pygame.transform.scale(image, (30, 30)), ( x + 65 + 21*len(str(tot_prod)), 350 ))
                elif bees[i][0].ressource() == "uranium":
                    image = pygame.image.load("./Images/uranium.png")
                    surface_dic['surface'][indice].blit(pygame.transform.scale(image, (30, 30)), ( x + 65 + 21*len(str(tot_prod)), 350 ))
                elif bees[i].ressource() == "pollen":
                    image = pygame.image.load("./Images/pollen.png")
                    surface_dic['surface'][indice].blit(pygame.transform.scale(image, (30, 30)), ( x + 65 + 21*len(str(tot_prod)), 350 ))

            else:
                image = pygame.image.load("./Images/sword.png")
                surface_dic['surface'][indice].blit(pygame.transform.scale(image, (30, 30)), ( x + 110 + 21*len(str(bees[i][0].strength() * bees[i][1])), 350 )) 

                strength = font.render("PDCT: " + str(bees[i][0].strength() * bees[i][1]) , 1, (0,0,0))
                surface_dic['surface'][indice].blit(strength, (x, 350))

            print(bees[i][0].cost() * bees[i][1])

            CET = font.render("CET: " + str(bees[i][0].cost() * bees[i][1]), 1, (0,0,0))
            surface_dic['surface'][indice].blit(CET, (x, 400))
            if bees[i][0]._price[1] == "honey":
                image = pygame.image.load("./Images/honey.png")
                surface_dic['surface'][indice].blit(pygame.transform.scale(image, (45, 45)), ( x + 80 + 21*len(str(bees[i][0].cost() * bees[i][1])), 393))
            elif bees[i][0]._price[1] == "water":
                image = pygame.image.load("./Images/water.png")
                surface_dic['surface'][indice].blit(pygame.transform.scale(image, (30, 30)), ( x + 90 + 21*len(str(bees[i][0].cost() * bees[i][1])), 400 ))
            elif bees[i][0]._price[1] == "metal":
                image = pygame.image.load("./Images/metal.png")
                surface_dic['surface'][indice].blit(pygame.transform.scale(image, (30, 30)), ( x + 90 + 21*len(str(bees[i][0].cost() * bees[i][1])), 400 ))
            elif bees[i][0]._price[1] == "uranium":
                image = pygame.image.load("./Images/uranium.png")
                surface_dic['surface'][indice].blit(pygame.transform.scale(image, (30, 30)), ( x + 90 + 21*len(str(bees[i][0].cost() * bees[i][1])), 400 ))
            elif bees[i][0]._price[1] == "pollen":
                image = pygame.image.load("./Images/pollen.png")
                surface_dic['surface'][indice].blit(pygame.transform.scale(image, (30, 30)), ( x + 90 + 21*len(str(bees[i][0].cost() * bees[i][1])), 400 ))

            # boutons
            bouton = button((212,180,0), x, 450, 390, 75, w, h,'Supprimer', font='comicsans', sizeFont=50, get=bees[i][0]._name)
            surface_dic['buttons'].append(bouton)
            bouton.draw_button(surface_dic['surface'][indice])

            x += 500 

        for i in range (0, len(surface_dic['buttons'])):
            surface_dic['buttons'][i]._x += 150
            surface_dic['buttons'][i]._y += 250 + scroll_y

        value = 550
        for i in range (3, len(surface_dic['buttons'])):
            
            if i % 3 == 0 and i != 3:
                value += 550
            surface_dic['buttons'][i]._y += value


        final_surface = pygame.Surface((width, total_height), pygame.SRCALPHA)
        y = 0
        for surface in surface_dic['surface']:
            final_surface.blit(surface, (0, y))
            y += height
        
        surface_dic['surface'] = final_surface
        
        return surface_dic

    def display_management(self, w, h, hive, scroll_y):
        surface = pygame.Surface((1920,1080))
        self._button_dic = {
            "back_button" : button((255,180,255), 1720, 985, 180, 75, w, h, 'Retour', sizeFont=50),
        }
        
            
        # Affichage basique
        surface.blit(self._background, (0, 0))
         
        font = pygame.font.SysFont('comicsans', 40)
        pygame.draw.rect(surface, (255, 247, 153), (0,50,1920,115))
        pygame.draw.line(surface, (0,0,0), (0, 105), (1920, 105), 5) 
        pygame.draw.line(surface, (0,0,0), (0, 165), (1920, 165), 5) 
        

        pygame.draw.line(surface, (0,0,0), (290, 50), (290, 103), 3)
        pygame.draw.line(surface, (0,0,0), (588, 50), (588, 103), 3)
        pygame.draw.line(surface, (0,0,0), (894, 50), (894, 103), 3)
        pygame.draw.line(surface, (0,0,0), (1190, 50), (1190, 103), 3)
        pygame.draw.line(surface, (0,0,0), (1486, 50), (1486, 103), 3)

        



        #infos de la ruche
        bees_possessed = font.render("Abeilles possédées: " + str(len(hive._bees)), 1, (0,0,0))
        surface.blit(bees_possessed, (230, 125))

        nbr_fighter = 0
        tot_strength = 0
        for bee in hive._bees:
            if bee._category == "fighter":
                nbr_fighter += 1
                print(hive.calcul_upgrade_fight(bee))
                tot_strength = tot_strength + bee._strength * hive.calcul_upgrade_fight(bee)

        nbr_worker = len(hive._bees) - nbr_fighter

        fighter = font.render("Combattantes: " + str(nbr_fighter), 1, (0,0,0))
        surface.blit(fighter, (650, 125))

        worker = font.render("Ouvrières: " + str(nbr_worker), 1, (0,0,0))
        surface.blit(worker, (1050, 125))

        strength = font.render("Force d'armée: " + str(int(tot_strength)), 1, (0,0,0))
        surface.blit(strength, (1450, 125))

        # territoires

        #infos sur les abeilles possédées
        list_bee = {}
        if len((hive._bees)) > 0:
            #ON FAIT DE LA MAGIE CIANTE
            list_bee = {}
            
            for bee in hive._bees:
                if bee._name not in list_bee:
                    list_bee[bee._name] = [bee, 1]
                else:
                    list_bee[bee._name][1] += 1 
            list_bee.items()
            list_bee = list_bee.values()
            list_bee = list(list_bee)

        bees_surface = self.display_management_bee(list_bee, w, h, scroll_y)
        self._button_dic["back_button"].draw_button(surface)

        surface = self.standard_line(surface)

        font = pygame.font.SysFont('comicsans', 20)

        PT = font.render("PT: Production totale", 1, (0,0,0))
        surface.blit(PT, (1700, 180))
        PDC = font.render("PDCT: Points de combat totaux", 1, (0,0,0))
        surface.blit(PDC, (1700, 200))
        CE = font.render("CET: Coût d'entretien total", 1, (0,0,0))
        surface.blit(CE, (1700, 220))

        font = pygame.font.SysFont('comicsans', 40)

        terr = hive.calcul_territory_space()
        
        hon = font.render(str(terr["honey"][0]) + " / " + str(terr["honey"][1]), 1, (0,0,0))
        surface.blit(hon, (95, 65))
        hon = font.render(str(terr["water"][0]) + " / " + str(terr["water"][1]), 1, (0,0,0))
        surface.blit(hon, (400, 65))
        hon = font.render(str(terr["metal"][0]) + " / " + str(terr["metal"][1]), 1, (0,0,0))
        surface.blit(hon, (700, 65))
        hon = font.render(str(terr["uranium"][0]) + " / " + str(terr["uranium"][1]), 1, (0,0,0))
        surface.blit(hon, (1010, 65))
        hon = font.render(str(terr["pollen"][0]) + " / " + str(terr["pollen"][1]), 1, (0,0,0))
        surface.blit(hon, (1300, 65))

        hon = font.render(": Occupation des territoires", 1, (0,0,0))
        surface.blit(hon, (1500, 65))
             
        return surface, bees_surface
    
    def display_shop_bee(self, bees, hive, w, h):
        
        font = pygame.font.SysFont('comicsans', 50)
        
        i = 0
        
        surface_dic = {}
        surface_dic['surface'] = []
        surface_dic['buttons'] = []
        height = 550
        width = 1800
        total_height = 0
        for i in range (0, len(bees)):
            
            indice = floor(i / 3) # Pour accéder à la bonne surface
            
           
            if i % 3 == 0:
                x = 100
                surface_dic['surface'].append(pygame.Surface((width, height), pygame.SRCALPHA)) # pygame.SRCALPHA créé une surface transparente dans laquelle on peut ajouter des éléments qui eux s'afficheront 
                total_height += height

            # nom abeille
            nom_abeille = font.render(bees[i]._name, 1, (0,0,0))
            surface_dic['surface'][indice].blit(nom_abeille, (x, 0))
            # image abeille
            image = pygame.image.load(bees[i]._sprite)
            surface_dic['surface'][indice].blit(image, (x, 30))


            if bees[i]._price[1] == "honey":
                image = pygame.image.load("./Images/honey.png")
                surface_dic['surface'][indice].blit(pygame.transform.scale(image, (45, 45)), ( x + 65 + 21*len(str(bees[i].cost())), 343 ))
            elif bees[i]._price[1] == "water":
                image = pygame.image.load("./Images/water.png")
                surface_dic['surface'][indice].blit(pygame.transform.scale(image, (30, 30)), ( x + 75 + 21*len(str(bees[i].cost())), 350 ))
            elif bees[i]._price[1] == "metal":
                image = pygame.image.load("./Images/metal.png")
                surface_dic['surface'][indice].blit(pygame.transform.scale(image, (30, 30)), ( x + 75 + 21*len(str(bees[i].cost())), 350 ))
            elif bees[i]._price[1] == "uranium":
                image = pygame.image.load("./Images/uranium.png")
                surface_dic['surface'][indice].blit(pygame.transform.scale(image, (30, 30)), ( x + 75 + 21*len(str(bees[i].cost())), 350 ))
            elif bees[i]._price[1] == "pollen":
                image = pygame.image.load("./Images/pollen.png")
                surface_dic['surface'][indice].blit(pygame.transform.scale(image, (30, 30)), ( x + 75 + 21*len(str(bees[i].cost())), 350 ))   

            cost = font.render("CE: " + str(bees[i].cost()) , 1, (0,0,0))
            surface_dic['surface'][indice].blit(cost, (x, 350)) 

            if bees[i]._price[1] == "honey":
                image = pygame.image.load("./Images/honey.png")
                surface_dic['surface'][indice].blit(pygame.transform.scale(image, (45, 45)), ( x + 85 + 22*len(str(bees[i]._price[0])), 393 ))
            elif bees[i]._price[1] == "water":
                image = pygame.image.load("./Images/water.png")
                surface_dic['surface'][indice].blit(pygame.transform.scale(image, (30, 30)), ( x + 90 + 22*len(str(bees[i]._price[0])), 400 ))
            elif bees[i]._price[1] == "metal":
                image = pygame.image.load("./Images/metal.png")
                surface_dic['surface'][indice].blit(pygame.transform.scale(image, (30, 30)), ( x + 90 + 22*len(str(bees[i]._price[0])), 400 ))
            elif bees[i]._price[1] == "uranium":
                image = pygame.image.load("./Images/uranium.png")
                surface_dic['surface'][indice].blit(pygame.transform.scale(image, (30, 30)), ( x + 90 + 22*len(str(bees[i]._price[0])), 400 ))
            elif bees[i]._price[1] == "pollen":
                image = pygame.image.load("./Images/pollen.png")
                surface_dic['surface'][indice].blit(pygame.transform.scale(image, (30, 30)), ( x + 90 + 22*len(str(bees[i]._price[0])), 400 ))

            prix = font.render( "Prix: " + str(bees[i]._price[0]), 1, (0,0,0))
            surface_dic['surface'][indice].blit(prix, (x, 400))
        
            if bees[i].category() == "worker":
                prod = font.render("Production: " + str(bees[i].prod()) + "    /s" , 1, (0,0,0))
                surface_dic['surface'][indice].blit(prod, (x, 300))

                if bees[i].ressource() == "honey":
                    image = pygame.image.load("./Images/honey.png")
                    surface_dic['surface'][indice].blit(pygame.transform.scale(image, (45, 45)), ( x + 200 + 21*len(str(bees[i].prod())), 293 ))
                elif bees[i].ressource() == "water":
                    image = pygame.image.load("./Images/water.png")
                    surface_dic['surface'][indice].blit(pygame.transform.scale(image, (30, 30)), ( x + 210 + 21*len(str(bees[i].prod())), 300 ))
                elif bees[i].ressource() == "metal":
                    image = pygame.image.load("./Images/metal.png")
                    surface_dic['surface'][indice].blit(pygame.transform.scale(image, (30, 30)), ( x + 210 + 21*len(str(bees[i].prod())), 300 ))
                elif bees[i].ressource() == "uranium":
                    image = pygame.image.load("./Images/uranium.png")
                    surface_dic['surface'][indice].blit(pygame.transform.scale(image, (30, 30)), ( x + 210 + 21*len(str(bees[i].prod())), 300 ))
                elif bees[i].ressource() == "pollen":
                    image = pygame.image.load("./Images/pollen.png")
                    surface_dic['surface'][indice].blit(pygame.transform.scale(image, (30, 30)), ( x + 210 + 21*len(str(bees[i].prod())), 300 ))


                
            
            elif bees[i].category() == "fighter":

                image = pygame.image.load("./Images/sword.png")
                surface_dic['surface'][indice].blit(pygame.transform.scale(image, (30, 30)), ( x + 92 + 21*len(str(bees[i].strength())), 300 )) 

                strength = font.render("PDC: " + str(bees[i].strength()) , 1, (0,0,0))
                surface_dic['surface'][indice].blit(strength, (x, 300))

                prix = font.render( "Prix: " + str(bees[i]._price[0]), 1, (0,0,0))
                surface_dic['surface'][indice].blit(prix, (x, 400))
            # boutons
            if bees[i].required_level() <= hive.level():
                bouton = button((212,180,0), x, 450, 390, 75, w, h,'Acheter', font='comicsans', sizeFont=50, get=bees[i]._name)
                surface_dic['buttons'].append(bouton)
                bouton.draw_button(surface_dic['surface'][indice])
            else:
                bouton = button((169, 169, 169), x, 450, 390, 75, w, h,"Niveau " + str(bees[i].required_level()) + " requis" , font='comicsans', sizeFont=50, get=None)
                bouton.draw_button(surface_dic['surface'][indice])

            x += 450 

        for i in range (0, len(surface_dic['buttons'])):
            surface_dic['buttons'][i]._x += 200
            surface_dic['buttons'][i]._y += 250

        value = 550
        for i in range (3, len(surface_dic['buttons'])):
            
            if i % 3 == 0 and i != 3:
                value += 550
            surface_dic['buttons'][i]._y += value


        final_surface = pygame.Surface((width, total_height), pygame.SRCALPHA)
        y = 0
        for surface in surface_dic['surface']:
            final_surface.blit(surface, (0, y))
            y += height
        
        surface_dic['surface'] = final_surface

        return surface_dic

    def display_shop(self, w, h, shop_bees, hive):
        #on redessine la surface
        surface = pygame.Surface((1920,1080))
        surface.blit(self._background, (0, 0))

        # création du texte du shop
        font = pygame.font.SysFont('comicsans', 70)
        welcome = font.render("Magasin", 1, (0,0,0))
        surface.blit(welcome, (820, 120))

        #Init des boutons
        self._button_dic = {
            "buy_bee_button" : [],
            "back_button" : button((255,180,255), 1720, 985, 180, 75, w, h, 'Retour', sizeFont=50)
        }

        # liste des surfaces
        bees_surfaces = self.display_shop_bee(shop_bees, hive, w, h)

        # Bouton Quitter

        self._button_dic["back_button"].draw_button(surface)
    
        surface = self.standard_line(surface)

        font = pygame.font.SysFont('comicsans', 30)
        PDC = font.render("PDC: point de combat", 1, (0,0,0))
        surface.blit(PDC, (1700, 60))
        CE = font.render("CE: Coût d'entretien", 1, (0,0,0))
        surface.blit(CE, (1700, 80))

        return surface, bees_surfaces
    
    