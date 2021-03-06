import pygame
import math
from pygame_textinput import TextInput
from create_button import button
from pygame.locals import *

class live_display():
    _tick = 60
    _shop_input = TextInput()
    _accepted_event1 = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
    _accepted_event2 = [K_BACKSPACE, K_DELETE, K_RETURN, K_RIGHT, K_LEFT, K_END, K_HOME, KEYUP]
    _temp_buttons = None
    _scroll_y = 0
    _black_surface = pygame.Surface((1920,1080), 255)
    _black_surface.set_alpha(190)

    def __init__(self, w, h, hive):
        self._w = w
        self._h = h
        self._hive = hive
        

    def give_display(self, live, alert, surface, events, buttons, first_call, bees_surfaces, scroll_y, territory, hive_territories): # permet d'appeler la méthode de live_display correspondant à l'affichage en cours, grâce à live
        if live == "menu":
             return self.live_menu(surface, alert, buttons)
        elif live == "management":
            return self.live_management(surface, events, buttons, alert, bees_surfaces, scroll_y)  
        elif live == "shop":
            return self.live_shop(surface, events, buttons, alert, first_call, bees_surfaces, scroll_y)
        elif live == "fight_menu":
            return self.live_fight_menu(surface, buttons, alert, first_call, territory, hive_territories)
        elif live == "up":
            return self.live_up(surface, bees_surfaces, scroll_y, events, buttons, alert, first_call)
    
    def live_up(self, surface, bees_surfaces, scroll_y, events, buttons, alert, first_time):
        max_y = 950
        scroll_surface, up_buttons, scroll_y = self.scroll(bees_surfaces, events, scroll_y, max_y)
        #positionner correctement purchase buttons
    
        surface = self.display_ressources(surface)

        buttons['upgrade_purchase'] = []
        buttons['desc'] = []

        for but in up_buttons:
            if but._text == "Description":
                buttons['desc'].append(but)
            else:
                buttons['upgrade_purchase'].append(but)

        pos_x = 400
        pos_y = 200 # valeurs liées aux boutons de display de la bee_surface
        
        container_surface = pygame.Surface((1200, 1000), pygame.SRCALPHA)
        
        container_surface.blit(scroll_surface, (0, scroll_y))

        surface.blit(container_surface, (pos_x, pos_y))

        good_up = None

        font = pygame.font.SysFont('comicsans', 50)

        #print("DEBUT", alert, first_time)

        if alert != None:
            if first_time == True:
                self._temp_buttons = buttons
                first_time = False
            for up in self._hive._upgrades:
                if up._name == alert[1] and up._lvl == alert[2]:
                    good_up = up

            surface.blit(self._black_surface, (0,0))

            msg = font.render(good_up._description, 1, (255,255,255))
            surface.blit(msg, (975-len(good_up._description)*9,550))
            
            buttons = {"ok": button((255,180,255), 900, 600, 150, 80, self._w, self._h, 'Ok', font='comicsans', sizeFont=40)}
            buttons["ok"].draw_button(surface)
        elif alert == None and first_time == False:
            buttons = {}
            buttons = self._temp_buttons
            first_time = True

        

        
        
        return surface, scroll_y, buttons, alert, first_time

    def live_fight_menu(self, surface, buttons, alert, first_call, sent_territory, hive_territories):
        
        # print(sent_territory, alert, first_call)

        if sent_territory != None and alert == None:
            if first_call == True:
                self._temp_buttons = buttons
                first_call = False
            
            for territory in hive_territories:
                if territory._name == sent_territory:
                    buttons = {}
                    surface.blit(self._black_surface, (0,0))
                    font = pygame.font.SysFont('comicsans', 50)
                    msg = font.render(territory._display_name, 1, (255,255,255))
                    surface.blit(msg, (900-len(territory._display_name)*7.5 ,400))
                    msg = font.render(territory._description, 1, (255,255,255))
                    surface.blit(msg, (900-len(territory._description)*8,450))
                    
                    if territory._possession == False:

                        msg = font.render("Force: " + str(territory.strength()), 1, (255,255,255))
                        surface.blit(msg, (810,500))
                        msg = font.render("Recompenses:", 1, (255,255,255))
                        surface.blit(msg, (780,550))
                        msg = font.render("+1 niveau", 1, (255,255,255))
                        surface.blit(msg, (820,600))
                        msg = font.render( str(territory.strength()), 1, (255,255,255))
                        surface.blit(msg, (900-len(str(territory.strength()))*7,650))

                        image = pygame.image.load("./Images/pollen.png")
                        surface.blit(pygame.transform.scale(image, (30, 30)), ( 890 + 20*len(str(territory.strength())), 650 ))

                        msg = font.render( str(territory.strength()), 1, (255,255,255))
                        surface.blit(msg, (900-len(str(territory.strength()))*7,700))

                        if territory.ressource() == "honey":
                            image = pygame.image.load("./Images/honey.png")
                            surface.blit(pygame.transform.scale(image, (30, 30)), ( 890 + 20*len(str(territory.strength())), 700 ))
                        elif territory.ressource() == "water":
                            image = pygame.image.load("./Images/water.png")
                            surface.blit(pygame.transform.scale(image, (30, 30)), ( 890 + 20*len(str(territory.strength())), 700 ))
                        elif territory.ressource() == "metal": 
                            image = pygame.image.load("./Images/metal.png")
                            surface.blit(pygame.transform.scale(image, (30, 30)), ( 890 + 20*len(str(territory.strength())), 700 ))
                        elif territory.ressource() == "uranium":
                            image = pygame.image.load("./Images/uranium.png")
                            surface.blit(pygame.transform.scale(image, (30, 30)), ( 890 + 20*len(str(territory.strength())), 700 ))


                        buttons["back"] = button((255,180,255), 950, 750, 150, 80, self._w, self._h, 'Retour', font='comicsans', sizeFont=40)
                        buttons["back"].draw_button(surface)

                        buttons["attack"] = button((255,180,255), 700, 750, 150, 80, self._w, self._h, 'Attaquer', font='comicsans', sizeFont=40)
                        buttons["attack"].draw_button(surface)
                    
                    else:
                        msg = font.render('Vous possédez déjà ce territoire !', 1, (255,255,255))
                        surface.blit(msg, (650,600))
                        buttons["back"] = button((255,180,255), 825, 750, 150, 80, self._w, self._h, 'Retour', font='comicsans', sizeFont=40)
                        buttons["back"].draw_button(surface)

        elif alert == "Done":
            buttons = self._temp_buttons
            alert = None
        # elif alert == "mine":
        #     font = pygame.font.SysFont('comicsans', 40)
        #     msg = font.render("Vous possédez déjà ce territoire", 1, (255,255,255))
        #     surface.blit(msg, (700,550))
        #     buttons = {"confirm" : button((255,180,255), 700, 600, 150, 80, self._w, self._h, 'Retourner sur la carte', font='comicsans', sizeFont=40)}
        #     buttons["confirm"].draw_button(surface)
        elif alert == "victory":
            
            surface.blit(self._black_surface, (0,0))
            font = pygame.font.SysFont('comicsans', 40)
            msg = font.render("Vous avez envahi ce territoire !", 1, (255,255,255))
            surface.blit(msg, (700,550))
            buttons = {"confirm" : button((255,180,255), 825, 600, 150, 80, self._w, self._h, 'Retour', font='comicsans', sizeFont=40)}
            buttons["confirm"].draw_button(surface)
            first_call = True
        elif alert == "cant_win":
            surface.blit(self._black_surface, (0,0))
            font = pygame.font.SysFont('comicsans', 40)
            msg = font.render("Votre armée est trop faible pour envahir le territoire", 1, (255,255,255))
            surface.blit(msg, (575,550))
            buttons = {"confirm" : button((255,180,255), 825, 600, 150, 80, self._w, self._h, 'Retour', font='comicsans', sizeFont=40)}
            buttons["confirm"].draw_button(surface)
        elif alert == None and first_call == False:
            buttons = self._temp_buttons
            first_call = True
        elif sent_territory == None and alert == None:
            self._temp_buttons = buttons
            

        return surface, buttons, first_call, alert

    def live_menu(self, surface, alert, buttons):
        
        surface = self.display_ressources(surface)
        
        # alert upgrade_choice
        if alert == "upgrade_choice":
            

            
            surface.blit(self._black_surface, (0,0))
            # display_surface = pygame.Surface((600, 150), pygame.SRCALPHA)
            
            # surface.blit(display_surface, (760, 480)) 

            buttons = {"fight_upgrades" : button((255,180,255), 730, 450, 200, 80, self._w, self._h, 'Combat', font='comicsans', sizeFont=55),
                        "hive_upgrades" : button((255,180,255), 990, 450, 200, 80, self._w, self._h, 'Ruche', font='comicsans', sizeFont=55),
                        "cancel" : button((212,180,0), 892, 550, 135, 55, self._w, self._h,'Annuler', font='comicsans', sizeFont=33)
                    }
            buttons["fight_upgrades"].draw_button(surface)
            buttons["hive_upgrades"].draw_button(surface)
            buttons["cancel"].draw_button(surface)

        return surface, buttons

    def live_management(self, surface, events, buttons, alert, bees_surfaces, scroll_y):
        max_y = 830
        scroll_surface, delete_buttons, scroll_y = self.scroll(bees_surfaces, events, scroll_y, max_y)
        
        buttons['delete_bee_button'] = delete_buttons

        surface = self.display_ressources(surface)

        pos_x = 150
        pos_y = 250
        
        container_surface = pygame.Surface((1500, 850), pygame.SRCALPHA)
        
        container_surface.blit(scroll_surface, (0, scroll_y))

        surface.blit(container_surface, (pos_x, pos_y))

        alert = ""

       

        return surface, "", buttons, alert, scroll_y
       


    def live_shop(self, surface, events, buttons, alert, first_call, bees_surfaces, scroll_y):
        max_y = 830
        scroll_surface, purchase_buttons, scroll_y = self.scroll(bees_surfaces, events, scroll_y, max_y)
        #positionner correctement purchase buttons
    
        
        buttons['buy_bee_button'] = purchase_buttons

        pos_x = 200
        pos_y = 250 # valeurs liées aux boutons de display de la bee_surface
        
        container_surface = pygame.Surface((1500, 850), pygame.SRCALPHA)
        
        container_surface.blit(scroll_surface, (0, scroll_y))

        surface.blit(container_surface, (pos_x, pos_y))
        

        surface = self.display_ressources(surface)
        
        # print(bees_surfaces[0][1])
        
        delete = False
        give_event = []      
        for event in events:
            if event.type == KEYDOWN:
                for accepted_tchong in self._accepted_event1:
                    if event.unicode == accepted_tchong:
                        give_event.append(event)
                        #print(event)
                        break
                for accepted_tchang in self._accepted_event2:
                    if event.key == accepted_tchang:
                        give_event.append(event)
                        if event.key == K_BACKSPACE:
                            delete = True
                        #print(event)
                        break

        if alert == "Buy":
            if first_call == True:
                self._temp_buttons = buttons
                first_call = False
                buttons = {}
            elif first_call == False:
                
                surface.blit(self._black_surface, (0,0))
                input_surface = pygame.Surface((400, 80))
                input_surface.fill(pygame.Color('White'))
                input_surface.blit(self._shop_input.get_surface(), (180,27))
                
                
                
                if len(self._shop_input.get_text()) < 10:
                    self._shop_input.update(give_event)
                elif delete == True:
                    self._shop_input.update(give_event)

                surface.blit(input_surface, (760, 480)) 

                buttons = {"cancel_buy" : button((255,180,255), 860, 615, 200, 80, self._w, self._h, 'Annuler Achat', font='comicsans', sizeFont=35)}
                buttons["cancel_buy"].draw_button(surface)

         

        elif alert == "CantBuy":
            if first_call == True:
                self._temp_buttons = buttons
                first_call = False
                buttons = {}
            elif first_call == False:
                
                surface.blit(self._black_surface, (0,0))
                buttons = {"cant_buy_alert" : button((255,50,0,0), 760, 480, 400, 60, self._w, self._h,'Ressource insuffisante', font='comicsans', sizeFont=50)}
                buttons["cant_buy_alert"].draw_button(surface)
        elif alert == "GetRideOfThisShit":
            self._shop_input.clear_text()
            buttons = self._temp_buttons
            self._temp_buttons = None
            alert = None 

        elif alert == "confirm_purchase":
            
            surface.blit(self._black_surface, (0,0))
            display_surface = pygame.Surface((400, 80))
            font = pygame.font.SysFont('comicsans', 50)
            msg = font.render("Achat effectué !", 1, (0,0,0))
            display_surface.fill(pygame.Color('White'))
            display_surface.blit(msg, (65,25))
                
            surface.blit(display_surface, (760, 480)) 

            buttons = {"purchase_confirmation" : button((255,180,255), 860, 615, 200, 80, self._w, self._h, 'Continuer', font='comicsans', sizeFont=35)}
            buttons["purchase_confirmation"].draw_button(surface)
       
        return surface, self._shop_input.get_text(), buttons, first_call, alert, scroll_y

    def scroll(self, surface, events, y, max_y):
        buttons = surface['buttons']
        surface = surface['surface']
        pixels = 40
        for event in events:
            if event.type == MOUSEBUTTONDOWN and event.button == 5: # vers le haut
                y -= pixels
                if y <= 0 and y > -(surface.get_height() - max_y):
                    buttons = self.new_button_pos(buttons, pixels, "-")
                else:
                    y += pixels
            if event.type == MOUSEBUTTONDOWN and event.button == 4: # vers le bas
                y += pixels
                if y <= 0:
                    buttons = self.new_button_pos(buttons, pixels, "+")
                else:
                    y -= pixels


        return surface, buttons, y

    def new_button_pos(self, buttons, pixels, axe):
        for i in range (0, len(buttons)):
            if axe == "+":
                buttons[i]._y += pixels
            elif axe == "-":
                buttons[i]._y -= pixels
            
        return buttons

    def text_rendering(self, font, sizeFont, text):
        font = pygame.font.SysFont(font, sizeFont)
        text = font.render(text, 1, (0,0,0))
        return text

    def display_ressources(self, surface):
        x = 10
        for ressource in self._hive._ressource:
            texte = self.translate_ressources(ressource)
            disp = texte + ": " + str(math.ceil(self._hive._ressource[ressource]))
            texte = self.text_rendering("comicsans", 40, disp)
            surface.blit(texte, (x, 14))
            x += 300
        
        text = "Lvl: " + str(self._hive._level)
        text = self.text_rendering("comicsans", 40, text)
        surface.blit(text, (x, 14))
        
        return surface

    def translate_ressources(self, name):
        if name == "honey":
            return "Miel"
        if name == "water":
            return "Eau"
        if name == "metal":
            return "Métal"
        if name == "uranium":
            return "Uranium"
        if name == "pollen":
            return "Pollen"
        
